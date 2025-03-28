from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator 
from airflow.models import Variable
from datetime import timedelta
import pandas as pd
import json
import os
import logging as log
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from utils import salva_modelo_scaler_metadados

PROCESSED_DATA_PATH = Variable.get('PROCESSED_DATA_PATH')
ARTEFATOS_PATH = Variable.get('ARTEFATOS_PATH')
METADADOS_PATH = Path('/home/ayres/Documents/projects/case-boticario/artefatos/metadados')

# Função Python a ser executada pela DAG
def treina_salva_modelo():
    """
    Funcao para treinar e salvar modelo
    
    Parâmetros: None
 
    Retorna: None
    
    """
    try:
        # Carrega os dados de um arquivo CSV
        df = pd.read_csv(f"{PROCESSED_DATA_PATH}HousePrices_HalfMil_processed.csv")
    
        # Separa as features (X) do target (y)
        X = df.drop("Prices", axis = 1)
        y = df["Prices"]

        # Divide os dados em conjuntos de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

        #Normaliza dados
        scaler = MinMaxScaler()

        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Instancia o modelo de regressão linear
        modelo = LinearRegression()

        # Treina o modelo com os dados de treino
        modelo.fit(X_train, y_train)

        # Salva o modelo treinado e seus metadados, retornando a versão do modelo
        version = salva_modelo_scaler_metadados(modelo, scaler, X_train, y_train)

        #Exibe a versão do modelo treinado
        log.info(f"\nModelo treinado e salvo com versão {version}\n")

    except Exception as e:
        log.error("Erro ao treinar o modelo: %s", str(e))


# Definindo os parâmetros da DAG
default_args = {
    'owner': 'Admin',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#DAG
dag = DAG(
    'dag_treina_salva_modelo',
    default_args=default_args,
    description='Dag de treinamento do modelo',
    #schedule_interval='@daily',  
    #start_date=datetime(2025, 3, 25), 
    catchup=False,
)


treinar_modelo = PythonOperator(
    task_id='treina_modelo',
    python_callable=treina_salva_modelo,
    dag=dag,
)

trigger_dag = TriggerDagRunOperator(
    task_id="trigger_dag_build_deploy_infra",  
    trigger_dag_id="build_deploy_infra",  
    dag=dag,
)

# Definindo a ordem de execução das tarefas
treinar_modelo 