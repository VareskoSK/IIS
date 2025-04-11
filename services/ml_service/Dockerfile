FROM python:3.11-slim


# устанавливаем рабочую директорию
WORKDIR /ml_service

# устнаваливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    curl \
    && apt-get clean

# копируем всё содержимое в контейнер
COPY . /ml_service

# models volume'ом
VOLUME ["/models"]

# ставим Python-зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

#  порт 
EXPOSE 8000

# запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# команда сборки образа
# docker build -t ml_service_image:1 .

# команда запуска контейнера
# docker run -p 8000:8000 -v $(pwd)/../models:/models ml_service_image:1