import json
import os
import pickle
from datetime import datetime, timedelta
import sklearn
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

# Função para salvar o modelo e gerar metadados
def salva_modelo_scaler_metadados(model, scaler, X_train, y_train, model_dir = "artefatos"):

    # Lista todos os arquivos de modelo no diretório especificado
    models = [f for f in os.listdir(model_dir) if f.startswith("modelo_dsa_v") and f.endswith(".pkl")]
    
    # Determina a próxima versão do modelo
    current_version = 1 if not models else max([int(m.split("_v")[-1].split(".pkl")[0]) for m in models]) + 1
    
    # Define os caminhos para os arquivos do modelo e dos metadados
    model_file = os.path.join(model_dir, f"/modelo/modelo_v{current_version}.pkl")
    metadata_file = os.path.join(model_dir, f"metadados/metadados_v{current_version}.json")
    scaler_file = os.path.join(model_dir, f"scaler/scaler_v{current_version}.pkl")
    
    # Salva o modelo no arquivo especificado
    with open(model_file, "wb") as f:
        pickle.dump(model, f)
    
    y_pred = model.predict(X_train)
    
    # Calcula metricas
    r2_train = model.score(X_train, y_train)
    mse_train = model.mean_squared_error(y_train, y_pred)  
    rmse_train = model.np.sqrt(mse_train)  
    mae_train = model.mean_absolute_error(y_train, y_pred)  
    mape_train = model.mean_absolute_percentage_error(y_train, y_pred)
    
    
    # Gera os metadados, incluindo versão, timestamp, versão do scikit-learn e R² em treino
    metadata = {
        "version": current_version,
        "timestamp": datetime.now().isoformat(),
        "scikit_learn_version": sklearn.__version__,
        "r2_train": r2_train,
        "mse_train": mse_train,
        "rmse_train": rmse_train,
        "mae_train": mae_train,
        "mape_train": mape_train
    }
    
    # Salva os metadados no arquivo especificado
    with open(metadata_file, "w") as f:
        json.dump(metadata, f)
    
    # Salva scaler no arquivo especificado
    with open(scaler_file, "w") as f:
        json.dump(scaler, f)
    
    # Retorna a versão do modelo salvo
    return current_version

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
    model_file = os.path.join(model_dir, f"modelo/modelo_dsa_v{latest}.pkl")
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
    'salvar_carregar_dag',
    default_args=default_args,
    description='Dag de treinamento do modelo',
    #schedule_interval='@daily',  
    #start_date=datetime(2025, 3, 25), 
    catchup=False,
)


salvar = PythonOperator(
    task_id='salva_modelo_scaler_e_metadados',
    python_callable=salva_modelo_scaler_metadados,
    dag=dag,
)

carregar = PythonOperator(
    task_id='carrega_modelo_scaler_e_metadados',
    python_callable=carrega_modelo_scaler_metadados,
    dag=dag,
)

salvar >> carregar
