import subprocess
import os

# Caminho para o repositório raiz do projeto
project_root = "C:\DesenvolvimentoSifatFlutter\waybe-mobile-flutter"  # Substitua pelo caminho correto

# Branch para a qual deseja fazer o checkout
target_branch = "EA-422"  # Substitua pelo nome da branch desejada

# Lista de diretórios a serem processados
directories = [
    "waypag", "autopesagem", "core", "erp", "models", 
    "pos", "requester", "service", "utils", "waycard", 
    "waypag", "waychef"
]

# Função para verificar se a branch existe
def branch_exists(branch_name):
    result = subprocess.run(f"git branch --list {branch_name}", shell=True, capture_output=True, text=True)
    return bool(result.stdout.strip())

# Função para verificar o status do repositório Git e fazer o checkout
def checkout_and_update_branch_if_clean(target_branch):
    os.chdir(project_root)
    
    # Verifica se a branch de destino existe
    if not branch_exists(target_branch):
        print(f"Erro: A branch '{target_branch}' não existe. Encerrando o processo.")
        return False
    
    # Verifica se há alterações pendentes no repositório
    status_result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    
    if status_result.stdout.strip():
        # Se o resultado não estiver vazio, há mudanças pendentes
        print("Erro: Há alterações não comitadas na branch atual.")
        print("Commit ou stash as alterações antes de fazer o checkout para outra branch.")
        return False
    
    # Sem alterações pendentes, pode fazer o checkout e atualizar
    print(f"Fazendo checkout para a branch '{target_branch}'...")
    subprocess.run(f"git checkout {target_branch}", shell=True)
    print(f"Branch '{target_branch}' verificada. Atualizando com 'git pull'...")
    subprocess.run("git pull", shell=True)
    print(f"Branch '{target_branch}' está atualizada.")
    return True

# Função para executar comandos do Flutter em cada diretório
def run_flutter_commands():
    for dir_name in directories:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path):
            print(f"\nProcessando diretório: {dir_name}")
            os.chdir(dir_path)
            print(f"Executando 'flutter clean' em {dir_name}...")
            subprocess.run("flutter clean", shell=True)
            print(f"Executando 'flutter pub get' em {dir_name}...")
            subprocess.run("flutter pub get", shell=True)
            os.chdir(project_root)  # Retorna ao diretório raiz do projeto
        else:
            print(f"Diretório '{dir_name}' não encontrado. Pulando...")

    # Comando específico para o diretório "models" ao final
    models_dir = os.path.join(project_root, "models")
    if os.path.exists(models_dir):
        print("\nExecutando build_runner no diretório 'models'...")
        os.chdir(models_dir)
        subprocess.run("flutter packages pub run build_runner build --delete-conflicting-outputs", shell=True)
        os.chdir(project_root)
    else:
        print("Diretório 'models' não encontrado.")

# Executa o script principal
os.chdir(project_root)
if checkout_and_update_branch_if_clean(target_branch):
    run_flutter_commands()
else:
    print("O processo foi interrompido devido a problemas com a branch ou alterações pendentes.")
