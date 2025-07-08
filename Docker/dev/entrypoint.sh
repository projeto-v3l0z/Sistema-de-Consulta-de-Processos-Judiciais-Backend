#!/usr/bin/env bash
# Entrypoint customizado para Django com PostgreSQL

set -e

echo "Verificando disponibilidade do PostgreSQL em $POSTGRES_HOST:$POSTGRES_PORT..."

# Espera até que o banco aceite conexões
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "PostgreSQL ainda não está disponível, aguardando..."
  sleep 1
done

echo "PostgreSQL está pronto!"

# Rodar migrations automaticamente
echo "Rodando migrations..."
python manage.py migrate --noinput


exec "$@"
