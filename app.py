import streamlit as st
from interrogazioni import *
import uuid
from datetime import date, datetime, timedelta
from streamlit.logger import get_logger
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import pandas as pd
import os
import subprocess

def app():

    # logger.info('Hello world')
    if 'cliente' not in st.session_state:
        start_time1 = datetime.now()
        print(f"    nuovo accesso: {start_time1.strftime('%H:%M:%S')}")
        UUID=str(uuid.uuid4())
        st.session_state.cliente = UUID
    UUID = st.session_state.cliente

    image_path = "C:\\Users\\g.stella\\Desktop\\CIAO\\logoCDR-2022-positivo_vert.png" 

    st.logo(image_path, icon_image=image_path) 
    per_ultag=leggi_opzioni_da_file("UAG.txt")
    TABELLA=leggi_opzioni_da_file("TAB_UP.txt")
    TABAGG=TABELLA[0]
    aa = st.sidebar.radio("Seleziona il tipo di tool di cui hai bisogno", ["De Minimis","Ricerca Avanzata", "Privato"], key=f"choosed_mood_{UUID}")#
    
    if aa== "De Minimis" :
        st.title("Verifica aiuti di stato")
        st.write(f"**`Dati Aggiornati al {per_ultag[0]}`**")


        col1, col2 = st.columns(2)
        with col1:
            cf_input= st.text_input("Codice Fiscale : ", key=f"get_cf_{UUID}")
        CFS={}
        if 'cf_input_value' not in st.session_state:
            st.session_state.cf_input_value = ""

        CFS["CF_1"]=cf_input

        cf_value = st.session_state.cf_input_value
        with col2:
            Collegate=st.text_input("Quante sono le imprese collegate? ",value=0)


        st.markdown(
            """
            <style>
            .instructions-light {
                background-color: #f0f0f5;
                border-left: 6px solid #0073e6;
                padding: 10px;
                margin: 10px 0;
                font-family: Arial, sans-serif;
                color: black;
            }
            .instructions-dark {
                background-color: #fff2cc;
                border-left: 6px solid #0073e6;
                padding: 10px;
                margin: 10px 0;
                font-family: Arial, sans-serif;
                color: white;
            }
            </style>
            <div class="instructions instructions-light" id="instruction-box">
                <h4>Ricorda:</h4>
                <ul>
                    <li>1: Non vanno inseriti i collegamenti tramite persona fisica;</li>
                    <ul>
                        <li>1.1: <strong>Eccezione</strong>: imprese individuali e lavoratori autonomi che svolgono attività economica;</li>
                    </ul>    
                    <li>2: Inserire solo imprese con sede in Italia.</li>
                </ul>
            </div>
            <script>
            // Funzione per applicare il tema
            function applyTheme(e) {
                var instructionBox = document.getElementById('instruction-box');
                if (e.matches) {
                    instructionBox.classList.remove('instructions-light');
                    instructionBox.classList.add('instructions-dark');
                } else {
                    instructionBox.classList.remove('instructions-dark');
                    instructionBox.classList.add('instructions-light');
                }
            }
                                                                                                                                        
            // Rilevamento del tema scuro
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', applyTheme);
            applyTheme(mediaQuery);
            </script>
            """,
            unsafe_allow_html=True
    )

        try:
            Collegate=int(Collegate)
            for i in range(2,Collegate+2) :
                if i%2==0:
                    with col1:
                        cf_inputs= st.text_input("Codice Fiscale : ",key=f"get_cf_{UUID}_{i}")
                else:
                    with col2:
                        cf_inputs= st.text_input("Codice Fiscale : ",key=f"get_cf_{UUID}_{i}")
                CFS[f"CF_{i}"]=cf_inputs
        except: 
            st.error(f"**{Collegate}** non sembra un numero ")

        if st.button("Esegui Ricerca"):
            start_time1 = datetime.now()
            print(f"    Ricerca: {start_time1.strftime('%H:%M:%S')}")
            try:
                CF_Result=Ask_CF(CFS)
                # st.write(NUOVO)
                
                # Visualizzazione= ["Identificativo Misura (CAR)", "Numero di riferimento della misura", "Titolo Misura", "Tipo Misura", "COR", "Titolo Progetto", "Data Concessione", "Denominazione Beneficiario", "C.F. Beneficiario", "Regione", "Regolamento/Comunicazione", "Elemento di aiuto"]
                # df_visualizzato = CF_Result[Visualizzazione]
                df_visualizzato = CF_Result.drop(columns=['id'])
                # st.dataframe(df_visualizzato, use_container_width=True)
                GENERALE = pd.DataFrame(columns=df_visualizzato.columns)
                AGRICOLTURA = pd.DataFrame(columns=df_visualizzato.columns)
                PESCA = pd.DataFrame(columns=df_visualizzato.columns)
                den_value = df_visualizzato.loc[df_visualizzato['C.F. Beneficiario'] == CFS["CF_1"].strip(), 'Denominazione Beneficiario'].iloc[0]
                st.write(den_value)
                for index, row in df_visualizzato.iterrows():
                    if "De Minimis" in row["Tipo procedimento"]:
                        GENERALE= pd.concat([GENERALE, pd.DataFrame([row])], ignore_index=True)
                    # if "2831" in row["Regolamento/Comunicazione"] :#or "1407" in row["Regolamento/Comunicazione"]:     
                    #     GENERALE= pd.concat([GENERALE, pd.DataFrame([row])], ignore_index=True)
                    # elif "1407" in row["Regolamento/Comunicazione"]:
                    #     GENERALE= pd.concat([GENERALE, pd.DataFrame([row])], ignore_index=True)
                    elif "1408" in row["Regolamento/Comunicazione"]:
                        AGRICOLTURA= pd.concat([AGRICOLTURA, pd.DataFrame([row])], ignore_index=True)
                    elif "717"  in row["Regolamento/Comunicazione"]: 
                        PESCA= pd.concat([PESCA, pd.DataFrame([row])], ignore_index=True)
                
                

                GENERALE['Data Concessione'] = pd.to_datetime(GENERALE['Data Concessione'])
                data_limite = datetime.now() - timedelta(days=3*365)
                df_filtro = GENERALE[GENERALE['Data Concessione'] >= data_limite]
                somma_importi_Generale = df_filtro['Elemento di aiuto'].sum()
                netto= 300000 - somma_importi_Generale
                # st.session_statef"Generale"] = somma_importi_Generale , den_value
                formatted_netto = f"{netto:,.2f}"
                if netto > 0 :  
                    url = "https://www.sian.it/GestioneTrasparenza/?op=0&referer=https%3A%2F%2Fwww.sian.it%2Fportale-sian%2Fsottosezione.jsp%3Fpid%3D6"
                    st.success(f"L'azienda **{den_value}** ha ancora a disposizione **{formatted_netto} €** in De Minimis")
                    st.warning("**ATTENZIONE**: \n \n  Confrontarsi con il cliente per verificare se ci sono stati negli ultimi 30 giorni: \n \n - NUOVE CONCESSIONI \n \n - PROVVEDIMENTI DI REVOCA \n \n in quanto queste variazioni potrebbero non essere aggiornate in questo calcolo. ")
                    st.warning("In caso di aziende nel settore agricolo e/o dell'acquacoltura consultare il [portale SIAN](%s)" % url)
                elif netto < 0 : 
                    st.warning("Sembrerebbe che l'azienda ha una capienza negativa in questo momento ..")
                    st.button("Chiama la guardi di finanza")
                elif netto == 0: 
                    st.warning("Esattamente zero euro disponibili 🫢")


                col1, col2, col3 = st.columns(3)
                if not GENERALE.empty:
                    GENERALE=CREA_DF(GENERALE)
                    excel1=COMPILA_EXCEL_gen(GENERALE)
                    oggi = date.today()
                    oggi_formato = oggi.strftime("%d-%m-%Y")
                    
                    with col1:
                            st.download_button(label='Download Excel - GENERALE', 
                                            data=excel1,
                                            file_name=f"DEMINIMIS_{den_value}_{oggi_formato} - GENERALE.xlsx",
                                            mime='application/xlsx')
                else: 
                    GENERALE=CREA_DF(GENERALE)
                    excel1=COMPILA_EXCEL_gen(GENERALE)
                    oggi = date.today()
                    oggi_formato = oggi.strftime("%d-%m-%Y")
                    
                    with col1:
                        st.download_button(label='Download Excel - GENERALE', 
                                        data=excel1,
                                        file_name=f"DEMINIMIS_{den_value}_{oggi_formato} - GENERALE.xlsx",
                                        mime='application/xlsx')

                if not AGRICOLTURA.empty:
                    AGRICOLTURA=CREA_DF(AGRICOLTURA)
                    excel2=COMPILA_EXCEL_agr(AGRICOLTURA)
                # if st.button('Download Excel'):
                    with col2:
                        st.download_button(label='Download Excel - AGRICOOLTURA', 
                                        data=excel2,
                                        file_name=f"DEMINIMIS_{den_value}_{oggi_formato} - AGRICOOLTURA.xlsx",
                                        mime='application/xlsx')

                if not PESCA.empty:
                    PESCA=CREA_DF(PESCA)
                    excel3=COMPILA_EXCEL_pes(PESCA)
                # if st.button('Download Excel'):
                    with col3:
                        st.download_button(label='Download Excel - PESCA', 
                                        data=excel3,
                                        file_name=f"DEMINIMIS_{den_value}_{oggi_formato} - PESCA e ACQUACOLTURA.xlsx",
                                        mime='application/xlsx')
            except Exception as e:
                st.error(f"Sembra che il codice Fiscale inserito non sia corretto... {e}")
    elif aa== "Ricerca Avanzata" :
        st.title("Consulta RNA")
        st.write(f"**`Dati Aggiornati al {per_ultag[0]}`**")
        op_reg = leggi_opzioni_da_file('REGIONI.txt') 
        # st.caption("Non è ancora consigliato usare questa pagina, non dovrebbe creare grossi problemi, ma potrebbe restituire degli errori perchè bisogna ancora sistemare un paio di cose in SQL")
        oggi = date.today()
        oggi_formato = oggi.strftime("%Y-%m-%d")
        PARAMETRI = ["Identificativo Misura (CAR)", 
                     "Titolo Misura",  
                     "COR", 
                     "Descrizione", 
                     "Data Concessione", 
                     "CUP", 
                     "Denominazione Beneficiario", 
                     "C.F. Beneficiario", 
                     "Regione", 
                     "Autorità Concedente",
                     "Numero di riferimento della misura",
                     "Tipo Procedimento", 
                     "Regolamento/Comunicazione", 
                     "Settore di attività"] 
        #st.sidebar.multiselect("Parametri di ricerca", PARAMETRI, key=f"choosed_param_{UUID}")
        richieste={}
        # if "Data Concessione" in PARAMETRI: 
        #     DATA=st.sidebar.radio("Data Concessione",["Intervallo di date", "Data Specifica", "Successiva a ", "Precedente a "], key=f"Spec_Data_{UUID}")
        col1, col2 = st.columns(2)



        for i in range(len(PARAMETRI)):
            param=PARAMETRI[i]
            if i % 2 == 0:
                if param=="Data Concessione": 
                    # if DATA ==  "Intervallo di date":
                    with col1:
                        input1 = st.date_input("Da", None,key=f"Datastart_{UUID}")
                    with col2:
                        input2 = st.date_input("A", None,key=f"Dataend_{UUID}")
                        
                    richieste["Data_Start"]= input1 if input1 is not None else ""
                    richieste["Data_End"]= input2 if input2 is not None else ""
                elif param == "Regione": 
                    with col1:
                        input=st.selectbox(f" {param} :", op_reg, key=f"get_{param}_{UUID}",placeholder="Scegliere un'opzione", index= None)
                        richieste[f"{param}"]=input if input is not None else ""
                else:
                    with col1:
                        input = st.text_input(f" {param} :",key=f"get_{param}_{UUID}")
                        richieste[f"{param}"]=input
  
            else:
                if param=="Data Concessione": 
                # if DATA ==  "Intervallo di date":
                    with col1:
                        input1 = st.date_input("Da", None,key=f"Datastart_{UUID}")
                    with col2:
                        input2 = st.date_input("A", None,key=f"Dataend_{UUID}")
                    
                    richieste["Data_Start"]=input1 if input1 is not None else ""
                    richieste["Data_End"]= input2 if input2 is not None else ""
                elif param == "Regione": 
                    with col2:
                        input=st.selectbox(f" {param} :", op_reg, key=f"get_{param}_{UUID}", placeholder="Scegliere un'opzione", index= None)
                        richieste[f"{param}"]=input if input is not None else ""
                else:
                    with col2:
                        input = st.text_input(f" {param} :",key=f"get_{param}_{UUID}")
                        richieste[f"{param}"]=input
        # st.write(TABAGG)
        a=0
        for key in richieste:
            # if richieste[key] == None: 
            #     richieste[key] = ""
            a+=1
            if richieste[key] != "" :
                
                if st.button("Esegui Ricerca"):
                    start_time1 = datetime.now()
                    print(f"    ADV_SMN: {start_time1.strftime('%H:%M:%S')}")

                    try:
                        with st.spinner("Eseguo la ricerca ..."):
                            ppp=ricerca_avanzata(richieste)

                        # st.write(richieste)
                        if len(ppp) > 50 and len(ppp) <= 99999:
                            st.warning(f"La tabella contiene {len(ppp)} righe, sono mostrate solo le prime 50")
                            df_ridotto = ppp.iloc[:50]
                            # st.write(len(ppp))
                        elif len(ppp) >99999:
                            df_ridotto = ppp.iloc[:50]
                            st.error("""
                                     Sembrerebbe che la ricerca restituisca più di 100.000 righe.
                                     
                                        l'excel sarà composto solo con le 100.000 più recenti, si prega di affinare la ricerca se si vuole risultati più precisi
                                     
                                     """)
                        else:
                            df_ridotto = ppp
                            st.success("Stai visualizzando tutti i risultati della ricerca")
                        Visualizzazione= ["Identificativo Misura (CAR)", "Numero di riferimento della misura", "Titolo Misura", "Tipo Misura", "COR", "Titolo Progetto", "Data Concessione", "Denominazione Beneficiario", "C.F. Beneficiario", "Regione", "Elemento di aiuto"]
                        df_visualizzato = df_ridotto[Visualizzazione]
                        st.dataframe(df_visualizzato, use_container_width=True)
                        with st.spinner("Sto compilando l'excel completo ..."):
                            excel=Excel_avanzato(ppp)

                        st.download_button(label='Download Riepilogo Ricerca', 
                                        data=excel,
                                        file_name=f"Ricerca_Avanzata_{oggi_formato}.xlsx",
                                        mime='application/xlsx')
                    except Exception as e: 
                        st.error(f"stg went wrong, cosa? ->  {e}")
                break

            if a == len(PARAMETRI):
                st.warning("**Compilare almeno un parametro di ricerca per procedere**")
        
        # st.write(richieste)
        # st.write(ppp)
    elif aa == "Privato":
        from pathlib import Path
        print("someone enter in privato")
        PW = st.text_input("SEI TU?", key="passwordd")
        if st.button("Si, sono io"):
            if PW== "MARANZA":
                # if st.button("Esegui Ciclo"):
                #     result = subprocess.run(['python', 'zzzzz.py'], capture_output=True, text=True)
                readme_path = Path('README.md')

                with readme_path.open('r', encoding='utf-8') as file:
                    readme_content = file.read()

                st.markdown(readme_content, unsafe_allow_html=True)
            
            
            else:
                print("accesso Negato") 
                st.write("sembra che non sia tu mi disp")
                # st.write("`RIP`")
    else:
        st.write("Mancata Selezione tool")
    # CF 


# except Exception as e:
#     st.error(f"Inserire nel Box il numero delle collegate, grazie. {e}")


def main():

    app()







if __name__ == '__main__':

    main()