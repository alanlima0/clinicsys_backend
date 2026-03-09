FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e garante logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalando dependências do sistema necessárias para o PostgreSQL e compilação
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalando dependências do Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiando o código do projeto para dentro do container
COPY . .

# Garante que o script de build tenha permissão de execução
RUN chmod +x build.sh

# O pulo do gato: Primeiro roda o build (migrações/static/superuser) 
# e só depois inicia o Gunicorn na porta 10000
CMD ["sh", "-c", "./build.sh && gunicorn gestao_clinica.wsgi:application --bind 0.0.0.0:10000"]