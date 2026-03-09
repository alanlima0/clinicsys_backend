FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalando dependências do sistema
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalando dependências do Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiando o projeto
COPY . .

# RENDER: Dando permissão de execução para o script de build
RUN chmod +x build.sh

# RENDER: O comando final agora roda o build (migrações/static) e inicia o servidor gunicorn
CMD ["sh", "-c", "./build.sh && gunicorn gestao_clinica.wsgi:application --bind 0.0.0.0:10000"]