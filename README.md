# 🚀 SCPJ - Projeto Django com Docker

Este projeto é uma API desenvolvida em Django, containerizada com Docker, utilizando PostgreSQL como banco de dados.  

## 🧩 Tecnologias utilizadas

- ⚙️ Python + Django 5.2.1  
- 🧱 Django REST Framework  
- 🐘 PostgreSQL 15 (via Docker)  
- 📘 Swagger (drf-yasg)  
- 🐳 Docker + Docker Compose  

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

- Docker  
- Docker Compose  
- Git  
- Python (opcional, apenas para gerar a SECRET_KEY)  

## 🔑 Gerando a DJANGO_SECRET_KEY

Você pode gerar uma chave secreta de duas formas:

**Usando Python puro:**
```python
import secrets
print(secrets.token_urlsafe(50))
```

**Ou usando Django (se instalado localmente):**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> Copie a chave gerada e cole no campo `DJANGO_SECRET_KEY` do arquivo `.env`.

## 🛠️ Criando o arquivo .env

Na raiz do projeto, crie um arquivo `.env` com o seguinte conteúdo:
Esse arquivo deve conter as variáveis de ambiente que definem as configurações sensíveis, como usuário, senha e nome do banco, além da secret key do Django.

```env
# Django
DJANGO_SECRET_KEY= não esqueça de gerar a secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de Dados
POSTGRES_DB= exemplo
POSTGRES_USER= exemplo_user
POSTGRES_PASSWORD= exemplo_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## 🐳 Subindo o projeto com Docker

No terminal, execute:

```bash
docker-compose up --build
```

Esse comando irá:

- Inicializar o container do PostgreSQL  
- Subir o container do Django  
- Expor as portas:  
  - 8000 → Backend (Django)  
  - 5432 → Banco de Dados (PostgreSQL)  

## ✅ Verificando o funcionamento

Após o Docker subir os serviços, acesse no navegador:

- Projeto: http://localhost:8000  
- Documentação Swagger: http://localhost:8000/swagger/  

## 🧠 Comandos úteis

**Parar os containers:**
```bash
docker-compose down
```

**Resetar completamente:**
```bash
docker-compose down -v --rmi all --remove-orphans
docker-compose up --build
```

**Acessar o terminal do container Django:**
```bash
docker exec -it SCPJ_django bash
```


