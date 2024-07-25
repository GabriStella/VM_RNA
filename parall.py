import csv
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import collections
import os
import re

def calculate_hash(row):
    data_string = '|'.join(map(str, row))
    hash_object = hashlib.sha256(data_string.encode())
    return hash_object.hexdigest()

def process_block(block):
    hash_list_local=[]
    i = 1
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

def process_files(files):
    hash_list = []
    element_counters = collections.defaultdict(int)
    start_time = datetime.datetime.now()
    print(f"Inizio : {start_time.strftime('%H:%M:%S')}")

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for file in files:
            start_time1 = datetime.datetime.now()
            print(f"nuovo file: {start_time1.strftime('%H:%M:%S')}")
            for block in read_csv_in_blocks(file):
                futures.append(executor.submit(process_block, block))

        for future in as_completed(futures):
            hash_list.extend(future.result())

    end_time = datetime.datetime.now()
    print(f"Finito: {end_time.strftime('%H:%M:%S')}")
    print(f"Righe Tot: {len(hash_list)}")
    hash=[tup[-1] for tup in hash_list]
    counter = collections.Counter(hash)
    row=[tup[0] for tup in hash_list]
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

    # for element in modified_hash_list:
    #     if "_" in element: 
    #         print(element)
    # return modified_hash_list



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
        # files=['N:\\035-DEMINIMIS\\02-CONVERSIONE_DATI\\CSV_GABRIELE_OK\\OpenData_Aiuti_2022_07.csv']
        # year="2024"
        # month="02"
        print(f"PROCESSO : {year}-{month}")
        modified_hash_list = process_files(files)

if __name__ == "__main__":
    main()

