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
from interrogazioni import *


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

    for i in range(len(row)):
        if counter[hash[i]] > 1:
            element_counters[hash[i]] += 1
            if element_counters[hash[i]] == 1:
                row[i].append(hash[i])
            else:
                row[i].append(f"{hash[i]}_{element_counters[hash[i]]}")
        else:
            row[i].append(hash[i])

    # datetime_column_index = 7
    # for linea in row:

    #     original_datetime_str = linea[datetime_column_index]
    #     parsed_datetime = datetime.datetime.strptime(original_datetime_str, '%d-%m-%Y')
        
    #     mysql_formatted_datetime = parsed_datetime.strftime('%Y-%m-%d')
        
  
    #     linea[datetime_column_index] = mysql_formatted_datetime
    # Nome_Tabella='rna_Aiuti_Individuali'
    RANTOLA=leggi_opzioni_da_file("TEMP.txt")
    Nome_Tabella=RANTOLA[0]
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(insert_rows, batch, Nome_Tabella) for batch in process_batches(row, batch_size)]
        
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
        print(f"Mese : {year}-{month}")
        process_files(files, batch_size=150)
    
    oggi =datetime.datetime.now() 
    formattata = oggi.strftime('%d-%m-%Y')
    with open('VAR_DINAMICHE\\UAG.txt', 'w', encoding='utf-8') as file:
        file.write(f"{formattata}")
    
    percorso_script = 'VAR_DINAMICHE\\tendine.py'
    os.system(f"python {percorso_script}")


if __name__ == "__main__":
    main()
