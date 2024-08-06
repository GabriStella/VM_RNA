import mysql.connector


config = {
    'user': 'RNAuser',
    'password': '7RKlo1StosGVSCnx',
    'host': 'localhost',
    'database': 'RNAuser'
}

conn = mysql.connector.connect(**config
)

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

with open('REGIONI.txt', 'w', encoding='utf-8') as file:
    for item in final_list:
        file.write(f"{item},\n")
