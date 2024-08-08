import datetime
import pandas as pd
import xml.etree.ElementTree as ET
from lxml import etree
import time
import os
import re
from tqdm import tqdm

xml_folder = "N:\\035-DEMINIMIS\\01-DOWNLOAD_DATI\\xml"   #  'N:\\035-DEMINIMIS\\01-DOWNLOAD_DATI\\'
output_folder = "N:\\035-DEMINIMIS\\02-CONVERSIONE_DATI\\CSV_GABRIELE_OK"



def remove_escapes(cell,column_name):
    if isinstance(cell, str):
        cleaned_cell = re.sub(r'[\n\r\t]', '', cell)
        cleaned_cell = cleaned_cell.replace(';', '.,')
        return cleaned_cell
    else:
        return cell
def read_processed_files():
    try:
        with open('processed_files.txt', 'r') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        open('processed_files.txt', 'a').close()
        return []

columns_to_keep = {
    'CAR'                           :        'Identificativo Misura (CAR)',
    'TITOLO_MISURA'                 :        'Titolo Misura',
    'DES_TIPO_MISURA'               :        'Tipo Misura',
    'COD_CE_MISURA'                 :        'Numero di riferimento della misura',
    'BASE_GIURIDICA_NAZIONALE'      :        'Norma Misura',
    'SOGGETTO_CONCEDENTE'           :        'Autorità Concedente',
    'COR'                           :        'COR',
    'TITOLO_PROGETTO'               :        'Titolo Progetto',
    'DESCRIZIONE_PROGETTO'          :        'Descrizione',
    'DATA_CONCESSIONE'              :        'Data Concessione',
    'CUP'                           :        'Cup',
    'ATTO_CONCESSIONE'              :        'Atto Concessione',
    'DENOMINAZIONE_BENEFICIARIO'    :        'Denominazione Beneficiario',
    'CODICE_FISCALE_BENEFICIARIO'   :        'C.F. Beneficiario',
    'DES_TIPO_BENEFICIARIO'         :        'Dimensione Beneficiario',
    'REGIONE_BENEFICIARIO'          :        'Regione',
    'ID_COMPONENTE_AIUTO'           :        'Identificativo componente',
    'DES_PROCEDIMENTO'              :        'Tipo procedimento',
    'DES_REGOLAMENTO'               :        'Regolamento/Comunicazione',
    'DES_OBIETTIVO'                 :        'Obiettivo',
    'SETTORE_ATTIVITA'              :        'Settore di attività',
    'COD_STRUMENTO'                 :        'Codice Strumento',
    'DES_STRUMENTO'                 :        'Strumento di aiuto',
    'ELEMENTO_DI_AIUTO'             :        'Elemento di aiuto',
    'IMPORTO_NOMINALE'              :        'Importo Nominale'
}

data = []

CTK={
    'CAR',
    'TITOLO_MISURA',              
    'DES_TIPO_MISURA',            
    'COD_CE_MISURA',              
    'BASE_GIURIDICA_NAZIONALE',   
    'SOGGETTO_CONCEDENTE',        
    'COR',                        
    'TITOLO_PROGETTO',            
    'DESCRIZIONE_PROGETTO',       
    'DATA_CONCESSIONE',           
    'CUP',                        
    'ATTO_CONCESSIONE',           
    'DENOMINAZIONE_BENEFICIARIO', 
    'CODICE_FISCALE_BENEFICIARIO',
    'DES_TIPO_BENEFICIARIO',      
    'REGIONE_BENEFICIARIO'
}       

