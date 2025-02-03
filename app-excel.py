import pandas as pd
import streamlit as st

# Caminho do arquivo Excel
excel_file = r"C:\Users\DSV19\Documents\qa\Homolog.xlsx"

# Carregar os dados do Excel
@st.cache_data
def load_data(sheet_name):
    return pd.read_excel(excel_file, sheet_name=sheet_name, engine="openpyxl")

# Salvar os dados no Excel
def save_data(df, sheet_name):
    with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# Interface do Streamlit
st.title("Gerenciamento de Dados no Excel")
excel_data = pd.ExcelFile(excel_file)
sheets = excel_data.sheet_names

# Seleção da aba
sheet_name = st.sidebar.selectbox("Selecione a aba", sheets)
df = load_data(sheet_name)

# Exibir os dados
st.subheader(f"Aba: {sheet_name}")
st.dataframe(df)

# Operações de edição
st.sidebar.subheader("Operações")
operation = st.sidebar.radio("Escolha uma operação", ["Adicionar", "Editar", "Deletar"])

if operation == "Adicionar":
    st.sidebar.subheader("Adicionar Linha")
    new_data = {}
    for col in df.columns:
        new_data[col] = st.sidebar.text_input(f"Novo valor para {col}")
    if st.sidebar.button("Adicionar Linha"):
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df, sheet_name)
        st.success("Linha adicionada com sucesso!")
        st.experimental_rerun()

elif operation == "Editar":
    st.sidebar.subheader("Editar Linha")
    row_to_edit = st.sidebar.number_input("Índice da linha para editar", min_value=0, max_value=len(df) - 1, step=1)
    if st.sidebar.button("Carregar Linha"):
        row_data = df.loc[row_to_edit].to_dict()
        updated_data = {}
        for col in df.columns:
            updated_data[col] = st.sidebar.text_input(f"Novo valor para {col}", value=row_data[col])
        if st.sidebar.button("Atualizar Linha"):
            for col, val in updated_data.items():
                df.at[row_to_edit, col] = val
            save_data(df, sheet_name)
            st.success("Linha atualizada com sucesso!")
            st.experimental_rerun()

elif operation == "Deletar":
    st.sidebar.subheader("Deletar Linha")
    row_to_delete = st.sidebar.number_input("Índice da linha para deletar", min_value=0, max_value=len(df) - 1, step=1)
    if st.sidebar.button("Deletar Linha"):
        df = df.drop(index=row_to_delete).reset_index(drop=True)
        save_data(df, sheet_name)
        st.success("Linha deletada com sucesso!")
        st.experimental_rerun()
