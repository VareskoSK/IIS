#!/bin/bash

# Создание базы данных, если не существует
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db

# Запуск MLflow UI
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000

