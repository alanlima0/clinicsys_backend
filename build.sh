#!/usr/bin/env bash
# O comando abaixo garante que o script pare se houver algum erro
set -o errexit

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "Rodando as migrações do banco de dados..."
python manage.py migrate

echo "Criando superusuário (se não existir)..."
# O Django 3.0+ permite criar superusuários via variáveis de ambiente.
# O "|| true" no final garante que, se o usuário já existir nos próximos deploys, o script não quebre o deploy.
if [[ -n "${DJANGO_SUPERUSER_USERNAME}" && -n "${DJANGO_SUPERUSER_PASSWORD}" ]]; then
  python manage.py createsuperuser \
      --noinput \
      --username "${DJANGO_SUPERUSER_USERNAME}" \
      --email "${DJANGO_SUPERUSER_EMAIL:-admin@exemplo.com}" || true
fi