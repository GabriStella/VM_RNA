# Tool di compilazione e consultazione aiuti di stato

Questo semplice tool nasce con l'obiettivo di velocizzare il processo di verifica di quanto un'azienda può ancora ricevere in regime De Minimis. 

E' importante per noi sapere quando un'azienda ha ancora una capienza positiva in questo regime perchè ci consente di verificare se è possibile richiedere l'aiuto che l'azienda vuole richiedere o offrire alle aziende soluzioni ad hoc sulla base della situazione specifica. 

Come vedremo nel corso di questa guida questo Tool ci viene in aiuto in entrambe queste situazioni. 

Per creare il database, che può essere definito il cuore di questo strumento, abbiamo fatto affidamento sulla disponbilità pubblica di questi dati, come riportato sul sito del ministero infatti: 
"*I dati contenuti e le informazioni presenti sul [Registro Aiuti](https://www.rna.gov.it/open-data#opendataLink-80), ove non diversamente segnalato all’interno della documentazione informativa, sono resi disponibili con licenza
["IODL: Italian Open Data License v2.0"](https://www.dati.gov.it/iodl/2.0/).*"

Implementato il database abbiamo infine aggiunto la possibilità di eseguire delle ricerche avanzate su diversi campi in modo da riuscire ad estrapolare informazioni che possono supportare le scelte strategiche a livello aziendale.

## Indice

- [Utilizzo](#utilizzo)
- [Aggiornamento Periodico](#Aggiornamento-Periodico)
- [Migrazione](#Migrazione)
- [Licenza](#licenza)
## Utilizzo
Accedendo al [link](https://rna.cdr-italia.com/) messo a disposizione dall'azienda sarà possibile, **tramite VPN**, accedere alla seguente interfaccia: 

![Home](Immagini\Home.png)

Sulla sinistra è possibile scegliere il tipo di tool di cui si ha bisogno. 
### De Minimis
Questo tool consente di valorizzare nel primo campo il codice fiscale dell'azienda per la quale si desidera verificare la disponibilità in regime De Minimis;

successivamente, se ci sono delle imprese collegate bisogna valorizzare il campo più a destra con il numero necesssario. 

A questo punto cliccando sul pulsante **Esegui Ricerca** in basso avremo le informazioni di cui abbiamo bisogno, qualche promemoria su come comportarci e la possibilità di scaricare il nostro file interno di verifica. 

#### Esempio pratico
Supponiamo di voler fare la ricerca per un nostro cliente **POWERSOFT** che ha 3 imprese collegate: 

![Home](Immagini\Pre-Ricerca.png)

Successivamente cliccando Esegui ricerca avremo 3 messaggi importanti che compariranno: 

![Risultato](Immagini\risultato.png)
Il primo messaggio racchiude un rapido riscontro con il nome dell'azienda per la quale abbiamo eseguito la ricerca e il valore in euro di aiut che l'azienda può ancora richiedere in regime De Minimis. 

![Allert1](Immagini\Allert1.png)
Questo primo allert è molto importante, perchè, purtroppo, il Ministero non sempre fornisce dati aggiornati al 100% di conseguenza è **Sempre** buona pratica verificare con il cliente su negli ultimi 15/30 giorni hanno avuto provvedimenti di revoca o concessione. 

![Allert2](Immagini\Allert2.png)
Questo allert ci ricorda che gli aiuti alle aziende nel settore agricolo e dell'acquacultura non vengono valorizzati in questo database e di conseguenza riporta il link cliccabile per procedere alla verifica nel caso l'azienda si trovi in uno di questi settori. 

![pulsantino](Immagini\st.button.png)

Infine cliccando il pulsante **Download Excel** è possibile scaricare il riepilogo della ricerca. 

### Ricerca avanzata 

Scegliendo invece La ricerca avanzata avremo a disposizione diversi campi che possiamo scegliere se valorizzare o meno, è importante però che almeno un campo venga valorizzato per eseguire la ricerca. 
I campi di ricerca sono: 
`Identificativo Misura (CAR)`, `Titolo Misura`, `COR`, `Descrizione`, `Data Concessione`, `CUP`, `Denominazione Beneficiario`, `C.F. Beneficiario`, `Regione`, `Autorità Concedente`, `Numero di riferimento della misura`, `Tipo Procedimento`, `Regolamento/Comunicazione`, `Settore di attività`. 
Una volta valorizzati i campi ed eseguita la ricerca avremo subito un'anteprima della nostra ricerca, se i risultati hanno meno di 50 aiuti allora potremo visualizzare subito tutti i risultati della nostra ricerca: 
![Tutti](Immagini\Lessthen50.png)

Se invece la nostra ricerca restituisce più di 50 risultati, ma meno di 100.000 allora la visualizzazione riguarderà solo i primi 50 risultati, ma l'excel riassuntivo scaricabile sarà comunque composto da tutti i campi. 
![Quasi_Tutti](Immagini\Morethen50.png)


Se la ricerca restituisce più di 100.000 risultati, invece, continueremo a visualizzare i primi 50 risultati, ma l'excel sarà composto solo dai primi 100.000, questo limite è modificabile per esigenze specfiche; tuttavia è importante tenerlo se non stretttamente necessaria la sua rimozione in quanto la compilazione di excel eccessivamente corposi appesantisce troppo il sistema rendendo il programma lento macchinoso sotto queste circostanze
![Haiesagerato](Immagini\HaiEsagerato.png)

Infine, abbiamo il tasto per scaricare l'excel riepilogativo della nostra ricerca

![Bottoneavanzato](Immagini\button_avanzata.png)




## Aggiornamento Periodico

Come riportato sul sito i file vengono aggiornati settimanalmente, purtroppo ad oggi non è ancora possibile automatizzare il download dei file a causa di rigidi controlli sul sito del ministero. 

Di conseguenza i file sono da scaricare manualmente in formato `zip` (Molto più veloce rispetto alla versione integrale `xml`)

Prima di procedere al download è necessario inizzializzare la cartella di destinazione al seguente percorso: `N:\035-DEMINIMIS\01-DOWNLOAD_DATI\NUOVO RNA`  eliminando il contenuto al suo interno e sostituendolo con quello all'interno della cartella: `N:\035-DEMINIMIS\01-DOWNLOAD_DATI\__FORMAT_AGGIORNAMENTO_RNA`

Una volta esguito questo passaggio è possibile passare all'operazione di download dei dati dal [sito del Ministero](https://www.rna.gov.it/open-data/aiuti). 

Una volta completato il download sarà sufficiente aprire il prompt dei comandi dala stessa macchina su cui è installato il codice sorgente ed eseguire il comando `cd desktop && [... cd fino alla cartella madre] && AV\Scripts\Activate && python Inizio_Aggiornamento.py` (queto inzierà il processo di Estrazione Zip, Conversione da xml a csv, inizializzazione vecchio db, Riempimento nuovo db aggiornamento menù a tendina per la ricerca avanzata)

Il comando ad oggi per avviare l'aggiornamento è: `cd desktop && cd ciao && cd VM_RNA && AV\Scripts\Activate && python Inizio_Aggiornamento.py`

**NB** : Aggiornare questo percorso qualora dovesse cambiare qualcosa

### Fasi di aggiornamento (post download):
è importante sapere che su SQL devono essere presenti due Tabelle: `rna_aiuti_individuali` e `aiuti_individuali`, verrà sempre utilizzata la più recente, ma qualora qualcosa dovesse andare storto nell'aggiornamento sarà sempre rendere di nuovo operativa la cartella più recente mdificando il file `UA_TAB.txt` all'interno della cartella `VAR_DINAMCIHE`.
In caso di **migrazione** è necessario fare il running dello script `Tabella.py` avendo cura di inserire i nuovi parametri di connessione al db e cambiando alternativamente ad ogni run la variabile `Nome_Tabella` con `rna_aiuti_individuali` prima e `aiuti_individuali` poi. 
Di seguito un'attenta spiegazione del funzionamento del codice di aggiornamento al fine di poter rapidamente modificare le variabili strutturali qualora venga effettuata una migrazione. 

#### Fase 1 (inizializzazione ed estrazione): 
Inizio aggiornamento ed estrazione zip, {File di esecuzione Inizio_Aggiornamento.py} 

Questo script creerà un file temporaneo `TEMP.txt` che conterrà il nome della tabella non attualmente in uso in modo da inizializzarla e popolarla. 
Successivamente darà indicazioni al terminale di runnare lo sript `Estrazione_Zip.py`, che come suggerisce il nome prenderà i file zip nella cartella `NUOVO_RNA` valorizzata nella variabile `base_dir` e li salverà nella cartella di destinazione valorizzata nella variabile `cartella_di_appoggio`. 
**Questo processo può impiegare fino a 2 ore e mezza**

#### Fase 2 (conversione): 
Comletata l'estrazione si eseguirà automaticamente il file `conversione.py` il quale esegue la conversione da `xml` a `csv`, purtroppo questo è il processo più time consuming può richiedere fino a 30 ore a seconda delle dimensioni dei file.
Le variabili di maggiore interesse in questo script sono: `xml_folder` deve corrispondere alla variabile `cartella_di_appoggio` precedentemente menzionata e `output_folder` percorso nel quale desideriamo vengano salvati i nuovi `csv`. 

#### Fase 3 (popola il db):
Una volta finito il lungo processo di conversione inizia il processo di popolamento del db eseguito dal file `Riempi_Tabella.py`. In questo processo le variabili fondamentali sono date da `folder_path` che deve corrispondere alla precedentemente menzionata `output_folder`. Questo processo può richiedere fino a 8 ore.

## Migrazione
Questa sezione offre una guida puntuale qualora si renda necessario l'installazione del codice sorgente su un'altra macchina, virtuale o non.
1. **Dopo aver installato la versione più recente di python e git**
   - Check: `python --version` e `git --version`
2. **Aprire prompt dei comandi ed eseguire**:
   - `cd fino a alla cartella di destinazione desiderata`
   - `git clone link_repo`
   - `python -m venv AV`
   - `AV\Scripts\Activate`
   - `pip install requirements.txt`
   - Installazione MySQL, configurazione appropriata di **interrogazioni.py** e di tutti i file di cui al capitolo [Aggiornamento Periodico](#Aggiornamento-Periodico)
   - `streamlit run app.py`

una volta eseguite queste istruzioni il Tool sarà disponibile solo dalla macchina sulla quale sono stati eseguiti questi comandi (in particolare all'indirizzo http://localhost:8501) e dai dispositivi che navigano sulla stessa rete della macchina; se viene è utilizzata una VPN i dispositivi per visualizzarla correttamente dovranno disporre di una VPN compatibile con quella su cui gira il codice sorgente. 

Se si vuole rendere disponibile per tutti gli utenti della rete aziendale sarà necessario utilizzare un **Reverse-Proxy** sul localhost della macchina. 

## Licenza
Licenza consultabile all'indirizzo [https://www.dati.gov.it/content/italian-open-data-license-v20]