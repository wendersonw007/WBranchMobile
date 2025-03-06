import streamlit as st
import pandas as pd

# Definir o tema escuro diretamente no código
st.set_page_config(page_title="Dashboard de Aprovações", page_icon="📊", initial_sidebar_state="expanded")




# Carregar o arquivo Excel local
file_path = r"C:\Users\DSV19\Downloads\Homolog.xlsx"

# Função para carregar dados de uma aba específica
@st.cache_data
def load_sheet(sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1)  # Ignorar a primeira linha
    return df

# Carregar os nomes das abas da planilha
with pd.ExcelFile(file_path) as xls:
    sheet_names = xls.sheet_names

# Interface do Streamlit
st.markdown("<h1 style='text-align: center; color: write;'>LISTAGEM APROVAÇÕES PARA HOMOLOG</h1>", unsafe_allow_html=True)

# Seleção da aba para exibir
selected_sheet = st.selectbox("Selecione uma aba:", sheet_names)

# Carregar e exibir os dados da aba selecionada
df = load_sheet(selected_sheet)
st.write(f"Dados da aba: {selected_sheet}")
st.dataframe(df)

# Exemplo de gráfico por projeto
if not df.empty:
    st.write("Visualização de dados por projeto:")
    
    # Verificar se a coluna 'PROJETO AFETADO' existe
    if 'PROJETO AFETADO' in df.columns:
        # Agrupar os dados pela coluna 'PROJETO AFETADO' e contar as ocorrências
        project_counts = df['PROJETO AFETADO'].value_counts()
        
        # Exibir gráfico de barras com a contagem de tarefas por projeto
        st.bar_chart(project_counts)
    else:
        st.error("Não foi encontrada a coluna 'PROJETO AFETADO' para agrupar os dados.")

