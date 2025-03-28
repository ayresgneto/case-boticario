from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from airflow.operators.dagrun_operator import TriggerDagRunOperator 
import json
import os
import logging as log

METADADOS_PATH = Variable.get('METADADOS_PATH')

# Funcao para carregar o valor de 'r2' do arquivo JSON
def carregar_r2_from_json():
    try:
            # Percorre diretorio de metadados
            metadados_files = [f for f in os.listdir(METADADOS_PATH) if f.startswith("metadados_v") and f.endswith(".json")]

            if metadados_files:

                latest_file = max(metadados_files, key=lambda f: int(f.split("_v")[-1].split(".json")[0]))
                with open(latest_file, "r") as f:
                    metadata = json.load(f)

                r2 = metadata.get('r2_train')

            else:
                log.info("No metadados files found.")
                return None
    except Exception as e:
        log.error("Erro ao carregar e otimizar modelo: %s", str(e))
    return r2

# Função para otimizar os hiperparâmetros
def otimizar_hiperparametros():
  
    log.info("Otimizacao dos hiperparametros em andamento...")
    
    return "Hiperparametros otimizados"

# Função principal para validar o valor de r2 e executar o fluxo
def verificar_e_otimizar():
    r2_value = carregar_r2_from_json()
    
    if r2_value is None:
        raise ValueError("Não foi possível carregar o valor de 'r2' do arquivo JSON.")
    
    log.info(f"Valor de 'r2': {r2_value}")
    
    # Verifique se o r2 é menor que 0.7
    if r2_value < 0.7:
        log.info("r2 é menor que 0.7, iniciando otimização dos hiperparâmetros...")
        
        # Otimizar hiperparametros
        otimizar_hiperparametros()
        
        # Retorna trigger da dag de treinamento
        return 'trigger_training_dag'
        
    else:
        log.info("r2 é maior ou igual a 0.7, não é necessário otimizar os hiperparâmetros.")

# Definindo a DAG
with DAG(
    'validar_e_otimizar_modelo',
    default_args={'owner': 'airflow'},
    description='DAG para validar o r2 e otimizar os hiperparâmetros',
    schedule_interval=None,  
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Defina a tarefa de verificação e otimização
    verificar_tarefa = PythonOperator(
        task_id='verificar_e_otimizar',
        python_callable=verificar_e_otimizar,
    )

    # Define a tarefa de disparar a DAG de treinamento
    trigger_training_dag = TriggerDagRunOperator(
        task_id='trigger_training_dag',
        trigger_dag_id='dag_treina_salva_modelo'
    )

    # Definindo o fluxo de tarefas
    verificar_tarefa >> trigger_training_dag