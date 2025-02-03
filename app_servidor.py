import streamlit as st
import os
from pathlib import Path
import subprocess

# Configuração inicial
st.set_page_config(page_title="Gerenciador de Bootstrap JBoss", layout="centered")

# Função para verificar configurações
def verificar_configuracao():
    java_home = os.environ.get("JAVA_HOME", "")
    jboss_home = os.environ.get("JBOSS_HOME", "")

    erros = []
    if not java_home or not Path(java_home).exists():
        erros.append("O JAVA_HOME não está configurado ou aponta para um diretório inválido.")
    else:
        java_exe = Path(java_home) / "bin" / "java"
        if not java_exe.exists():
            erros.append(f"Executável Java não encontrado em {java_exe}.")
    
    if not jboss_home or not Path(jboss_home).exists():
        erros.append("O JBOSS_HOME não está configurado ou aponta para um diretório inválido.")
    else:
        jboss_jar = Path(jboss_home) / "jboss-modules.jar"
        if not jboss_jar.exists():
            erros.append(f"jboss-modules.jar não encontrado em {jboss_home}.")
    
    return erros

# Função para executar o JBoss
def executar_jboss(debug_mode, debug_port, server_opts):
    jboss_home = os.environ["JBOSS_HOME"]
    java_home = os.environ["JAVA_HOME"]
    java_exe = Path(java_home) / "bin" / "java"

    deployments_dir = Path(jboss_home) / "standalone" / "deployments"

    # Verificar se a pasta de deployments existe
    if not deployments_dir.exists():
        st.error(f"Diretório de deployments não encontrado: {deployments_dir}")
        return

    # Comando para executar o JBoss
    command = [
        str(java_exe),
        f"-Djboss.home.dir={jboss_home}",
        f"-Djboss.server.base.dir={jboss_home}/standalone",
        f"-Dorg.jboss.boot.log.file={jboss_home}/standalone/log/server.log",
        f"-Dlogging.configuration=file:{jboss_home}/standalone/configuration/logging.properties",
        "-jar",
        str(Path(jboss_home) / "jboss-modules.jar"),
        "-mp",
        f"{jboss_home}/modules",
        "org.jboss.as.standalone",
        f"-Djboss.socket.binding.port-offset=0",
        server_opts,
    ]

    if debug_mode:
        command.append(f"-agentlib:jdwp=transport=dt_socket,address={debug_port},server=y,suspend=n")

    st.write(f"Executando o comando: {' '.join(command)}")

    try:
        process = subprocess.run(command, text=True, capture_output=True, check=True)
        st.success("JBoss iniciado com sucesso!")
        st.text(process.stdout)
    except subprocess.CalledProcessError as e:
        st.error("Erro ao iniciar o JBoss:")
        st.text(e.stderr)

# Interface principal
st.title("Gerenciador de Bootstrap JBoss")

# Entrada de configuração
st.header("Configuração Inicial")
java_home = st.text_input("Caminho do JAVA_HOME", value=os.environ.get("JAVA_HOME", ""))
jboss_home = st.text_input("Caminho do JBOSS_HOME", value=os.environ.get("JBOSS_HOME", ""))

if st.button("Salvar Configuração"):
    if java_home and Path(java_home).exists():
        os.environ["JAVA_HOME"] = java_home
        st.success(f"JAVA_HOME configurado: {java_home}")
    else:
        st.error("Caminho inválido para JAVA_HOME.")

    if jboss_home and Path(jboss_home).exists():
        os.environ["JBOSS_HOME"] = jboss_home
        st.success(f"JBOSS_HOME configurado: {jboss_home}")
    else:
        st.error("Caminho inválido para JBOSS_HOME.")

# Verificar dependências
st.header("Verificar Configurações")
erros = verificar_configuracao()
if erros:
    for erro in erros:
        st.error(erro)
else:
    st.success("Configurações válidas. Pronto para iniciar o JBoss!")

# Opções de execução
st.header("Iniciar o JBoss")
debug_mode = st.checkbox("Ativar modo de depuração", value=False)
debug_port = st.number_input("Porta de depuração", min_value=1024, max_value=65535, value=8787)
server_opts = st.text_input("Opções do servidor", value="")

if st.button("Iniciar JBoss"):
    if erros:
        st.error("Corrija os erros antes de iniciar o JBoss.")
    else:
        executar_jboss(debug_mode, debug_port, server_opts)
