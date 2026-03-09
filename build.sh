#!/usr/bin/env bash
# O comando abaixo garante que o script pare se houver algum erro
set -o errexit

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "Rodando as migrações do banco de dados..."
python manage.py migrate

echo "Criando superusuário..."
# Quando usamos --no-input, o Django busca SOZINHO as variáveis:
# DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL e DJANGO_SUPERUSER_PASSWORD
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input || true
fi