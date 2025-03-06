
# Gerenciamento de Branch e Atualização do Projeto Flutter

Este projeto facilita o gerenciamento de branches e a atualização de dependências em projetos Flutter, automatizando processos repetitivos e aumentando a produtividade ao gerenciar múltiplos diretórios dentro de uma aplicação. A interface é amigável e foi desenvolvida em Python com o framework **Streamlit**, que possibilita uma experiência visual simples e interativa, tornando o fluxo de trabalho mais eficiente.

## Funcionalidades Principais

- **Verificação de Alterações**: Examina se há alterações não comitadas em todos os diretórios especificados, garantindo que o usuário tenha controle total antes de executar ações de atualização de branches ou dependências.
- **Atualização de Branches Git**: Realiza checkout em uma branch específica e a atualiza, caso necessário. Se a branch não existir, o usuário é notificado, evitando erros.
- **Automação de Comandos Flutter**: Executa comandos como `flutter clean` e `flutter pub get` em múltiplos diretórios, agilizando a preparação de builds e garantindo que todas as dependências estejam atualizadas.
- **Confirmação Interativa**: Oferece opções de confirmação antes de limpar alterações não comitadas, proporcionando controle adicional ao usuário durante o processo.

## Tecnologias Utilizadas

- **Python**: Linguagem principal para implementar a lógica de verificação de Git e execução de comandos.
- **Streamlit**: Framework de interface gráfica que possibilita uma experiência interativa, permitindo que usuários escolham diretórios e configurem o processo de atualização com botões e seleções visuais.
- **Git**: Utilizado para gerenciamento de branches e verificação de alterações em cada diretório do projeto.

## Como Usar

1. **Configuração Inicial**: Instale as dependências necessárias, incluindo Streamlit.
    
    bash
    
    Copiar código
    
    `pip install streamlit`
    
2. **Execução do Projeto**: Para iniciar a aplicação, navegue até o diretório do projeto e execute o comando:
    
    bash
    
    Copiar código
    
    `streamlit run app.py`
    
3. **Seleção e Execução**:
    
    - Insira o caminho para o diretório raiz do seu projeto Flutter.
    - Escolha os diretórios que deseja incluir no processo.
    - Escolha o projeto onde será feita a atualização da branch, bem como o nome da branch de destino.
    - Siga as instruções na interface para limpar alterações ou iniciar o processo de atualização.

## Propósito e Aplicação

Este projeto foi desenvolvido como uma ferramenta de portfólio, demonstrando habilidades em **Python**, **Streamlit** e **automação de fluxo de trabalho** com Git e Flutter. É especialmente útil para engenheiros de dados e recrutadores que buscam profissionais com experiência prática na criação de ferramentas de automação, gestão de versões e trabalho com múltiplos serviços integrados.

## Estrutura do Projeto

- **app.py**: Script principal que contém a lógica da aplicação e a interface Streamlit.
- **funções auxiliares**: Funções para verificação de branches, atualização de dependências e reset de alterações.
- **README.md**: Documentação do projeto.

## Possíveis Melhorias

- **Autenticação Git Integrada**: Possibilidade de integrar autenticação automática para repositórios privados.
- **Feedback em Tempo Real**: Adição de logs em tempo real para melhor acompanhamento do progresso das ações.
- **Suporte para Outras Plataformas**: Possibilidade de integração com sistemas como Bitbucket e GitLab.
