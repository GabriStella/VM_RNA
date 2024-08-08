import os
from interrogazioni import *
import datetime



def svuota_tabella(tabella):
    try:
        config = {
            'user': 'RNAuser',
            'password': '7RKlo1StosGVSCnx',
            'host': 'localhost',
            'database': 'RNAuser'
        }
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        if conn.is_connected():
            cursor = conn.cursor()
            query = f"TRUNCATE TABLE {tabella}"
            cursor.execute(query)
            conn.commit()
            print(f"La tabella '{tabella}' è stata svuotata con successo.")
    
    except Exception as e:
        print(f"Errore durante la connessione al database: {e}")
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connessione al database chiusa.")



RANTOLA=leggi_opzioni_da_file("TAB_UP.txt")
UTAB = RANTOLA[0]

if UTAB == "aiuti_individuali":
    a="continua"
    nuova= "rna_aiuti_individuali"
    print("aggiungo rna")
elif UTAB == "rna_aiuti_individuali":
    a="continua"
    nuova= "aiuti_individuali"
    print("RIMUOVO RNA")
else:
    a="STOP"
    print("errorissimo")
    
percorso="VAR_DINAMICHE\\TEMP.txt"
with open(percorso, 'w', encoding='utf-8') as file:
    file.write(f"{nuova}")

percorso="VAR_DINAMICHE\\UAG.txt"
DATA = datetime.datetime.today()
oggi= DATA.strftime("%d-%m-%Y")
with open(percorso, 'w', encoding='utf-8') as file:
    file.write(f"{oggi}")

svuota_tabella(nuova)

if a == "continua": 
    os.system('python Estrazione_Zip.py > Processo_Aggiornamento\\EstrazioneZIP.log 2>&1')


