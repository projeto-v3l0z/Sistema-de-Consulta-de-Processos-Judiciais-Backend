FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    bash \
    curl \
    vim \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash v3loz

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

COPY Docker/dev/.bashrc /home/v3loz/.bashrc



USER v3loz



# O comando padrão (pode ser sobrescrito no docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000