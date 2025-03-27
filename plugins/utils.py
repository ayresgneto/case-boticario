import os
import pickle as pkl
import json
import sklearn
from datetime import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
import numpy as np
from pathlib import Path

LOCAL_ARTEFATOS = Path('/home/ayres/Documents/projects/case-boticario/artefatos')

def salva_modelo_scaler_metadados(modelo, scaler, X_train, y_train, model_dir = LOCAL_ARTEFATOS):
    """
    Funcao para salvar modelo, scaler e metadados
    
    Parâmetros:
    - modelo(Object): Objeto instanciado do modelo
    - scaler(Object): Objeto instanciado do scaler
    - X_train(ndarray): array com dados de x_train
    - y_train(ndarray): array com dados de y_train
    - model_dir(string): Caminho do diretorio onde estao armazenados os artefatos gerados pelo modelo
    
    Retorna:
    current_version(int): versao do modelo salvo
    """

    # Lista todos os arquivos de modelo no diretorio especificado
    models = [f for f in model_dir.rglob('modelo_v*.pkl')]
    
    # Determina a proxima versao do modelo
    current_version = 1 if not models else max([int(m.name.split("_v")[-1].split(".pkl")[0]) for m in models]) + 1
    
    # Define os caminhos para os arquivos do modelo e dos metadados
    model_file = os.path.join(model_dir, f"modelo/modelo_v{current_version}.pkl")
    metadata_file = os.path.join(model_dir, f"metadados/metadados_v{current_version}.json")
    scaler_file = os.path.join(model_dir, f"scaler/scaler_v{current_version}.pkl")
    
    # Salva o modelo no arquivo especificado
    with open(model_file, "wb") as f:
        pkl.dump(modelo, f)
    
    y_pred = modelo.predict(X_train)
    
    # Calcula as métricas de avaliação do modelo
    r2_train = r2_score(y_train, y_pred)
    mse_train = mean_squared_error(y_train, y_pred)
    rmse_train = np.sqrt(mse_train)
    mae_train = mean_absolute_error(y_train, y_pred)
    mape_train = mean_absolute_percentage_error(y_train, y_pred)
    
    
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
    with open(scaler_file, "wb") as f:
        pkl.dump(scaler, f)
    
    # Retorna a versão do modelo salvo
    return current_version

CONTAINER_ARTEFATOS = Path('/app/artefatos')

# Função para carregar o modelo e seus metadados
def carrega_modelo_scaler_metadados(model_dir = CONTAINER_ARTEFATOS):
    """
    Funcao para carregar modelo, scaler e metadados
    
    Parâmetros: 
    - model_dir(string): Caminho do diretorio onde estao armazenados os artefatos gerados pelo modelo
 
    Retorna:
    - model(Object pickle): Objeto com modelo carregado
    - scaler(Object pickle): Objeto com scaler carregado
    - metadata(JSON): Json com metadados carregado
    """

    # Lista todos os arquivos de modelo no diretório especificado
    models = [f for f in model_dir.rglob('modelo_v*.pkl')]
    
    # Retorna None caso não existam modelos no diretório
    if not models:
        print("No model files found.")
        return None, None, None
    
    # Extrai as versões dos modelos disponíveis
    versions = [int(m.name.split("_v")[-1].split(".pkl")[0]) for m in models]

    # Determina a versão mais recente
    latest = max(versions)
    
    # Define os caminhos para os arquivos do modelo, scaler e dos metadados mais recentes
    model_file = os.path.join(model_dir, f"modelo/modelo_v{latest}.pkl")
    scaler_file = os.path.join(model_dir, f"scaler/scaler_v{latest}.pkl")
    metadata_file = os.path.join(model_dir, f"metadados/metadados_v{latest}.json")
    
    # Carrega o modelo do arquivo
    with open(model_file, "rb") as f:
        model = pkl.load(f)

        # Carrega o modelo do arquivo
    with open(scaler_file, "rb") as f:
        scaler = pkl.load(f)
    
    # Carrega os metadados do arquivo
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    
    # Retorna o modelo e seus metadados
    return model, scaler, metadata