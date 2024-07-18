import pandas as pd
import pyodbc

server = 'VDI-RNA\\SQLEXPRESS'  
database = 'RNA'
trusted_connection = 'yes'
driver = 'ODBC Driver 17 for SQL Server'  

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'

conn = pyodbc.connect(conn_str)

table_name = 'Open_Data'
create_table_query = f'''
    CREATE TABLE {table_name} (
        [Identificativo Misura (CAR)] NVARCHAR(400),
        [Titolo Misura] NVARCHAR(4000),
        [Tipo Misura] NVARCHAR(1000),
        [Norma Misura] NVARCHAR(4000),
        [COR] INT,
        [Titolo Progetto] NVARCHAR(4000),
        [Descrizione] NVARCHAR(4000),
        [Data Concessione] VARCHAR(100),
        [Cup] NVARCHAR(4000),
        [Atto Concessione] NVARCHAR(4000),
        [Denominazione Beneficiario] NVARCHAR(4000),
        [C.F. Beneficiario] NVARCHAR(4000),
        [Dimensione Beneficiario] NVARCHAR(4000),
        [Regione] NVARCHAR(4000),
        [Autorità Concedente] NVARCHAR(3000),
        [Numero di riferimento della misura] NVARCHAR(4000),
        [Identificativo componente] INT,
        [Tipo procedimento] NVARCHAR(4000),
        [Regolamento/Comunicazione] NVARCHAR(4000),
        [Obiettivo] NVARCHAR(4000),
        [Settore di attività] NVARCHAR(4000),
        [Strumento di aiuto] NVARCHAR(4000),
        [Codice Strumento] NVARCHAR(4000),
        [Elemento di aiuto] FLOAT,
        [Importo Nominale] FLOAT ,
        [Codice Univoco] NVARCHAR(4000)       
    );
'''

cursor = conn.cursor()
cursor.execute(create_table_query)
conn.commit()
conn.close()
print(f'Tabella "{table_name}" creata con successo.')