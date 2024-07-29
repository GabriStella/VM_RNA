import streamlit as st
from interrogazioni import *
import uuid
from datetime import date, datetime, timedelta
from streamlit.logger import get_logger
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import pandas as pd



def app():


    # logger.info('Hello world')
    if 'cliente' not in st.session_state:
        UUID=str(uuid.uuid4())
        st.session_state.cliente = UUID
    UUID = st.session_state.cliente

    
    aa = st.sidebar.radio("Seleziona il tipo di tool di cui hai bisogno", ["De Minimis","Ricerca Avanzata"], key=f"choosed_mood_{UUID}")
    if aa== "De Minimis" :
        st.title("Compila DeMinimis")
        # if "Generale" in st.session_state: 
        #     den_value, somma_importi_Generale = st.session_state["Generale"]
        #     st.success(f"{den_value}, {somma_importi_Generale}")
        
        cf_input= st.text_input("Codice Fiscale : ", key=f"get_cf_{UUID}")
        CFS={}
        if 'cf_input_value' not in st.session_state:
            st.session_state.cf_input_value = ""

        CFS["CF_1"]=cf_input

        cf_value = st.session_state.cf_input_value
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

        # try:
        Collegate=int(Collegate)
        if Collegate != "0":
            
            for i in range(2,Collegate+2) :
                cf_inputs= st.text_input("Codice Fiscale : ",key=f"get_cf_{UUID}_{i}")
                CFS[f"CF_{i}"]=cf_inputs
        if st.button("Esegui Ricerca"):
            try:
                CF_Result=Ask_CF(CFS)
                # st.write(NUOVO)
                
                # Visualizzazione= ["Identificativo Misura (CAR)", "Numero di riferimento della misura", "Titolo Misura", "Tipo Misura", "COR", "Titolo Progetto", "Data Concessione", "Denominazione Beneficiario", "C.F. Beneficiario", "Regione", "Regolamento/Comunicazione", "Elemento di aiuto"]
                # df_visualizzato = CF_Result[Visualizzazione]
                df_visualizzato = CF_Result.drop(columns=['id'])
                st.dataframe(df_visualizzato, use_container_width=True)
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
                    
                    st.success(f"L'azienda **{den_value}** ha ancora a disposizione **{formatted_netto} €** in De Minimis")
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
        # st.caption("Non è ancora consigliato usare questa pagina, non dovrebbe creare grossi problemi, ma potrebbe restituire degli errori perchè bisogna ancora sistemare un paio di cose in SQL")
        oggi = date.today()
        oggi_formato = oggi.strftime("%Y-%m-%d")
        PARAMETRI = st.sidebar.multiselect("Parametri di ricerca", ["Identificativo Misura (CAR)", "Titolo Misura",  "COR", "Descrizione", "Data Concessione", "CUP", "Denominazione", "C.F. Beneficiario", "Regione", "Autorita Concedente", "Numero di riferimento della misura", "Tipo Procedimento", "Regolamento/Comunicazione", "Settore di attività"], key=f"choosed_param_{UUID}")
        richieste={}
        if "Data Concessione" in PARAMETRI: 
            DATA=st.sidebar.radio("Data Concessione",["Intervallo di date", "Data Specifica", "Successiva a ", "Precedente a "], key=f"Spec_Data_{UUID}")
        for param in PARAMETRI:
            if param=="Data Concessione": 
                if DATA ==  "Intervallo di date":
                    st.write(f"<div style='text-align: center;'>{param}</div>", unsafe_allow_html=True)
                    col1, col2 = st.columns(2,vertical_alignment= 'center') 
                    with col1:
                        input1 = st.date_input("Da", datetime(2022, 1, 1),key=f"Datastart_{UUID}")
                    with col2:
                        input2 = st.date_input("A", datetime(2024, 1, 1),key=f"Dataend_{UUID}")
                    st.caption("La ricerca restituirà gli aiuti nel Range di date inserite")
                    richieste["Data_Start"]=input1
                    richieste["Data_End"]=input2
                elif DATA ==  "Successiva a ":
                
                    input = st.date_input(f" {param} :", datetime(2024, 1, 1),key=f"get_{param}_{UUID}")
                    st.caption("La ricerca restituirà gli aiuti successivi alla data inserita")
                    richieste["Data_Start"]=input
                elif DATA ==  "Precedente a ":
                    input = st.date_input(f" {param} :", datetime(2024, 1, 1),key=f"get_{param}_{UUID}")
                    st.caption("La ricerca restituirà gli aiuti precedenti alla data inserita")
                    richieste["Data_End"]=input
                else:  #! DATA SPECIFICA
                    input = st.date_input(f" {param} :", datetime(2024, 1, 1),key=f"get_{param}_{UUID}")
                    st.caption("La ricerca restituirà gli aiuti nella data inserita")
                    richieste[f"{param}"]=input
      
            else:
                input = st.text_input(f" {param} :",key=f"get_{param}_{UUID}")
                richieste[f"{param}"]=input
        if PARAMETRI != []: 
            if st.button("Esegui Ricerca"):
                try:
                    ppp=ricerca_avanzata(richieste)
                    # st.write(richieste)
                    if len(ppp) > 50:
                        st.warning(f"La tabella contiene {len(ppp)} righe, sono mostrate solo le prime 50")
                        df_ridotto = ppp.iloc[:50]
                        st.write(len(ppp))
                    else:
                        df_ridotto = ppp
                        st.write("TUTTO")
                    Visualizzazione= ["Identificativo Misura (CAR)", "Numero di riferimento della misura", "Titolo Misura", "Tipo Misura", "COR", "Titolo Progetto", "Data Concessione", "Denominazione Beneficiario", "C.F. Beneficiario", "Regione", "Elemento di aiuto"]
                    df_visualizzato = df_ridotto[Visualizzazione]
                    st.dataframe(df_visualizzato, use_container_width=True)
                    excel=Excel_avanzato(ppp)

                    st.download_button(label='Download Riepilogo Ricerca', 
                                    data=excel,
                                    file_name=f"Ricerca_Avanzata_{oggi_formato}.xlsx",
                                    mime='application/xlsx')
                except Exception as e: 
                    st.error(f"stg went wrong, cosa? ->  {e}")
        else: 
            st.warning("**Selezionare almeno un parametro di ricerca per procedere**")
        
        # st.write(richieste)
        # st.write(ppp)
    else:
        st.write("Mancata Selezione tool")
    # CF 


