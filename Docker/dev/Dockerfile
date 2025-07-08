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
COPY Docker/dev/entrypoint.sh /home/v3loz/entrypoint.sh
RUN chown v3loz:v3loz /home/v3loz/.bashrc /home/v3loz/entrypoint.sh

USER v3loz

# Chama o entrypoint explicitamente com bash
ENTRYPOINT ["bash", "/home/v3loz/entrypoint.sh"]

# O comando padrão (pode ser sobrescrito no docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000