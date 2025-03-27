import pandas as pd
from fastapi import FastAPI
from app.modelo import InputData
from plugins.utils import carrega_modelo_scaler_metadados

# Cria uma instância da aplicação FastAPI
app = FastAPI()

# Define uma rota de check do serviço
@app.get("/check")
def health_check():

    # Retorna o status do serviço
    return {"status": "ok"}

# Define uma rota para previsão
@app.post("/predict")
def predict(input_data: InputData):

    # Carrega o modelo treinado e seus metadados
    model, scaler, metadata = carrega_modelo_scaler_metadados()
    
    # Verifica se um modelo está disponível
    if model is None:

        # Retorna erro caso não haja modelo treinado
        return {"error": "Nenhum modelo treinado disponível"}
    
    
    X = pd.DataFrame([[input_data.Area, 
                       input_data.Garage, 
                       input_data.FirePlace,
                       input_data.Baths,
                       input_data.White_Marble,
                       input_data.Black_Marble,
                       input_data.Indian_Marble,
                       input_data.Floors,
                       input_data.City,
                       input_data.Solar,
                       input_data.Electric,
                       input_data.Fiber,
                       input_data.Glass_Doors,
                       input_data.Swiming_Pool,
                       input_data.Garden]], 
                     columns = ['Area', 'Garage', 'FirePlace', 'Baths', 'White Marble', 'Black Marble', 
                        'Indian Marble', 'Floors', 'City', 'Solar', 'Electric', 'Fiber', 
                        'Glass Doors', 'Swiming Pool', 'Garden'])
    
    # Aplica o scaler aos dados de entrada
    X_scaled = scaler.transform(X)

    # Predict
    prediction = model.predict(X_scaled)[0]
    
    # Retorna a previsão e a versão do modelo utilizado
    return {"Previsão": prediction, 
            "Versão do Modelo": metadata["version"], 
            "timestamp": metadata["timestamp"],
            "Versão do Scikit-Learn": metadata["scikit_learn_version"], 
            "Coeficiente R2 em Treino": metadata["r2_train"],
            "MSE": metadata["mse_train"],
            "RMSE": metadata["rmse_train"],
            "MAE": metadata["mae_train"],
            "MAPE": metadata["mape_train"],
            }





