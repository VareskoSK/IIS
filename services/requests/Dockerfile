FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

CMD ["python", "send_requests.py"]

# Сборка образа
# docker build -t request_sender_image:1 .

# Запуск контейнера
# docker run --rm request_sender_image:1
