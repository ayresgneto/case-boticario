import pandas as pd
import logging as log
from datetime import timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

RAW_DATA_PATH = Variable.get('RAW_DATA_PATH')
PROCESSED_DATA_PATH = Variable.get('PROCESSED_DATA_PATH')

def extrai_trata_dados():
    """
    Funcao para extrair e tratar dados
    
    Parâmetros: None

    Retorna: None

    """

    df = pd.read_csv(f"{RAW_DATA_PATH}HousePrices_HalfMil.csv")

    #=================TRATAMENTO NULOS=============================

    log.info('Início do processo de detecção e remoção de nulos')

    nulos = df.isnull().sum().sum()
 
    # Exibir informações sobre os nulos
    if nulos > 0:
        log.info(f'Encontrados {nulos} valores nulos no DataFrame.')
        log.info('Linhas com valores nulos:')
        log.info(df[df.isnull().any(axis=1)]) 

        # Remover linhas com valores nulos
        df = df.dropna()
        log.info('Linhas com valores nulos removidas.')
    else:
        log.info('Nenhum valor nulo encontrado no DataFrame.')
    
    #==============TRATAMENTO OUTLIERS==========================================
    for coluna in df.columns:
        
        log.info('Inicio do processo de deteccao e remocao de outliers')

        #metodo IQR
        Q1 = df[coluna].quantile(0.25)
        Q3 = df[coluna].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        log.info(f'Q1: {Q1}, Q3: {Q3}, IQR: {IQR}')
        log.info(f'Limite inferior: {limite_inferior}, Limite superior: {limite_superior}')

        # Exibir os dados com outliers
        outliers = df[(df[coluna] < limite_inferior) | (df[coluna] > limite_superior)]
        if not outliers.empty:
            log.info('Outliers encontrados:')
            log.info(outliers)

        # Remover os outliers
        df = df[(df[coluna] >= limite_inferior) & (df[coluna] <= limite_superior)]

        log.info('Outliers removidos.')


    #=============TRATAMENTO DUPLICATAS================================================
    
    log.info('Inicio do processo de deteccao e remocao de duplicatas')

    duplicatas_completas = df.duplicated()

    if duplicatas_completas.sum() > 0:
        log.info(f'Foram encontradas {duplicatas_completas.sum()} duplicatas.')
        log.info(df[duplicatas_completas])
        df = df.drop_duplicates()
        log.info('Duplicatas removidas.')
    else:
        log.info('Nenhuma duplicata encontrada.')

    df.to_csv(f"{PROCESSED_DATA_PATH}HousePrices_HalfMil_processed.csv", index=False)

# Definindo os parâmetros da DAG
default_args = {
    'owner': 'Admin',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#DAG
dag = DAG(
    'extrai_dados_dag',
    default_args=default_args,
    description='Dag de extracao de dados',
    #schedule_interval='@daily',  
    #start_date=datetime(2025, 3, 25), 
    catchup=False,
)


extrai = PythonOperator(
    task_id='extrai_trata_dados',
    python_callable=extrai_trata_dados,
    dag=dag,
)

trigger_dag = TriggerDagRunOperator(
    task_id="trigger_dag_treina_salva_modelo",  
    trigger_dag_id="dag_treina_salva_modelo",  
    dag=dag,
)

extrai

