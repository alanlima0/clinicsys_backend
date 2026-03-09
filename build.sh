#!/usr/bin/env bash
# O comando abaixo garante que o script pare se houver algum erro
set -o errexit

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "Rodando as migrações do banco de dados..."
python manage.py migrate

echo "Criando superusuário customizado..."
# Como seu modelo usa 'nome' em vez de 'username', passamos o argumento explicitamente.
# O Django lerá a senha da variável DJANGO_SUPERUSER_PASSWORD automaticamente.
if [ "$DJANGO_SUPERUSER_NOME" ]; then
  python manage.py createsuperuser \
    --no-input \
    --nome "$DJANGO_SUPERUSER_NOME" \
    --email "$DJANGO_SUPERUSER_EMAIL" || true
fi