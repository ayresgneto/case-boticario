from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Definindo a DAG
dag = DAG(
    'build_deploy_infra',
    description='Executa comandos Bash para infraestrura',
    schedule_interval=None,
    #start_date=datetime(2025, 3, 27),
    catchup=False  
)

working_directory = '/home/ayres/Documents/projects/case-boticario'

# Definindo o operador Bash que executa o comando Docker Compose
cria_imagem = BashOperator(
    task_id='cria_imagem',
    bash_command=''
    '''
    if [[ -z $(docker images -q case-boticario-image) ]]; then
        echo "Imagem não existe, criando imagem..."
            docker compose build --no-cache
        else
            echo "Imagem já existe, pulando criação da imagem."
        fi
    ''',  
    dag=dag,
    cwd=working_directory
    
)

# Definindo o operador Bash que executa o comando Docker Compose
cria_container = BashOperator(
    task_id='cria_container',
    bash_command=''
    '''
    if [[ -z $(docker ps -q -f name=caseboticario) ]]; then
        echo "Container não está em execução, iniciando container..."
        docker compose up --build -d
    else
        echo "Container já está em execução."
    fi
    ''',  
    dag=dag,
    cwd=working_directory
   
)

cria_imagem >> cria_container

