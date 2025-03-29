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




