import os
from interrogazioni import *

RANTOLA=leggi_opzioni_da_file("TAB_UP.txt")
UTAB = RANTOLA[0]

if UTAB == "aiuti_individuali":
    nuova= "rna_aiuti_individuali"
    print("aggiungo rna")
elif UTAB == "rna_aiuti_individuali":
    nuova= "aiuti_individuali"
    print("RIMUOVO RNA")
else:
    print("errorissimo")
    
percorso="VAR_DINAMICHE\\TEMP.txt"
with open(percorso, 'w', encoding='utf-8') as file:
    file.write(f"{nuova}")


os.system('python zzz3.py > Processo_Aggiornamento\\Conversione_XML_CSV.log 2>&1')