# except Exception as e:
#     st.error(f"Inserire nel Box il numero delle collegate, grazie. {e}")


def main():

    app()







if __name__ == '__main__':

    main()






    




# """#? QUESTI DA AGGIUNGERE IN RICERCA AVANZATA MI RACCOMANDO AGGIUNGERE NON SOLO LORO. 
# #             #? volendo aggiungiamo altri parametri di ricerca, ma sinceramente mi sembra inutile. 
#     # Data Concessione #! INSERIRE POSSIBILITà DI RANGE

    # end_date = date.today()
    # start_date = end_date - timedelta(days=3*365)
#     # st.warning("non modificare questo campo per la compilazione del file DEMINIMIS")
    
#     cf_input1= st.date_input("Data Concessione : ", (start_date, end_date),key=f"get_dc_{UUID}")
#     st.caption("Il periodo preso in considerazione inizialmente prevede già 3 anni indietro da oggi")
#     if len(cf_input1) == 2:
#         start_date, end_date = cf_input1
#         # Formattare le date come dd/mm/yyyy
#         formatted_start_date = start_date.strftime('%d/%m/%Y')
#         formatted_end_date = end_date.strftime('%d/%m/%Y')
#         st.write(f'L\'intervallo di date selezionato è dal {formatted_start_date} al {formatted_end_date}')
#     elif len(cf_input1) == 1:
#         formatted_start_date = start_date.strftime('%d/%m/%Y')
#     else: 
#         st.warning("nessun periodo selezionato")
#     if 'cf_input_value1' not in st.session_state:
#         st.session_state.cf_input_value1 = ""

#     st.session_state.cf_input_value1 = cf_input1

#     cf_value1 = st.session_state.cf_input_value1

#     # Denominazione Beneficiario
#     cf_input2= st.text_input("Denominazionee : ",key=f"get_db_{UUID}")

#     if 'cf_input_value2' not in st.session_state:
#         st.session_state.cf_input_value2 = ""

#     st.session_state.cf_input_value2 = cf_input2

#     cf_value2 = st.session_state.cf_input_value2

#     # COR
#     cf_input3= st.text_input("COR : ",key=f"get_COR_{UUID}")

#     if 'cf_input_value3' not in st.session_state:
#         st.session_state.cf_input_value3 = ""

#     st.session_state.cf_input_value3 = cf_input3

#     cf_value3 = st.session_state.cf_input_value3

#     if st.button("Esegui Ricerca"):
#         params = {
#             'CF': cf_value,
#             'Data_atto': cf_value1,
#             'Denominazione': cf_value2,
#             'COR': cf_value3
#         }



            
#     # Settore di attività
#     cf_input= st.text_input("Codice Fiscale : ",key=f"get_cf_{UUID}")

#     if 'cf_input_value' not in st.session_state:
#         st.session_state.cf_input_value = ""

#     st.session_state.cf_input_value = cf_input

#     cf_value = st.session_state.cf_input_value

#     # Tipo procedimento
#     cf_input= st.text_input("Codice Fiscale : ",key=f"get_cf_{UUID}")

#     if 'cf_input_value' not in st.session_state:
#         st.session_state.cf_input_value = ""

#     st.session_state.cf_input_value = cf_input

#     cf_value = st.session_state.cf_input_value



#  """
# Chiamata alla funzione main per avviare l'applicazione