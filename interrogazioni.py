import pyodbc
import pandas as pd
from openpyxl import load_workbook
import tempfile
import os
import mysql.connector




def Ask_CF(CFS):
    config = {
        'user': 'root',
        'host': 'localhost',
        'database': 'RNAuser'
    }

    # Costruzione della query
    base_query = "SELECT * FROM `rna` WHERE 1=1"
    query_params = []
    
    if len(CFS) == 1:
        base_query += " AND `C.F. Beneficiario` = %s"
        query_params.append(CFS['CF_1'])
    elif len(CFS) > 1:
        placeholders = ', '.join(['%s'] * len(CFS))
        base_query += f" AND `C.F. Beneficiario` IN ({placeholders})"
        for key in CFS:
            query_params.append(CFS[key])
    else:
        return None

    # Connessione al database e esecuzione della query
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    try:
        cursor.execute(base_query, query_params)
        rows = cursor.fetchall()

        # Ottenere i nomi delle colonne
        columns = [column[0] for column in cursor.description]

        # Creare un DataFrame Pandas
        df = pd.DataFrame.from_records(rows, columns=columns)
    finally:
        # Chiudere il cursore e la connessione
        cursor.close()
        conn.close()

    return df



def CREA_DF(AMBITO):
    
    if not AMBITO.empty: 
        selected_columns = AMBITO#.iloc[:, [2, 3, 4, 8, 10]]
        new_df = pd.DataFrame({
            'DEN' : selected_columns.iloc[:, 10],
            'CFB' : selected_columns.iloc[:, 11],
            'DATA' : selected_columns.iloc[:, 7],
            'autorita' : selected_columns.iloc[:, 14],
            'Tit_misura' : selected_columns.iloc[:, 2],       
            'Norma_misura' : selected_columns.iloc[:, 3],
            'AIUTO' : selected_columns.iloc[:, 23]
        })
        return new_df

def COMPILA_EXCEL_agr(ambito):

    excel_template = "C:\\Users\\g.stella\\Desktop\\CIAO\\DE MINIMIS 1408 - AGRICOLTURA.xlsx"
    wb = load_workbook(excel_template)
    ws = wb.active

    mapping = {
    'C': 'DEN',
    'D': 'CFB',
    'E': 'DATA',
    'G': 'autorita',
    'H': 'Tit_misura',
    'I': 'Norma_misura',
    'J': 'AIUTO'
    }

    start_row = 6
    for index, row in ambito.iterrows():
        for excel_col, df_col in mapping.items():
            ws[f'{excel_col}{start_row + index}'] = row[df_col]

    with tempfile.TemporaryDirectory() as tmpdirname:
        doc_path = os.path.join(tmpdirname, "TENTATIVO.xlsx")
        wb.save(doc_path)
        with open(doc_path, "rb") as f:
            doc_contents = f.read()
        return doc_contents


def COMPILA_EXCEL_pes(ambito):

    excel_template = "C:\\Users\\g.stella\\Desktop\\CIAO\\DE MINIMIS 717 - PESCA E ACQUACOLTURA.xlsx"
    wb = load_workbook(excel_template)
    ws = wb.active

    mapping = {
    'C': 'DEN',
    'D': 'CFB',
    'E': 'DATA',
    'G': 'autorita',
    'H': 'Tit_misura',
    'I': 'Norma_misura',
    'J': 'AIUTO'
    }

    start_row = 6
    for index, row in ambito.iterrows():
        for excel_col, df_col in mapping.items():
            ws[f'{excel_col}{start_row + index}'] = row[df_col]

    with tempfile.TemporaryDirectory() as tmpdirname:
        doc_path = os.path.join(tmpdirname, "TENTATIVO.xlsx")
        wb.save(doc_path)
        with open(doc_path, "rb") as f:
            doc_contents = f.read()
        return doc_contents

def COMPILA_EXCEL_gen(ambito):

    excel_template = "C:\\Users\\g.stella\\Desktop\\CIAO\\DE MINIMIS 2831 - GENERALE.xlsx"
    wb = load_workbook(excel_template)
    ws = wb.active

    mapping = {
    'C': 'DEN',
    'D': 'CFB',
    'E': 'DATA',
    'H': 'autorita',
    'I': 'Tit_misura',
    'J': 'Norma_misura',
    'K': 'AIUTO'
    }

    start_row = 6
    for index, row in ambito.iterrows():
        for excel_col, df_col in mapping.items():
            ws[f'{excel_col}{start_row + index}'] = row[df_col]

    with tempfile.TemporaryDirectory() as tmpdirname:
        doc_path = os.path.join(tmpdirname, "TENTATIVO.xlsx")
        wb.save(doc_path)
        with open(doc_path, "rb") as f:
            doc_contents = f.read()
        return doc_contents
