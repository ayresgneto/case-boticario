## Case técnico para grupo Oboticário

### Objetivo

1. Desenvolvimento de um modelo de previsões sobre os preços de imóveis a partir de suas características.
2. Implementação do modelo atavés de um pipeline de treinamento automatizado e disponibilização por web service (API)

### Playbook

Este case foi desenvolvido com ferramentas open source e localmente. Portanto é necessário a instalação local dessas
ferramentas para executá-lo. Segue abaixo os passos necessários para ambiente linux:

1. Instalação Airflow localmente:<br>
    No terminal digite:<br>
        <i>pip install apache-airflow</i><br>
    Após a instalação, executar em 2 janelas do terminal:<br>
        <i>airflow webserver --port 8080</i><br>
        <i>airflow scheduler</i><br>
    Obs: essas janelas devem ficar em execução

2. Instalação Docker Desktop<br>
    No terminal digite:<br>
        Para ubuntu: <i>sudo apt-get install ./docker-desktop-amd64.deb</i><br>
        Caso use outro sistema operacional, obtenha mais informações aqui: [aqui](https://www.docker.com/products/docker-desktop/)<br>
    Obs: O Docker desktop deve estar em execução

3. Crie um ambiente virtual e ative-o:<br>
    No terminal digite:<br>
        <i>python -m venv nome_do_ambiente</i><br>
        ou, caso esteja usando python3<br>
        <i>python3 -m venv nome_do_ambiente</i><br>
        Ative-o usando o seguinte comando:<br>
        <i>source nome_do_ambiente/bin/activate</i><br>

4. Instale as dependências:<br>
    No terminal digite:<br>
        <i>pip install -r requirements.txt</i>

5. Configurando o airflow:<br>
    5.1 criando um novo usuario admin:<br>
        No terminal digite:<br>
            airflow users create \
            --username admin \
            --firstname Peter \
            --lastname Parker \
            --role Admin \
            --email spiderman@superhero.org<br>
        obs: coloque seus dados
    5.2 Acessando airflow:<br>
        No navegador digite:<br>
        <i>http://localhost:8080/</i><br>
        Faça o login com o usuario criado
    
    5.3 Configurando as dags e plugins<br>
        Adicione as dags do projeto dentro do diretório dags onde o airflow foi instalado<br> 
        e o diretório plugins na raíz da instalação<br>
    Obs: caso nao exista os diretórios, crie-os

### Estrutura de diretórios

```
└── 📁case-boticario
    └── 📁app
        └── main.py
        └── modelo.py
    └── 📁artefatos
        └── 📁metadados
            └── metadados_v1.json
            └── metadados_v2.json
            └── metadados_v3.json
            └── metadados_v4.json
            └── metadados_v5.json
            └── metadados_v6.json
            └── metadados_v7.json
            └── metadados_v8.json
            └── metadados_v9.json
        └── 📁modelo
            └── modelo_v1.pkl
            └── modelo_v2.pkl
            └── modelo_v3.pkl
            └── modelo_v4.pkl
            └── modelo_v5.pkl
            └── modelo_v6.pkl
            └── modelo_v7.pkl
            └── modelo_v8.pkl
            └── modelo_v9.pkl
        └── 📁scaler
            └── scaler_v1.pkl
            └── scaler_v2.pkl
            └── scaler_v3.pkl
            └── scaler_v4.pkl
            └── scaler_v5.pkl
            └── scaler_v6.pkl
            └── scaler_v7.pkl
            └── scaler_v8.pkl
            └── scaler_v9.pkl
    └── 📁dados
        └── 📁processed
            └── HousePrices_HalfMil_processed.csv
        └── 📁raw
            └── HousePrices_HalfMil.csv
    └── 📁dags
        └── build_deploy_infra.py
        └── extrai_trata_dados.py
        └── treina_salva_modelo.py
    └── Docs
        └── arquitetura_case_boticario.png
    └── 📁notebooks
        └── model.ipynb
    └── 📁plugins
        └── __init__.py
        └── 📁__pycache__
            └── __init__.cpython-311.pyc
            └── utils.cpython-311.pyc
        └── utils.py
    └── .gitignore
    └── cliente.py
    └── docker-compose.yml
    └── Dockerfile
    └── README.md
    └── requirements.txt
```
### explicar os arquivos e diretorios

### Arquitetura

![Logo do Projeto](docs/arquitetura_case_boticario.png)





