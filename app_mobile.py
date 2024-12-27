import streamlit as st
import subprocess
import os

# Função para verificar e limpar alterações pendentes no repositório raiz
def reset_all_changes_in_root(project_root):
    st.info("Verificando alterações pendentes no repositório raiz...")
    status_result = subprocess.run("git status --porcelain", shell=True, cwd=project_root, capture_output=True, text=True)
    if status_result.stdout.strip():
        st.warning("Alterações não comitadas ou modificações encontradas no repositório raiz.")
        st.info("Removendo alterações não comitadas...")
        reset_result = subprocess.run("git reset --hard", shell=True, cwd=project_root, capture_output=True, text=True)
        if reset_result.returncode == 0:
            st.success("Alterações removidas com sucesso.")
        else:
            st.error(f"Erro ao remover alterações: {reset_result.stderr}")
            return False
    else:
        st.info("Nenhuma alteração pendente encontrada no repositório raiz.")
    return True

# Função para realizar um git pull na master antes de iniciar qualquer processo
def update_master_branch(project_root):
    st.info("Atualizando a branch master no projeto raiz...")
    os.chdir(project_root)
    subprocess.run("git checkout master", shell=True, cwd=project_root)
    subprocess.run("git pull", shell=True, cwd=project_root)
    st.success("Branch master atualizada com sucesso.")

# Função para verificar e criar/alternar para uma branch remota, se necessário
def checkout_and_update_branch(project_root, target_branch):
    os.chdir(project_root)  # Certifica-se de estar na raiz do repositório

    # Verifica se há alterações pendentes e as remove
    if not reset_all_changes_in_root(project_root):
        st.error("Não foi possível limpar as alterações pendentes. Processo encerrado.")
        return False

    # Verifica se a branch existe localmente
    result_local = subprocess.run(f"git branch --list {target_branch}", shell=True, cwd=project_root, capture_output=True, text=True)
    branch_exists_local = bool(result_local.stdout.strip())

    # Verifica se a branch existe remotamente
    result_remote = subprocess.run(f"git ls-remote --heads origin {target_branch}", shell=True, cwd=project_root, capture_output=True, text=True)
    branch_exists_remote = bool(result_remote.stdout.strip())

    # Logs para depuração
    st.info(f"Verificando branches: Local: {'Sim' if branch_exists_local else 'Não'}, Remoto: {'Sim' if branch_exists_remote else 'Não'}")

    # Cenário 1: A branch não existe localmente nem remotamente
    if not branch_exists_local and not branch_exists_remote:
        st.error(f"A branch '{target_branch}' não existe localmente nem remotamente. Processo encerrado.")
        return False

    # Cenário 2: A branch existe no remoto, mas não localmente
    if not branch_exists_local and branch_exists_remote:
        st.info(f"Branch '{target_branch}' encontrada no remoto. Criando branch local...")
        create_branch = subprocess.run(f"git checkout -b {target_branch} origin/{target_branch}", shell=True, cwd=project_root, capture_output=True, text=True)
        if create_branch.returncode != 0:
            st.error(f"Erro ao criar a branch local '{target_branch}' a partir de 'origin/{target_branch}': {create_branch.stderr}")
            return False
        st.success(f"Branch '{target_branch}' criada localmente com sucesso.")

    # Cenário 3: A branch já existe localmente
    if branch_exists_local:
        st.info(f"Fazendo checkout para a branch '{target_branch}'...")
        checkout = subprocess.run(f"git checkout {target_branch}", shell=True, cwd=project_root, capture_output=True, text=True)
        if checkout.returncode != 0:
            st.error(f"Erro ao fazer checkout na branch '{target_branch}': {checkout.stderr}")
            return False
        st.success(f"Checkout realizado com sucesso na branch '{target_branch}'.")

    # Sempre atualize a branch com 'git pull'
    st.info(f"Atualizando a branch '{target_branch}' com 'git pull'...")
    update_branch = subprocess.run("git pull", shell=True, cwd=project_root, capture_output=True, text=True)
    if update_branch.returncode != 0:
        st.error(f"Erro ao atualizar a branch '{target_branch}': {update_branch.stderr}")
        return False

    st.success(f"Branch '{target_branch}' pronta para uso e atualizada.")
    return True

# Função para executar comandos do Flutter em cada diretório
def run_flutter_commands(project_root, selected_directories):
    for dir_name in selected_directories:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path):
            st.info(f"Processando diretório: {dir_name}")
            os.chdir(dir_path)
            st.write(f"Executando 'flutter clean' em {dir_name}...")
            subprocess.run("flutter clean", shell=True)
            st.write(f"Executando 'flutter pub get' em {dir_name}...")
            subprocess.run("flutter pub get", shell=True)
            os.chdir(project_root)
        else:
            st.warning(f"Diretório '{dir_name}' não encontrado. Pulando...")

    models_dir = os.path.join(project_root, "models")
    if os.path.exists(models_dir):
        st.info("Executando build_runner no diretório 'models'...")
        os.chdir(models_dir)
        subprocess.run("flutter packages pub run build_runner build --delete-conflicting-outputs", shell=True)
        os.chdir(project_root)
    else:
        st.warning("Diretório 'models' não encontrado.")

# Interface do Streamlit
st.title("Gerenciamento de Branch e Atualização do Projeto Flutter")

# Campo para seleção do caminho do projeto
project_root = st.text_input("Insira o caminho para a pasta raiz do projeto")

if project_root and os.path.isdir(project_root):
    # Listar diretórios automaticamente após a seleção do projeto, ignorando pastas que começam com ponto (.)
    all_directories = [d for d in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, d)) and not d.startswith('.')]
    
    selected_directories = st.multiselect("Selecione os diretórios para atualização:", all_directories, default=all_directories)

    # Campo de entrada para o nome da branch de destino
    target_branch = st.text_input("Nome da branch de destino (repositório raiz)")

    if st.button("Iniciar Processo") and selected_directories:
        os.chdir(project_root)

        # Atualiza a branch master
        update_master_branch(project_root)

        # Atualiza a branch de destino, se fornecida
        if target_branch and checkout_and_update_branch(project_root, target_branch):
            run_flutter_commands(project_root, selected_directories)
            st.success("Processo concluído com sucesso.")
        else:
            st.error("Erro ao atualizar a branch. Processo interrompido.")
else:
    st.warning("Por favor, insira um caminho válido para o projeto.")
