import mlflow
import mlflow.sklearn
import joblib
import os

from mlflow.tracking import MlflowClient

MLFLOW_TRACKING_URI = "sqlite:////Users/sergejvaresko/iis_proj/mlflow/mlflow.db"  # путь от models/ где у нас лежат данные с пред лр
RUN_ID = "14e724e45887496b805b870e4ddd2364"  
MODEL_PATH = "/Users/sergejvaresko/iis_proj/services/models/model.pkl"

def download_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    model_uri = f"runs:/{RUN_ID}/model"
    model = mlflow.sklearn.load_model(model_uri)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    download_model()
