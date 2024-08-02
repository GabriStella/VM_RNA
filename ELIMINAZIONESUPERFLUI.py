import mysql.connector
from mysql.connector import pooling, Error
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime

def elimina_batch(connection_pool):
    while True:
        conn = connection_pool.get_connection()
        cursor = conn.cursor()

        try:
            delete_query = """
            DELETE FROM CUPROVA
            WHERE CODU NOT IN (
                SELECT COD_UN
                FROM TempCodiciGlobal
            )
            LIMIT 500
            """

            cursor.execute(delete_query)
            conn.commit()
            rows_deleted = cursor.rowcount

            if rows_deleted == 0:
                break

            yield rows_deleted

        except Error as e:
            print(f"Errore durante l'eliminazione in batch: {e}")
            break

        finally:
            cursor.close()
            conn.close()

def esegui_eliminazione_batch(connection_pool):
    total_rows_deleted = 0
    for rows_deleted in elimina_batch(connection_pool):
        total_rows_deleted += rows_deleted
        print(f"{rows_deleted} righe eliminate nel batch corrente.")
    return total_rows_deleted

def elimina_righe_batch():
    config = {
        'user': 'RNAuser',
        'password': '7RKlo1StosGVSCnx',
        'host': 'localhost',
        'database': 'RNAuser'
    }
    
    try:
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            **config
        )
        
        conn = connection_pool.get_connection()
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS TempCodiciGlobal (COD_UN TEXT)")

        cursor.execute("TRUNCATE TABLE TempCodiciGlobal")
        
        cursor.execute("INSERT INTO TempCodiciGlobal (COD_UN) SELECT COD_UN FROM CU")
        cursor.execute("CREATE INDEX idx_cod_un ON TempCodiciGlobal (COD_UN)")
        conn.commit()

        cursor.close()
        conn.close()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(esegui_eliminazione_batch, connection_pool) for _ in range(5)]
            total_rows_deleted = 0

            for future in as_completed(futures):
                try:
                    result = future.result()
                    total_rows_deleted += result
                except Exception as e:
                    print(f"Errore durante l'esecuzione del futuro: {e}")

        print(f"{total_rows_deleted} righe eliminate con successo.")

    except Error as e:
        print(f"Errore: {e}")
    
    finally:
        if connection_pool:
            conn = connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS TempCodiciGlobal")
            conn.commit()
            cursor.close()
            conn.close()

end_time = datetime.datetime.now()
print(f"    Iniziato: {end_time.strftime('%H:%M:%S')}")
elimina_righe_batch()
end_time = datetime.datetime.now()
print(f"    Finito: {end_time.strftime('%H:%M:%S')}")

print("FINE")
print("FORSE") 