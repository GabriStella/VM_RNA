import mysql.connector

config = {
    'user': 'root',
    'host': 'localhost',
    'database': 'RNAuser'
}

def verify_codice_univoco():
    queries = [
        "SELECT `Codice Univoco` FROM `rna` LIMIT 100;",
        "SELECT `Codice Univoco`, LENGTH(`Codice Univoco`) as length FROM `rna` LIMIT 100;",
        "SELECT `Codice Univoco` FROM `rna` WHERE TRIM(`Codice Univoco`) LIKE '%_%' LIMIT 100;",
        "SELECT `Codice Univoco` FROM `rna` WHERE `Codice Univoco` NOT LIKE '%_%' LIMIT 100;",
        "SELECT `Codice Univoco` FROM `rna` WHERE INSTR(`Codice Univoco`, '_') = 0 LIMIT 100;"
    ]
    
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        for query in queries:
            print(f"Executing query: {query}")
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(row)
            print("\n")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

verify_codice_univoco()