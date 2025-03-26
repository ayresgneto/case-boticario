import json
import os
import pickle
from datetime import datetime, timedelta
import sklearn
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

# Função para carregar o modelo e seus metadados
def carrega_modelo_scaler_metadados(model_dir = "artefatos"):

    # Lista todos os arquivos de modelo no diretório especificado
    models = [f for f in os.listdir(os.path.join(model_dir, "modelo")) if f.startswith("modelo_v") and f.endswith(".pkl")]

    # Retorna None caso não existam modelos no diretório
    if not models:
        return None, None
    
    # Extrai as versões dos modelos disponíveis
    versions = [int(m.split("_v")[-1].split(".pkl")[0]) for m in models]
    
    # Determina a versão mais recente
    latest = max(versions)
    
    # Define os caminhos para os arquivos do modelo e dos metadados mais recentes
    model_file = os.path.join(model_dir, f"modelo/modelo_v{latest}.pkl")
    metadata_file = os.path.join(model_dir, f"metadados/metadados_v{latest}.json")
    scaler_file = os.path.join(model_dir, f"scaler/scaler_v{latest}.json")
    
    # Carrega o modelo do arquivo
    with open(model_file, "rb") as f:
        model = pickle.load(f)

    # Carrega o scaler do arquivo
    with open(scaler_file, "rb") as f:
        scaler = json.load(f)
    
    # Carrega os metadados do arquivo
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    
    # Retorna o modelo e seus metadados
    return model, scaler, metadata

# Definindo os parâmetros da DAG
default_args = {
    'owner': 'Admin',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#DAG
dag = DAG(
    'carregar_dag',
    default_args=default_args,
    description='Dag de treinamento do modelo',
    #schedule_interval='@daily',  
    #start_date=datetime(2025, 3, 25), 
    catchup=False,
)


carregar = PythonOperator(
    task_id='carrega_modelo_scaler_e_metadados',
    python_callable=carrega_modelo_scaler_metadados,
    dag=dag,
)

carregar
