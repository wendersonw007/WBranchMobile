import os
import subprocess
import streamlit as st

# Caminho da pasta principal
base_path = r"C:\Sifat"
# Caminho da área de trabalho do usuário
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Função para listar as pastas que contêm waychef.jar
def listar_pastas_com_waychef(caminho):
    pastas = []
    for item in os.listdir(caminho):
        caminho_completo = os.path.join(caminho, item)
        if os.path.isdir(caminho_completo) and "waychef.jar" in os.listdir(caminho_completo):
            pastas.append(item)
    return pastas

# Verifica se o Java está instalado
def verificar_java():
    try:
        resultado = subprocess.run(["java", "-version"], capture_output=True, text=True, check=True)
        return True, resultado.stderr  # A versão do Java geralmente aparece no stderr
    except subprocess.CalledProcessError:
        return False, "Java não encontrado ou erro ao executá-lo."
    except FileNotFoundError:
        return False, "Java não está instalado no sistema."

# Função para executar o waychef.jar e salvar logs
def executar_waychef(caminho_pasta):
    caminho_jar = os.path.join(caminho_pasta, "waychef.jar")
    log_path = os.path.join(desktop_path, "waychef_log.txt")
    
    if not os.path.exists(caminho_jar):
        st.error(f"O arquivo {caminho_jar} não foi encontrado.")
        return
    
    try:
        os.chdir(caminho_pasta)
        with open(log_path, "w") as log_file:
            processo = subprocess.Popen(
                ["java", "-jar", "waychef.jar", "debug=True"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )

            st.success(f"Executando: {caminho_jar}")
            st.text("Logs de execução:")

            # Exibir e salvar logs em tempo real
            for linha in iter(processo.stdout.readline, ''):
                st.text(linha.strip())
                log_file.write(linha)
            
            processo.stdout.close()
            processo.wait()
            
            if processo.returncode != 0:
                erro = processo.stderr.read().strip()
                st.error(f"Erro ao executar {caminho_jar}: {erro}")
                log_file.write(f"Erro: {erro}\n")
        
        st.success(f"Log salvo em: {log_path}")
    except Exception as e:
        st.error(f"Erro ao executar {caminho_jar}: {e}")

# Função principal da aplicação
def main():
    st.title("Executador de Waychef.jar")

    # Verifica Java antes de continuar
    java_instalado, java_msg = verificar_java()
    if not java_instalado:
        st.error("Java não está instalado ou não foi encontrado no sistema.")
        st.text(java_msg)
        return

    st.success("Java está instalado e pronto para uso.")

    # Listar as pastas que contêm waychef.jar
    pastas = listar_pastas_com_waychef(base_path)
    if not pastas:
        st.warning("Nenhuma pasta com waychef.jar encontrada.")
        return

    st.write("Pastas disponíveis com waychef.jar:")
    pasta_selecionada = st.selectbox("Selecione uma pasta para executar:", pastas)

    # Botão para executar o waychef.jar
    if st.button("Executar waychef.jar"):
        caminho_pasta = os.path.join(base_path, pasta_selecionada)
        executar_waychef(caminho_pasta)

    # Botão para exportar o log
    log_path = os.path.join(desktop_path, "waychef_log.txt")
    if os.path.exists(log_path):
        with open(log_path, "r") as log_file:
            log_conteudo = log_file.read()
        st.download_button(label="Baixar Log", data=log_conteudo, file_name="waychef_log.txt", mime="text/plain")

# Executar a aplicação
if __name__ == "__main__":
    main()
