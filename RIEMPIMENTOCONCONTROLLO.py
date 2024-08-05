import pandas as pd
import mysql.connector
from mysql.connector import pooling
import csv
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import collections
import os
import re
from itertools import islice

config = {
    'user': 'RNAuser',
    'password': '7RKlo1StosGVSCnx',
    'host': 'localhost',
    'database': 'RNAuser',
    'pool_name': 'mypool',
    'pool_size': 5
}

pool = mysql.connector.pooling.MySQLConnectionPool(**config)

def insert_rows(batch, table_name):
    insert_query = f'''
        INSERT INTO {table_name} (
            `Identificativo Misura (CAR)`, `Titolo Misura`, `Tipo Misura`, `Norma Misura`, `COR`, `Titolo Progetto`, `Descrizione`, 
            `Data Concessione`, `Cup`, `Atto Concessione`, `Denominazione Beneficiario`, `C.F. Beneficiario`, `Dimensione Beneficiario`, 
            `Regione`, `Autorità Concedente`, `Numero di riferimento della misura`, `Identificativo componente`, `Tipo procedimento`, `Regolamento/Comunicazione`, 
            `Obiettivo`, `Settore di attività`, `Strumento di aiuto`, `Codice Strumento`, `Elemento di aiuto`, `Importo Nominale`, `Codice Univoco`
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    '''
    
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()
        cursor.executemany(insert_query, batch)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_hash(batch, table_name):
    insert_query = f'''
        INSERT INTO {table_name} (CODU) VALUES (%s)
    '''
    
    conn = None
    cursor = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()
        cursor.executemany(insert_query, batch)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def process_batches(rows, batch_size=150):
    for i in range(0, len(rows), batch_size):
        yield rows[i:i + batch_size]

def calculate_hash(row):
    data_string = '|'.join(map(str, row))
    hash_object = hashlib.md5(data_string.encode())
    return hash_object.hexdigest()

def process_block(block):
    hash_list_local = []
    for row in block:
        Codice_Univoco = calculate_hash(row)
        hash_list_local.append((row, Codice_Univoco))
    return hash_list_local

def read_csv_in_blocks(file_path, block_size=150000):
    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        next(csv_reader)  
        block = []
        for index, row in enumerate(csv_reader):
            if index > 0 and index % block_size == 0:
                yield block
                block = []
            block.append(row)
        if block:
            yield block


def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            break
        yield chunk

def zero_uno_batch(hashes):
    conn = pool.get_connection()
    nome_tabella = 'rna_aiuti_individuali' #! AGGIUSTARE
    batch_size = 10000  
    result_dict = {}

    try:
        cursor = conn.cursor()
        for batch in chunked_iterable(hashes, batch_size):
            # hashes_str = ','.join(['%s'] * len(batch))
            # test = f"""
            # SELECT 
            #     `Codice Univoco`, 
            #     CASE 
            #         WHEN COUNT(*) > 0 THEN 1
            #         ELSE 0
            #     END AS is_not_unique
            # FROM 
            #     `{nome_tabella}`
            # WHERE 
            #     `Codice Univoco` IN ({hashes_str})
            # GROUP BY `Codice Univoco`
            # HAVING is_not_unique = 0;
            # """


            subqueries = [f"SELECT '{h}' AS hash" for h in batch]
            hashes_str = " UNION ALL ".join(subqueries)

            query = f"""
            SELECT hash AS `Codice Univoco`
            FROM (
                {hashes_str}
            ) AS subquery
            LEFT JOIN {nome_tabella} AS t
            ON subquery.hash = t.`Codice Univoco`
            WHERE t.`Codice Univoco` IS NULL;
            """

            cursor.execute(query)
            results = cursor.fetchall()
            result_dict.update({row[0] for row in results})



    except Exception as e:
        print(f"Errore durante l'esecuzione della query batch: {e}")
    finally:
        cursor.close()
        conn.close()

    return result_dict

def process_row(index, row, hash, counter, element_counters):
    d = 0
    current_hash = hash[index]
    modified_row = row[index]
    
    if counter[current_hash] > 1:
        element_counters[current_hash] += 1
        if element_counters[current_hash] == 1:
            modified_row.append(current_hash)
        else:
            new_hash = f"{current_hash}sbatti{element_counters[current_hash]}"
            hash[index]=new_hash
            modified_row.append(new_hash)
            print(index)
    else:
        modified_row.append(current_hash)
    
    return (index, modified_row, d, hash)

