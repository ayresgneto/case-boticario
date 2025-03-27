from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Definindo a DAG
dag = DAG(
    'build_deploy_infra',
    description='Executa comandos Bash para infraestrura',
    schedule_interval=None,
    start_date=datetime(2025, 3, 27),
    catchup=False  
)

# Definindo o operador Bash que executa o comando Docker Compose
docker_compose_build = BashOperator(
    task_id='docker_compose_build_task',
    bash_command='docker compose build --no-cache',  
    dag=dag
)

# Definindo o operador Bash que executa o comando Docker Compose
docker_compose_build = BashOperator(
    task_id='docker_compose_build_task',
    bash_command='docker compose build --no-cache',  
    dag=dag
)

