FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential libpq-dev bash && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt


RUN useradd -ms /bin/bash v3loz

COPY . .

COPY .bashrc /home/v3loz/.bashrc
RUN chown v3loz:v3loz /home/v3loz/.bashrc


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

