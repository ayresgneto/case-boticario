# Projeto 6 - Construindo e Operacionalizando Pipeline de Previsão em Tempo Real
# Módulo Cliente Para Consumo da API

# Import
import requests

# Função para testar a API
def check_api():
    
    # URL do endpoint da API
    url = "http://localhost:8000/check"
    
    # Faz a chamada à API e armazena a resposta
    response = requests.get(url)
    
    # Imprime a resposta
    if response.status_code == 200:
        print("Status da saúde da API:", response.json())
    else:
        print(f"Erro ao checar saúde da API. Código de status: {response.status_code}")

# Função para consumir a API
def consome_api():
    
    # URL do endpoint da API
    url = "http://localhost:8000/predict"
    
    # Dados de entrada
    payload = {
        
        "Area": 120,
        "Garage": 1,
        "FirePlace": 1,
        "Baths": 2,
        "White_Marble":0,
        "Black_Marble":0,
        "Indian_Marble":1,
        "Floors":1,
        "City":1,
        "Solar":0,
        "Electric":1,
        "Fiber":0,
        "Glass_Doors":1,
        "Swiming_Pool":0,
        "Garden":1
    }
    
    # Faz a chamada à API e armazena a resposta
    response = requests.post(url, json = payload)
    
    # Imprime a resposta
    if response.status_code == 200:
        print("Resposta da API:", response.json())
    else:
        print(f"Erro ao chamar a API. Código de status: {response.status_code}")

# Bloco principal
if __name__ == "__main__":
    check_api()
    consome_api()



