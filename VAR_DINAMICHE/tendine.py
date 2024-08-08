import mysql.connector
import os

config = {
    'user': 'RNAuser',
    'password': '7RKlo1StosGVSCnx',
    'host': 'localhost',
    'database': 'RNAuser'
}

conn = mysql.connector.connect(**config)

cursor = conn.cursor()

cursor.execute("SELECT DISTINCT regione FROM rna_aiuti_individuali")
results = cursor.fetchall()

cursor.close()
conn.close()

processed_values = []

for row in results:
    regione_values = row[0].split(',')
    for value in regione_values:
        processed_values.append(value.strip())

final_list = sorted(set(processed_values))
percorso="VAR_DINAMICHE\\REGIONI.txt"
with open(percorso, 'w', encoding='utf-8') as file:
    for item in final_list:
        file.write(f"{item},\n")


percorso="VAR_DINAMICHE\\TEMP.txt"
with open(percorso, 'r', encoding='utf-8') as file:
    contenuto = file.read()
    opzioni = [opzione.strip() for opzione in contenuto.split(',') if opzione.strip()]



UTAB = opzioni[0]
percorso="VAR_DINAMICHE\\TAB_UP.txt"
with open(percorso, 'w', encoding='utf-8') as file:
    file.write(f"{UTAB}")


file="VAR_DINAMICHE\\TEMP.txt"
file1="processed_files_zip.txt"
file2="processed_file.txt"
os.remove(file)
os.remove(file1)
os.remove(file2)