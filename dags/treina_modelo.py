from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator 
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from dags import salva_modelo_scaler_metadados

# Função Python a ser executada pela DAG
def treina_modelo(data_path = "dados/processed/HousePrices_HalfMil_processed.csv"):
    
    # Carrega os dados de um arquivo CSV
    df = pd.read_csv(data_path)
    
    # Separa as features (X) do target (y)
    X = df.drop("target", axis = 1)
    y = df["target"]
    
    # Divide os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
    
    # Instancia o modelo de regressão linear
    modelo = LinearRegression()
    
    # Treina o modelo com os dados de treino
    modelo.fit(X_train, y_train)

    return {
        "model": modelo,
        "X_train": X_train,
        "y_train": y_train,
        "model_version": 1,
    }
    
    # Salva o modelo treinado e seus metadados, retornando a versão do modelo
    #version = salva_modelo_scaler_metadados(modelo, X_train, y_train)
    
    # Exibe a versão do modelo treinado
    #print(f"\nModelo treinado e salvo com versão {version}\n")

# Definindo os parâmetros da DAG
default_args = {
    'owner': 'Admin',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#DAG
dag = DAG(
    'exemplo_python_e_shell',
    default_args=default_args,
    description='Dag de treinamento do modelo',
    #schedule_interval='@daily',  
    #start_date=datetime(2025, 3, 25), 
    catchup=False,
)


treinar_modelo = PythonOperator(
    task_id='treina_modelo',
    python_callable=treina_modelo,
    dag=dag,
)

salvar_carregar_dag = TriggerDagRunOperator(
    task_id="trigger_save_model_dag",
    trigger_dag_id="salvar_carregar_dag",
    conf={
        "model": "{{ task_instance.xcom_pull(task_ids='treina_modelo')['model'] }}",
        "X_train": "{{ task_instance.xcom_pull(task_ids='treina_modelo')['X_train'] }}",
        "y_train": "{{ task_instance.xcom_pull(task_ids='treina_modelo')['y_train'] }}",
        "model_version": "{{ task_instance.xcom_pull(task_ids='treina_modelo')['model_version'] }}"
    }, 
    dag=dag,
)


# Definindo a ordem de execução das tarefas
treinar_modelo >> salvar_carregar_dag
