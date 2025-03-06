import streamlit as st
import subprocess
import os

# Função para verificar se a branch existe
def branch_exists(branch_name, project_root):
    result = subprocess.run(f"git branch --list {branch_name}", shell=True, cwd=project_root, capture_output=True, text=True)
    return bool(result.stdout.strip())

# Função para verificar o status do repositório Git e remover alterações não comitadas e modificadas
def reset_all_changes(project_root, selected_directories):
    changes_found = False  # Variável para controlar se alterações foram encontradas
    for project in selected_directories:
        project_dir = os.path.join(project_root, project)
        os.chdir(project_dir)

        # Verifica se há alterações não comitadas ou modificações nos arquivos
        status_result = subprocess.run("git status --porcelain", shell=True, cwd=project_dir, capture_output=True, text=True)

        if status_result.stdout.strip():  # Se houver alterações não comitadas ou modificações
            st.warning(f"Há alterações não comitadas ou modificações no projeto '{project}'.")
            changes_found = True
            st.info(f"Removendo alterações no projeto '{project}'...")

            # Comando para resetar as alterações
            subprocess.run("git reset --hard", shell=True, cwd=project_dir)  # Remove todas as alterações
            st.success(f"As alterações foram removidas no projeto '{project}'.")
        else:
            st.info(f"Não há alterações não comitadas ou modificações no projeto '{project}'. Continuando...")

    return changes_found

# Função para verificar e atualizar a branch
def checkout_and_update_branch(project_root, target_branch, selected_project):
    project_dir = os.path.join(project_root, selected_project)
    os.chdir(project_dir)

    # Verifica se a branch de destino existe
    if not branch_exists(target_branch, project_dir):
        st.error(f"A branch '{target_branch}' não existe no projeto '{selected_project}'. Encerrando o processo.")
        return False
    
    # Faz o checkout da branch e atualiza com 'git pull'
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

    # Variável para controlar o estado de execução
    if 'process_in_progress' not in st.session_state:
        st.session_state.process_in_progress = False
        st.session_state.changes_removed = False

    # Botão para iniciar o processo
    if st.button("Iniciar Processo") and selected_directories:
        if selected_project and target_branch:  # Verifica se o nome da branch e o projeto foram fornecidos
            os.chdir(project_root)
            
            # Limpa as alterações não comitadas e modificações em todos os projetos selecionados
            if not st.session_state.changes_removed:
                changes_found = reset_all_changes(project_root, selected_directories)
                
                if changes_found:  # Se alterações foram encontradas e removidas, reinicia o processo
                    st.session_state.process_in_progress = False  # Impede a continuação do processo até o usuário confirmar
                    st.session_state.changes_removed = True  # Marca que as alterações foram removidas
                    st.button("Deseja iniciar o processo novamente?", key="restart")  # Espera a interação do usuário
                    st.stop()  # Interrompe o fluxo até o usuário confirmar

                # Atualiza o projeto específico com a nova branch
                if not changes_found:
                    if checkout_and_update_branch(project_root, target_branch, selected_project):
                        # Atualiza os outros diretórios sem fazer o checkout de branch
                        remaining_directories = [d for d in selected_directories if d != selected_project]
                        run_flutter_commands(project_root, remaining_directories)
                        st.success("Processo concluído com sucesso.")
                    else:
                        st.error(f"O processo foi interrompido devido a problemas com a branch ou alterações pendentes no projeto '{selected_project}'.")
            else:
                st.session_state.process_in_progress = True  # Marca o processo como em andamento
                # Atualiza o projeto específico com a nova branch
                if checkout_and_update_branch(project_root, target_branch, selected_project):
                    # Atualiza os outros diretórios sem fazer o checkout de branch
                    remaining_directories = [d for d in selected_directories if d != selected_project]
                    run_flutter_commands(project_root, remaining_directories)
                    st.success("Processo concluído com sucesso.")

    # Botão para reiniciar o processo
    if st.session_state.changes_removed and not st.session_state.process_in_progress:
        if st.button("Iniciar o processo novamente"):
            st.session_state.process_in_progress = False
            st.session_state.changes_removed = False
            st.experimental_rerun()  # Reinicia o fluxo de execução do Streamlit

else:
    st.warning("Por favor, insira um caminho válido para o projeto.")
