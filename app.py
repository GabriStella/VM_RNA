import streamlit as st
from interrogazioni import *
import uuid
from datetime import date, timedelta
from streamlit.logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info('Hello world')
    if 'cliente' not in st.session_state:
        UUID=str(uuid.uuid4())
        st.session_state.cliente = UUID
    UUID = st.session_state.cliente

    # st.write(f"UUID = {UUID}")

    # st.session_state.cliente.Variabile= "prova prova"
    # Varriabile=st.session_state.cliente.Variabile
    # st.write(f"UUID = {Varriabile}")
    # st.write(f"UUID = {st.session_state}")
    st.title("Compila DeMinimis")

    #?DA QUA IN POI DA INSERIRE NELLA RICERCA SEMPLICE 
    
    # CF #? cf GIà FUNGE
    cf_input= st.text_input("Codice Fiscale : ",key=f"get_cf_{UUID}")
    CFS={}
    if 'cf_input_value' not in st.session_state:
        

        st.session_state.cf_input_value = ""

    CFS["CF_1"]=cf_input

    cf_value = st.session_state.cf_input_value
    Collegate=st.text_input("Quante sono le imprese collegate? ",value=0)
    # st.event("No collegamenti tramite persone fisiche tranne imprese individuali e lavoratori autonomi che svolgono attività economica. \n \n Solo imprese con sede in Italia")
#     st.markdown(
#     """
#     <style>
#     .instructions {
#         background-color: #f0f0f5;
#         border-left: 6px solid #0073e6;
#         padding: 10px;
#         margin: 10px 0;
#         font-family: Arial, sans-serif;
#     }
#     </style>
#     <div class="instructions">
#         <h4>Ricorda:</h4>
#         <ul>
#             <li>1: Non vanno inseriti i collegamenti tramite persona fisica;</li>
#             <ul>
#                 <li>1.1: <strong>Eccezione</strong>: imprese individuali e lavoratori autonomi che svolgono attività economica;</li>
#             </ul>    
#             <li>2: Inserire solo imprese con sede in Italia.</li>
#         </ul>
#     </div>
#     """,
#     unsafe_allow_html=True
# )



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
            st.dataframe(CF_Result, use_container_width=True)
            GENERALE = pd.DataFrame(columns=CF_Result.columns)
            AGRICOLTURA = pd.DataFrame(columns=CF_Result.columns)
            PESCA = pd.DataFrame(columns=CF_Result.columns)
            den_value = CF_Result.loc[CF_Result['C.F. Beneficiario'] == CFS["CF_1"], 'Denominazione Beneficiario'].iloc[0]
            st.write(den_value)
            for index, row in CF_Result.iterrows():
                if "2831" in row["Regolamento/Comunicazione"] :#or "1407" in row["Regolamento/Comunicazione"]:     
                    GENERALE= pd.concat([GENERALE, pd.DataFrame([row])], ignore_index=True)
                elif "1407" in row["Regolamento/Comunicazione"]:
                    GENERALE= pd.concat([GENERALE, pd.DataFrame([row])], ignore_index=True)
                elif "1408" in row["Regolamento/Comunicazione"]:
                    AGRICOLTURA= pd.concat([AGRICOLTURA, pd.DataFrame([row])], ignore_index=True)
                elif "717"  in row["Regolamento/Comunicazione"]: 
                    PESCA= pd.concat([PESCA, pd.DataFrame([row])], ignore_index=True)



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

    # except Exception as e:
    #     st.error(f"Inserire nel Box il numero delle collegate, grazie. {e}")

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