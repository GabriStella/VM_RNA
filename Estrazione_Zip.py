import os
import zipfile
import datetime

def read_processed_files():
    try:
        with open('processed_files_zip.txt', 'r') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        open('processed_files_zip.txt', 'a').close()
        return [] 

def estrai_zip_in_cartella_di_appoggio(base_dir, cartella_di_appoggio):
    if not os.path.exists(cartella_di_appoggio):
        os.makedirs(cartella_di_appoggio)
    processed_files = read_processed_files()
    ora_corrente = datetime.datetime.now()
    print(ora_corrente.strftime("%H:%M:%S")+" \n")
    for anno in range(2014, 2025):  
        anno_dir = os.path.join(base_dir, str(anno))
        if os.path.exists(anno_dir) and os.path.isdir(anno_dir):
            for nome_file in os.listdir(anno_dir):
                percorso_file = os.path.join(anno_dir, nome_file)
                if zipfile.is_zipfile(percorso_file) and nome_file not in processed_files:
                    with zipfile.ZipFile(percorso_file, 'r') as zip_ref:
                        zip_ref.extractall(cartella_di_appoggio)
                    print(f'Contenuto di {nome_file} estratto in {cartella_di_appoggio}')
                else:
                    print(f'{nome_file} non è un file ZIP, ignorato.')
                ora_corrente = datetime.datetime.now()
                print(ora_corrente.strftime("%H:%M:%S")+" \n")
                with open('processed_files_zip.txt', 'a') as f:
                    f.write(nome_file + '\n')


base_dir = "N:\\035-DEMINIMIS\\01-DOWNLOAD_DATI\\NUOVO RNA"  
cartella_di_appoggio = "N:\\035-DEMINIMIS\\01-DOWNLOAD_DATI\\xml"  


estrai_zip_in_cartella_di_appoggio(base_dir, cartella_di_appoggio)

os.system('python conversione.py > Processo_Aggiornamento\\Conversione_XML_CSV.log 2>&1')