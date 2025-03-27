# imagem base mínima com Linux e Linguagem Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências especificadas no arquivo requirements.txt sem cache
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação para o container
COPY app/ app/

# Copia os dados necessários para o container
COPY dados/processed/ dados/

# Copia o diretório do modelo treinado para o container
COPY modelo/ modelo/

# Define a porta que será exposta para acesso à aplicação
EXPOSE 8000

# Comando para iniciar o servidor FastAPI com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
