import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from utils import salva_modelo_scaler_metadados
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pandas as pd
import logging as log

# Variáveis de caminho de dados
PROCESSED_DATA_PATH = Variable.get('PROCESSED_DATA_PATH')
ARTEFATOS_PATH = Variable.get('ARTEFATOS_PATH')
METADADOS_PATH = Variable.get('METADADOS_PATH')

#================CONFIG MLFLOW===================================================================
# Defina o nome do experimento
experiment_name = 'case_experimento_mlflow'

# Cria ou obtém o experimento

experiment_id = mlflow.create_experiment(experiment_name) if mlflow.get_experiment_by_name(experiment_name) is None else mlflow.get_experiment_by_name(experiment_name).experiment_id
# Configura o experimento no MLflow
mlflow.set_experiment(experiment_name)

#====================FUNÇÕES==========================================================================

# Função para treinar e otimizar o modelo
def treina_salva_modelo(**kwargs):
    """
    Funcao para treinar e salvar modelo
    
    Parâmetros:
    - kwargs(dict): retorno para passar r2 para funcao de check metricas
    """
    try:
        # Carrega os dados de um arquivo CSV
        df = pd.read_csv(f"{PROCESSED_DATA_PATH}HousePrices_HalfMil_processed.csv")
    
        # Separa as features (X) do target (y)
        X = df.drop("Prices", axis=1)
        y = df["Prices"]

        # Divide os dados em conjuntos de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Normaliza os dados
        scaler = MinMaxScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Hiperparametros para otimizacao
        param_grid = {
            'fit_intercept': [True, False]
        }

        modelo = LinearRegression()

        # Otimização de hiperparâmetros com GridSearchCV
        grid_search = GridSearchCV(modelo, param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1)

        # Inicia o monitoramento no MLflow
        with mlflow.start_run():

            # Adicionando os hiperparametros no MLflow
            for param, value in param_grid.items():
                mlflow.log_param(param, value)

            # Realiza o ajuste dos hiperparametros
            grid_search.fit(X_train, y_train)

            # Melhor modelo e seus parâmetros
            best_model = grid_search.best_estimator_

            # Logando o melhor modelo no MLflow
            mlflow.sklearn.log_model(best_model, "modelo_treinado")
            
            # Calculando r2 e logando no MLflow
            r2 = best_model.score(X_test, y_test)
            log.info(f"R2 Score: {r2}")
            mlflow.log_metric("r2", r2)

            # Registra os parametros no MLflow
            mlflow.log_params(param_grid)

            # Salva o modelo e os metadados, e retorna a versão
            version = salva_modelo_scaler_metadados(best_model, scaler, X_train, y_train)

            log.info(f"\nModelo treinado e salvo com versão {version}\n")
            kwargs['ti'].xcom_push(key='r2', value=r2)

    except Exception as e:
        log.error("Erro ao treinar o modelo: %s", str(e))


# Função para monitorar métricas e detectar drift
def check_metricas(**kwargs):
    """
    Funcao para check de metricas
    
    Parâmetros:
    - kwargs(dict): retorno de treino_salva_modelo()
    """
    # dados recebidos via xcom
    ti = kwargs['ti']
    r2 = ti.xcom_pull(task_ids='treina_modelo', key='r2')
    try:

        if r2:
            if r2 < 0.7:
                log.info("ATENÇÃO: R2 é menor que 0.7. Possível Drift")

                #aqui poderiamos adicionar alertas por e-mail, slack ou outras ferramentas como grafana, etc
            else:
                log.info(f"R2: {r2}")
        else:
            log.info("Nenhum valor de R2 encontrado.")
                    
    except Exception as e:
        log.error("Erro ao checar metadados: %s", str(e))

#=====================DAG CONFIGS=========================================================

# Definindo os parametros da DAG
default_args = {
    'owner': 'Admin',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG
dag = DAG(
    'dag_treina_salva_modelo',
    default_args=default_args,
    schedule_interval=None,
    description='DAG de treinamento do modelo com MLflow e otimização',
    catchup=False,
)

# Definindo as tarefas
treinar_modelo = PythonOperator(
    task_id='treina_modelo',
    python_callable=treina_salva_modelo,
    provide_context=True,
    dag=dag,
)

checar_metricas = PythonOperator(
    task_id='check_metricas',
    python_callable=check_metricas,
    provide_context=True,
    dag=dag,
)


trigger_dag = TriggerDagRunOperator(
    task_id="trigger_dag_build_deploy_infra",  
    trigger_dag_id="build_deploy_infra",  
    dag=dag,
)

# Ordem de execução das tarefas
treinar_modelo >> checar_metricas

