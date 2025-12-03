# Dockerfile
FROM python:3.11-slim

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD cd /app/web_ui && uvicorn app:app --host 0.0.0.0 --port 8000