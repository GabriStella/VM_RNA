import time
from datetime import datetime, timedelta
import os
from interrogazioni import *

RANTOLA=leggi_opzioni_da_file("TEMP.txt")
TEMP = RANTOLA[0]
if TEMP == "rna_aiuti_individuali":
    print(f"stai usando aiuti_individuali passerai a {TEMP}")
elif TEMP == "aiuti_individuali":
    print(f"stai usando rna_aiuti_individuali passerai a {TEMP}")
else: 
    print("errorissimo")

percorso="VAR_DINAMICHE\\TAB_UP.txt"
with open(percorso, 'w', encoding='utf-8') as file:
    file.write(f"{TEMP}")

file="VAR_DINAMICHE\\TEMP.txt"
os.remove(file)
