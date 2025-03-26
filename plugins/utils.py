import os
import pickle as pkl
import json
import sklearn
from datetime import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
import numpy as np

LOCAL_ARTEFATOS = '/home/ayres/Documents/projects/case-boticario/artefatos'

def salva_modelo_scaler_metadados(modelo, scaler, X_train, y_train, model_dir = LOCAL_ARTEFATOS):

    # Lista todos os arquivos de modelo no diretório especificado
    models = [f for f in os.listdir(model_dir) if f.startswith("modelo_v") and f.endswith(".pkl")]
    
    # Determina a próxima versão do modelo
    current_version = 1 if not models else max([int(m.split("_v")[-1].split(".pkl")[0]) for m in models]) + 1
    
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