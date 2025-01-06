FROM python:3.9-slim

WORKDIR /app

COPY rabbitmq_exporter.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV RABBITMQ_PROTOCOL=http \
    RABBITMQ_HOST=localhost \
    RABBITMQ_PORT=15672 \
    RABBITMQ_USER=guest \
    RABBITMQ_PASSWORD=guest \
    EXPORTER_PORT=8000

EXPOSE 8000

CMD ["python", "rabbitmq_exporter.py"]