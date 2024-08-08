import mysql.connector
import pandas as pd

config = {
    'user': 'RNAuser',
    'password': '7RKlo1StosGVSCnx',
    'host': 'localhost',
    'database': 'RNAuser'
}


conn = mysql.connector.connect(**config)
cursor = conn.cursor()

query = """
SELECT `Codice Univoco`
FROM `aiuti_individuali`
WHERE YEAR(`Data Concessione`) = 2021
  AND MONTH(`Data Concessione`) = 6;
"""

cursor.execute(query)

PROVA=["fc91f38d20961d82c26d3122cf643b11",
 "a94d66fdcaaa4282f8efee146afbe739",
 "ed1941312f2980c44bc14eec22d638fe",
 "4fd88a6e21000b5c6cb760425c24c82b",
 "ea0f228b4d4921507c0deb909a745082",
 "1d6d5f067e847a1f8f47f2abfb98c792",
 "b029b179351d8acc95fd8b53186cf6c9",
 "b4b2ae6c80a1b36bc4a328d3c504dbff",
 "ed2334b496d4619f562f915303d8ce81",
 "f1b33afc15e910458481669816252877",
 "5bfb266cd348163e97bc94040a718486",
 "fd1fe5b12e2823a82c3ae3c93ba111ca",
 "5b3416e422a39717ea54e4efe633e284",
 "ef8c027201f7d81521bc7dea58b0d9c9",
 "2c5c4c58069d3b57fad64fc74eb47004",
 "2bc24161ba42b254191c7deb11d2759e",
 "49ab3da35fe6a12b4fc0686969b52483",
 "5a8c21ec85a4e3f98dad040cfb5f2ab0",
 "42c9329b9e7fedf9d003579a48d43b50"]

# Fetch all the results
results = cursor.fetchall()
values = [row[0] for row in results]
list2=set(values)
list1=set(PROVA)

common_elements = [item for item in list1 if item in list2]

unique_to_list1 = [item for item in list1 if item not in common_elements]
unique_to_list2 = [item for item in list2 if item not in common_elements]


df = pd.DataFrame(results)

values = [row[0] for row in results]

if 'ed1941312f2980c44bc14eec22d638hfe' in values: 
    print("c'è")
elif '4fd88a6e21000b5c6cb760425c24c82' in values: 
    print("questo non dovrebbeesserci)")
elif 'b029b179351d8acc95fd8b53186cf6c9' in values: 
    print("se printa questo siamo a cavallo ciao fine.")

for row in results: 
    print(row[0])












