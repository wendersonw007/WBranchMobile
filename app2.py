import streamlit as st
import subprocess
import os

# Função para verificar se a branch existe
def branch_exists(branch_name, project_root):
    result = subprocess.run(f"git branch --list {branch_name}", shell=True, cwd=project_root, capture_output=True, text=True)
    return bool(result.stdout.strip())

# Função para verificar o status do repositório Git e fazer o checkout
def checkout_and_update_branch_if_clean(project_root, target_branch, selected_project):
    project_dir = os.path.join(project_root, selected_project)
    os.chdir(project_dir)

    # Verifica se a branch de destino existe
    if not branch_exists(target_branch, project_dir):
        st.error(f"A branch '{target_branch}' não existe no projeto '{selected_project}'. Encerrando o processo.")
        return False
    
    # Verifica se há alterações pendentes no repositório
    status_result = subprocess.run("git status --porcelain", shell=True, cwd=project_dir, capture_output=True, text=True)
    
    if status_result.stdout.strip():
        st.warning(f"Há alterações não comitadas no projeto '{selected_project}'.")
        
        # Opção para remover alterações não comitadas
        if st.button(f"Remover alterações não comitadas no projeto '{selected_project}' e continuar"):
            st.info(f"Removendo alterações não comitadas no projeto '{selected_project}'...")
            subprocess.run("git reset --hard", shell=True, cwd=project_dir)  # Remove alterações não comitadas
            st.success(f"As alterações não comitadas no projeto '{selected_project}' foram removidas.")
            return True  # Após remover as alterações, podemos continuar o processo

        # Se o usuário não quiser remover as alterações, o processo é interrompido
        st.error(f"As alterações não comitadas precisam ser removidas ou comitadas antes de mudar de branch.")
        return False
    
    # Se não houver alterações, faz o checkout da branch e atualiza
    st.info(f"Fazendo checkout para a branch '{target_branch}' no projeto '{selected_project}'...")
    subprocess.run(f"git checkout {target_branch}", shell=True, cwd=project_dir)
    st.info(f"Branch '{target_branch}' verificada. Atualizando com 'git pull' no projeto '{selected_project}'...")
    subprocess.run("git pull", shell=True, cwd=project_dir)
    st.success(f"Branch '{target_branch}' do projeto '{selected_project}' está atualizada.")
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
project_root = st.text_input("Insira o caminho para a pasta do projeto")

if project_root and os.path.isdir(project_root):
    # Listar diretórios automaticamente após a seleção do projeto, ignorando pastas que começam com ponto (.)
    all_directories = [d for d in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, d)) and not d.startswith('.')]
    
    # Exibir checkboxes para os diretórios encontrados
    selected_directories = st.multiselect("Selecione os diretórios para atualização:", all_directories, default=all_directories)

    # Campo de entrada para o nome da branch de destino (apenas para um projeto específico)
    target_branch = st.text_input("Nome da branch de destino (apenas para o projeto selecionado)")

    # Dropdown para selecionar o projeto específico que terá a branch atualizada
    selected_project = st.selectbox("Selecione o projeto para atualizar a branch", selected_directories)

    # Botão para iniciar o processo
    if st.button("Iniciar Processo") and selected_directories:
        if target_branch and selected_project:  # Verifica se o nome da branch e o projeto foram fornecidos
            os.chdir(project_root)
            if checkout_and_update_branch_if_clean(project_root, target_branch, selected_project):
                # Atualiza os outros diretórios sem fazer o checkout de branch
                remaining_directories = [d for d in selected_directories if d != selected_project]
                run_flutter_commands(project_root, remaining_directories)
                st.success("Processo concluído com sucesso.")
            else:
                st.error(f"O processo foi interrompido devido a problemas com a branch ou alterações pendentes no projeto '{selected_project}'.")
        else:
            # Se não houver branch, apenas faz a atualização dos diretórios selecionados
            run_flutter_commands(project_root, selected_directories)
            st.success("Processo concluído com sucesso.")

else:
    st.warning("Por favor, insira um caminho válido para o projeto.")