def process_files(files, batch_size=150):
    hash_list = []
    element_counters = collections.defaultdict(int)
    start_time = datetime.datetime.now()
    print(f"    Inizio: {start_time.strftime('%H:%M:%S')}")
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for file in files:
            start_time1 = datetime.datetime.now()
            print(f"    nuovo file: {start_time1.strftime('%H:%M:%S')}")
            for block in read_csv_in_blocks(file):
                futures.append(executor.submit(process_block, block))

        for future in as_completed(futures):
            hash_list.extend(future.result())

    end_time = datetime.datetime.now()
    print(f"    Finito: {end_time.strftime('%H:%M:%S')}")
    print(f"    Righe Tot: {len(hash_list)}")
    
    hash = [tup[-1] for tup in hash_list]
    counter = collections.Counter(hash)
    row = [tup[0] for tup in hash_list]
    modified_hash_list = []
    element_counters = collections.defaultdict(int)
    
    
    
    c = 0
    results = []
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_index = {executor.submit(process_row, i, row, hash, counter, element_counters): i for i in range(len(row))}
        for future in as_completed(future_to_index):
            i = future_to_index[future]
            try:
                index, modified_row, d, hash = future.result()
                results.append((index, modified_row, d))
            except Exception as e:
                print(f"Errore durante l'elaborazione della riga {i}: {e}")

    new_row = []
    # for index, modified_row, remove_row, d in results:
    #     if not remove_row:
    #         new_row.append(modified_row)

    end_time = datetime.datetime.now()
    print(f"    fine check row: {end_time.strftime('%H:%M:%S')}")

    unique_hashes = list(set(hash))  
    batch_results = zero_uno_batch(unique_hashes)  

    # dati_tuples = [(valore,) for valore in hash]
    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     futures = [executor.submit(insert_hash, batch, 'CUPROVA') for batch in process_batches(dati_tuples, batch_size)]
        
    #     for future in futures:
    #         future.result()
    # end_time = datetime.datetime.now()
    # print(f"    fine creazione CU: {end_time.strftime('%H:%M:%S')}")
    datetime_column_index = 7
    for linea in new_row: #! ROW PERò NON VA BENE, VORREMMO MODIFIED_row

        original_datetime_str = linea[datetime_column_index]
        parsed_datetime = datetime.datetime.strptime(original_datetime_str, '%d-%m-%Y')
        
        mysql_formatted_datetime = parsed_datetime.strftime('%Y-%m-%d')
        
  
        linea[datetime_column_index] = mysql_formatted_datetime
    nome_tabella='rna_aiuti_individuali'                                                #! OCCHIOLO
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(insert_rows, batch, nome_tabella) for batch in process_batches(new_row, batch_size)]
        
        for future in futures:
            future.result()

def main():
    folder_path = "N:\\035-DEMINIMIS\\02-CONVERSIONE_DATI\\CSV_GABRIELE_OK"  
    file_pattern = re.compile(r'OpenData_Aiuti_(\d{4})_(\d{2})_?.*\.csv')

    files_by_month = collections.defaultdict(list)

    for filename in os.listdir(folder_path):
        match = file_pattern.match(filename)
        if match:
            year, month = match.groups()
            files_by_month[(year, month)].append(os.path.join(folder_path, filename))

    for (year, month), files in sorted(files_by_month.items()):
        # files=['N:\\035-DEMINIMIS\\02-CONVERSIONE_DATI\\CSV_GABRIELE_OK\\OpenData_Aiuti_2024_02.csv']#, 'N:\\035-DEMINIMIS\\02-CONVERSIONE_DATI\\CSV_GABRIELE_OK\\OpenData_Aiuti_2024_02_002.csv', 'N:\\035-DEMINIMIS\\02-CONVERSIONE_DATI\\CSV_GABRIELE_OK\\OpenData_Aiuti_2024_02_003.csv', 'N:\\035-DEMINIMIS\\02-CONVERSIONE_DATI\\CSV_GABRIELE_OK\\OpenData_Aiuti_2024_02_004.csv', 'N:\\035-DEMINIMIS\\02-CONVERSIONE_DATI\\CSV_GABRIELE_OK\\OpenData_Aiuti_2024_02_005.csv', 'N:\\035-DEMINIMIS\\02-CONVERSIONE_DATI\\CSV_GABRIELE_OK\\OpenData_Aiuti_2024_02_006.csv']
        

        print(f"Mese : {year}-{month}")
        process_files(files, batch_size=150)

if __name__ == "__main__":
    main()
