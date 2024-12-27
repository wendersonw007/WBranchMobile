import streamlit as st
import subprocess
import os

# Função para executar comandos no terminal
def execute_command(command):
    """Execute a shell command and return its output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr

st.title("Gerenciamento de Branch e Compilação de Projeto")

# Seleção do diretório onde estão os projetos
st.subheader("Seleção do Diretório dos Projetos")
if 'project_directory' not in st.session_state:
    st.session_state['project_directory'] = ""

project_directory = st.text_input(
    "Informe o caminho do diretório dos projetos:",
    st.session_state['project_directory']
)

if st.button("Confirmar Diretório"):
    if os.path.isdir(project_directory):
        st.session_state['project_directory'] = project_directory
        st.success(f"Diretório selecionado: {project_directory}")
    else:
        st.error("O caminho informado não é um diretório válido. Por favor, tente novamente.")

if 'project_directory' in st.session_state and st.session_state['project_directory']:
    st.write(f"Diretório atual dos projetos: {st.session_state['project_directory']}")
else:
    st.warning("Por favor, informe e confirme o diretório dos projetos.")

# Gerenciamento de branch
st.subheader("Gerenciamento de Branch")
if 'project_directory' in st.session_state and st.session_state['project_directory']:
    os.chdir(st.session_state['project_directory'])
    git_branches, git_error = execute_command("git branch")
    if git_error:
        st.error(f"Erro ao listar branches: {git_error}")
    else:
        st.write("Branches disponíveis:")
        st.text(git_branches)

    branch = st.text_input("Informe a branch para checkout:")
    if st.button("Realizar Checkout"):
        if branch:
            # Verificar a branch ativa
            current_branch, current_branch_error = execute_command("git rev-parse --abbrev-ref HEAD")
            if current_branch_error:
                st.error(f"Erro ao verificar branch atual: {current_branch_error}")
            else:
                current_branch = current_branch.strip()
                if current_branch == branch:
                    st.info(f"Já está na branch '{branch}'. Executando git pull...")
                    pull_cmd = "git pull"
                    stdout_pull, stderr_pull = execute_command(pull_cmd)
                    if stderr_pull:
                        st.error(f"Erro no pull: {stderr_pull}")
                    else:
                        st.write("Saída do Pull:")
                        st.text(stdout_pull)
                else:
                    checkout_cmd = f"git checkout {branch} && git pull"
                    stdout, stderr = execute_command(checkout_cmd)
                    if stderr:
                        st.error(f"Erro no checkout ou pull: {stderr}")
                    else:
                        st.write("Saída do comando:")
                        st.text(stdout)
        else:
            st.warning("Por favor, informe uma branch válida.")
else:
    st.warning("Selecione o diretório dos projetos para continuar.")

# Menu de compilação
st.subheader("Menu de Compilação")
compilation_option = st.selectbox(
    "Escolha uma opção:",
    ["Compile ALL", "Compile ERP", "Compile API", "Compile WAYCHEF"]
)

branch_origin = st.radio(
    "Qual foi a branch de origem?",
    ["working", "rc", "master"]
)

if st.button("Iniciar Merge e Push"):
    if 'project_directory' in st.session_state and st.session_state['project_directory']:
        # Verificar alterações locais antes do merge
        changes_cmd = "git status --porcelain"
        stdout_changes, stderr_changes = execute_command(changes_cmd)
        if stdout_changes:
            st.warning("Existem alterações locais não commitadas. Salvando alterações temporariamente (stash)...")
            stash_cmd = "git stash"
            stdout_stash, stderr_stash = execute_command(stash_cmd)
            if stderr_stash:
                st.error(f"Erro ao executar stash: {stderr_stash}")
            else:
                st.write("Alterações locais salvas temporariamente:")
                st.text(stdout_stash)

        merge_cmd = f"git merge origin/{branch_origin}"
        push_cmd = f"git push origin {branch}"
        stdout_merge, stderr_merge = execute_command(merge_cmd)
        stdout_push, stderr_push = execute_command(push_cmd)

        if stderr_merge:
            st.error(f"Erro no merge: {stderr_merge}")
        else:
            st.write("Saída do Merge:")
            st.text(stdout_merge)

        if stderr_push:
            st.error(f"Erro no push: {stderr_push}")
        else:
            st.write("Saída do Push:")
            st.text(stdout_push)

        # Restaurar alterações do stash, se necessário
        if stdout_changes:
            st.info("Restaurando alterações locais (stash apply)...")
            apply_stash_cmd = "git stash apply"
            stdout_apply, stderr_apply = execute_command(apply_stash_cmd)
            if stderr_apply:
                st.error(f"Erro ao restaurar stash: {stderr_apply}")
            else:
                st.write("Alterações locais restauradas:")
                st.text(stdout_apply)
    else:
        st.warning("Selecione o diretório dos projetos para continuar.")

# Escolha do banco
st.subheader("Configuração do Banco")
database = st.selectbox(
    "Escolha o banco:",
    ["Waybe-working", "Waybe-RC", "Waybe-master", "Waybe-email"]
)

# Origem do banco
origin = st.radio(
    "Origem do banco:",
    ["MeuBanco", "Outro", "Dev"]
)

if st.button("Configurar Banco e Compilar"):
    if 'project_directory' in st.session_state and st.session_state['project_directory']:
        db_config = {
            "MeuBanco": {"porta": "3308", "senha": "generator", "usuario": "generator", "ip": "127.0.0.1"},
            "Outro": {"porta": "3308", "senha": "generator", "usuario": "generator", "ip": "192.168.5.20"},
            "Dev": {"porta": "3306", "senha": "generator", "usuario": "generator", "ip": "192.168.5.237"},
        }

        banco_config = db_config[origin]
        st.write("Configuração do banco:")
        st.json(banco_config)

        compile_scripts = {
            "Compile ALL": "Bats/CompileALL/CompileWaybe",
            "Compile ERP": "Bats/CompileERP/CompileWaybe",
            "Compile API": "Bats/CompileAPI/CompileWaybe",
            "Compile WAYCHEF": "Bats/CompileWaychef/CompileWaybe",
        }

        compile_script = compile_scripts[compilation_option]
        compile_cmd = f"{compile_script}.bat {banco_config['porta']} {banco_config['senha']} {banco_config['usuario']} {banco_config['ip']} {database}"

        stdout_compile, stderr_compile = execute_command(compile_cmd)
        if stderr_compile:
            st.error(f"Erro na compilação: {stderr_compile}")
        else:
            st.write("Saída da Compilação:")
            st.text(stdout_compile)
    else:
        st.warning("Selecione o diretório dos projetos para continuar.")
