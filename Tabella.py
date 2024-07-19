import mysql.connector


config = {
    'user': 'RNAuser',
    'password': '7RKlo1StosGVSCnx',
    'host': 'localhost',
    'database': 'RNAuser'
}


conn = mysql.connector.connect(**config)
cursor = conn.cursor()


table_name = 'RNA_TAB'
create_table_query = '''
    CREATE TABLE RNA (
        `Identificativo Misura (CAR)` VARCHAR(255),
        `Titolo Misura` VARCHAR(1000),
        `Tipo Misura` VARCHAR(255),
        `Norma Misura` VARCHAR(1000),
        `COR` INT,
        `Titolo Progetto` VARCHAR(1000),
        `Descrizione` TEXT,
        `Data Concessione` VARCHAR(100),
        `Cup` VARCHAR(255),
        `Atto Concessione` VARCHAR(1000),
        `Denominazione Beneficiario` VARCHAR(1000),
        `C.F. Beneficiario` VARCHAR(255),
        `Dimensione Beneficiario` VARCHAR(255),
        `Regione` VARCHAR(255),
        `Autorità Concedente` VARCHAR(1000),
        `Numero di riferimento della misura` VARCHAR(1000),
        `Identificativo componente` INT,
        `Tipo procedimento` VARCHAR(1000),
        `Regolamento/Comunicazione` VARCHAR(1000),
        `Obiettivo` VARCHAR(1000),
        `Settore di attività` VARCHAR(1000),
        `Strumento di aiuto` VARCHAR(1000),
        `Codice Strumento` VARCHAR(255),
        `Elemento di aiuto` FLOAT,
        `Importo Nominale` FLOAT,
        `Codice Univoco` VARCHAR(255)
    )
'''

cursor.execute(create_table_query)
print(f"Tabella {table_name} creata con successo.")

cursor.close()
conn.close()