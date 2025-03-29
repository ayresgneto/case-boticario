## Case técnico para grupo Oboticário

### Objetivo

1. Desenvolvimento de um modelo de previsões sobre os preços de imóveis a partir de suas características.
2. Implementação do modelo atavés de um pipeline de treinamento automatizado e disponibilização por web service (API)

### Playbook

Este case foi desenvolvido com ferramentas open source e localmente. Portanto é necessário a instalação local dessas
ferramentas para executá-lo. Segue abaixo os passos necessários para ambiente linux:

1. Instalação Airflow localmente:
    No terminal digite: 
        <i>pip install apache-airflow</i>
    Após a instalação, executar em 2 janelas do terminal:
        <i>airflow webserver --port 8080</i>
        <i>airflow scheduler</i>
    Obs: essas janelas devem ficar em execução

2. Instalação Docker Desktop
    No terminal digite:
        Para ubuntu: <i>sudo apt-get install ./docker-desktop-amd64.deb</i>
        Caso use outro sistema operacional, obtenha mais informações aqui: [text](https://www.docker.com/products/docker-desktop/)
    Obs: O Docker desktop deve estar em execução

3. Crie um ambiente virtual e ative-o:
    No terminal digite:
        <i>python -m venv nome_do_ambiente</i> 
        ou, caso esteja usando python3
        <i>python3 -m venv nome_do_ambiente</i>
        Ative-o usando o seguinte comando:
        <i>source nome_do_ambiente/bin/activate</i>

4. Instale as dependências:
    No terminal digite:
        <i>pip install -r requirements.txt</i>

5. Configurando o airflow:
    5.1 criando um novo usuario admin:
        No terminal digite:
            airflow users create \
            --username admin \
            --firstname Peter \
            --lastname Parker \
            --role Admin \
            --email spiderman@superhero.org
        obs: coloque seus dados
    5.2 Acessando airflow:
        No navegador digite:
        <i>http://localhost:8080/</i>
        Faça o login com o usuario criado
    
    5.3 Configurando as dags e plugins
        Adicione as dags do projeto dentro do diretório dags onde o airflow foi instalado 
        e o diretório plugins na raíz da instalação 
    Obs: caso nao exista os diretórios, crie-os




