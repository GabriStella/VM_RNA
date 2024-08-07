# import mysql.connector


# config = {
#     'user': 'RNAuser',
#     'password': '7RKlo1StosGVSCnx',
#     'host': 'localhost',
#     'database': 'RNAuser'
# }

# conn = mysql.connector.connect(**config
# )

# cursor = conn.cursor()

# cursor.execute("SELECT DISTINCT regione FROM rna_aiuti_individuali")
# results = cursor.fetchall()

# cursor.close()
# conn.close()

# processed_values = []

# for row in results:
#     regione_values = row[0].split(',')
#     for value in regione_values:
#         processed_values.append(value.strip())

# final_list = sorted(set(processed_values))
# percorsor=""
# with open('REGIONI.txt', 'w', encoding='utf-8') as file:
#     for item in final_list:
#         file.write(f"{item},\n")

def leggi_opzioni_da_file(nome_file):
    percorso_file=f"VAR_DINAMICHE\\{nome_file}"
    with open(percorso_file, 'r', encoding='utf-8') as file:
        contenuto = file.read()
        opzioni = [opzione.strip() for opzione in contenuto.split(',') if opzione.strip()]
    return opzioni


per_ultag=leggi_opzioni_da_file("UAG.txt")
print(per_ultag[0])