processed_files = read_processed_files()
for filename in tqdm(os.listdir(xml_folder), desc="Elaborazione dei file XML"):
    if filename.endswith(".xml") and filename not in processed_files:
        ora_corrente = datetime.datetime.now()
        file_path = os.path.join(xml_folder, filename)
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        file_size_mb_int = int(file_size_mb)
        print(f"Processing file: {filename} dimensioni: {file_size_mb_int}")
        print(f"    {ora_corrente.strftime("%H:%M:%S")}")
        file= os.path.join(xml_folder, filename)
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(file, parser)
        root = tree.getroot()

        data = []
        start_time = time.time()
        i=0
        namespace = {'ns': 'http://www.rna.it/RNA_aiuto/schema'}
        for aiuto in root.findall('ns:AIUTO', namespace):
            if i == 0 or i % 100000 == 0:
                ora_corrente = datetime.datetime.now()
                print(f"    {i} - {ora_corrente.strftime("%H:%M:%S")}")
            i+=1
            common_values = {element: aiuto.find(f'ns:{element}', namespace).text if aiuto.find(f'ns:{element}', namespace) is not None else None for element in CTK}
            for componente in aiuto.findall('.//ns:COMPONENTE_AIUTO', namespace):
                common_values1={
                    'ID_COMPONENTE_AIUTO': componente.find('ns:ID_COMPONENTE_AIUTO', namespace).text  if   componente.find('ns:ID_COMPONENTE_AIUTO', namespace)       is not None else None,
                    'DES_PROCEDIMENTO'   : componente.find('ns:DES_PROCEDIMENTO', namespace).text     if   componente.find('ns:DES_PROCEDIMENTO', namespace)          is not None else None,
                    'DES_REGOLAMENTO'    : componente.find('ns:DES_REGOLAMENTO', namespace).text      if   componente.find('ns:DES_REGOLAMENTO', namespace)           is not None else None,
                    'DES_OBIETTIVO'      : componente.find('ns:DES_OBIETTIVO', namespace).text        if   componente.find('ns:DES_OBIETTIVO', namespace)             is not None else None,
                    'SETTORE_ATTIVITA'   : componente.find('ns:SETTORE_ATTIVITA', namespace).text     if   componente.find('ns:SETTORE_ATTIVITA', namespace)          is not None else None

                }
                for strumento in componente.findall('.//ns:STRUMENTO_AIUTO', namespace):
                    row = common_values.copy()
                    row.update(common_values1)
                    row.update({
                    'COD_STRUMENTO': strumento.find('ns:COD_STRUMENTO', namespace).text if strumento.find('ns:COD_STRUMENTO', namespace) is not None else None,
                    'DES_STRUMENTO': strumento.find('ns:DES_STRUMENTO', namespace).text if strumento.find('ns:DES_STRUMENTO', namespace) is not None else None,
                    'ELEMENTO_DI_AIUTO': strumento.find('ns:ELEMENTO_DI_AIUTO', namespace).text if strumento.find('ns:ELEMENTO_DI_AIUTO', namespace) is not None else None,
                    'IMPORTO_NOMINALE': strumento.find('ns:IMPORTO_NOMINALE', namespace).text if strumento.find('ns:IMPORTO_NOMINALE', namespace) is not None else None,
                    })
                    data.append(row)

        df = pd.DataFrame(data)
        df=df[['CAR', 'TITOLO_MISURA', 'DES_TIPO_MISURA','BASE_GIURIDICA_NAZIONALE','COR','TITOLO_PROGETTO', 'DESCRIZIONE_PROGETTO', 'DATA_CONCESSIONE','CUP', 'ATTO_CONCESSIONE', 'DENOMINAZIONE_BENEFICIARIO', 'CODICE_FISCALE_BENEFICIARIO', 'DES_TIPO_BENEFICIARIO', 'REGIONE_BENEFICIARIO','SOGGETTO_CONCEDENTE', 'COD_CE_MISURA', 'ID_COMPONENTE_AIUTO', 'DES_PROCEDIMENTO', 'DES_REGOLAMENTO', 'DES_OBIETTIVO', 'SETTORE_ATTIVITA', 'DES_STRUMENTO', 'COD_STRUMENTO', 'ELEMENTO_DI_AIUTO', 'IMPORTO_NOMINALE']]
        df.rename(columns=columns_to_keep, inplace=True)
        def convert_to_int(x):
            try:
                return str(x)
            except ValueError:
                return None
        df_cleaned = df.apply(lambda col: col.apply(remove_escapes, column_name=col.name))
        df_cleaned['Data Concessione'] = df_cleaned['Data Concessione'].str.split('+').str[0]
        df_cleaned['Data Concessione'] = pd.to_datetime(df_cleaned['Data Concessione'], format='%Y-%m-%d')
        # df_cleaned['Data Concessione'] = df_cleaned['Data Concessione'].dt.strftime('%d-%m-%Y')

        
        
        output_file = os.path.join(output_folder, filename.replace(".xml", ".csv"))
        ora_corrente = datetime.datetime.now()
        print(f"    inizio salvataggio alle - {ora_corrente.strftime("%H:%M:%S")}")
        df_cleaned.to_csv(output_file, sep='|', index=False, encoding='utf-8-sig')
        ora_corrente = datetime.datetime.now()
        print(f"    fine: {ora_corrente.strftime("%H:%M:%S")} \n")
        with open('processed_files.txt', 'a') as f:
            f.write(filename + '\n')

print("Inizio DB SQL")

os.system("python Riempi_Tabella.py > PopolaSQL.log 2>&1")

