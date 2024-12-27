import streamlit as st
import pandas as pd

# Função para carregar os dados da planilha
def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    sheets_data = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
    return sheets_data

# Função para exibir dados paginados
def display_paginated_data(data, page_size):
    total_rows = len(data)
    page = st.number_input("Página", min_value=1, max_value=(total_rows // page_size) + 1, step=1)
    start_row = (page - 1) * page_size
    end_row = start_row + page_size
    st.write(data.iloc[start_row:end_row])

# Caminho do arquivo
file_path = r'C:\Users\DSV19\Downloads\Homolog.xlsx'

# Carregar dados
sheets_data = load_data(file_path)
sheet_names = list(sheets_data.keys())

# Interface Streamlit
st.title("Visualizador de Planilhas - Paginação")
selected_sheet = st.selectbox("Selecione uma aba", sheet_names)

if selected_sheet:
    st.subheader(f"Aba: {selected_sheet}")
    data = sheets_data[selected_sheet]
    page_size = st.slider("Tamanho da página", 5, 50, 10)
    display_paginated_data(data, page_size)
