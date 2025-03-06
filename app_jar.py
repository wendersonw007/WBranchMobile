import os
import subprocess
import streamlit as st

# Caminho da pasta principal
base_path = r"C:\Sifat"

# Função para listar as pastas que contêm waychef.jar
def listar_pastas_com_waychef(caminho):
    pastas = []
    for item in os.listdir(caminho):
        caminho_completo = os.path.join(caminho, item)
        if os.path.isdir(caminho_completo) and "waychef.jar" in os.listdir(caminho_completo):
            pastas.append(item)
    return pastas

# Função para executar o waychef.jar
def executar_waychef(caminho_pasta):
    caminho_jar = os.path.join(caminho_pasta, "waychef.jar")
    try:
        # Altera o diretório de trabalho para a pasta onde o waychef.jar está localizado
        os.chdir(caminho_pasta)
        # Executa o comando java -jar waychef.jar
        processo = subprocess.Popen(["java", "-jar", "waychef.jar", "debug=True"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = processo.communicate()
        
        if processo.returncode == 0:
            st.success(f"Executado com sucesso: {caminho_jar}")
            st.text("Saída do comando:")
            st.text(stdout.decode())
        else:
            st.error(f"Erro ao executar {caminho_jar}:")
            st.text(stderr.decode())
    except Exception as e:
        st.error(f"Erro ao executar {caminho_jar}: {e}")

# Função principal da aplicação
def main():
    st.title("Executador de Waychef.jar")

    # Listar as pastas que contêm waychef.jar
    pastas = listar_pastas_com_waychef(base_path)
    if not pastas:
        st.warning("Nenhuma pasta com waychef.jar encontrada.")
        return

    st.write("Pastas disponíveis com waychef.jar:")
    for pasta in pastas:
        st.write(f"- {pasta}")

    # Selecionar uma pasta
    pasta_selecionada = st.selectbox("Selecione uma pasta para executar:", pastas)

    # Botão para executar o waychef.jar
    if st.button("Executar waychef.jar"):
        caminho_pasta = os.path.join(base_path, pasta_selecionada)
        executar_waychef(caminho_pasta)

# Executar a aplicação
if __name__ == "__main__":
    main()