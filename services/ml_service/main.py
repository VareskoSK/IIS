from typing import Union
from fastapi import FastAPI, HTTPException, Path, Request
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from prometheus_client import Histogram, generate_latest, Counter
from api_handler import FastAPIHandler
import traceback
import pandas as pd

# Путь к модели
MODEL_PATH = "/models/model.pkl" #такой путь указан для сбора докера иначе он не находит путь (для локал апи нужен полный путь)

# Гистограмма предсказаний модели
prediction_histogram = Histogram(
    'model_prediction_values',
    'Распределение предсказаний модели',
    buckets=[0, 0.2, 0.4, 0.6, 0.8, 1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, float('inf')]
)

# Счётчик по статусам HTTP-ответов
http_status_counter = Counter(
    'http_request_status_total',
    'Количество ответов по HTTP статусам',
    ['status']
)

# --- Middleware через FastAPI без сторонних зависимостей ---
app = FastAPI()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        http_status_counter.labels(status=str(response.status_code)).inc()
        return response
    except Exception:
        http_status_counter.labels(status="500").inc()
        raise

handler = FastAPIHandler(model_path=MODEL_PATH)

# Модель данных для входных параметров
class PredictionRequest(BaseModel):
    Driven_kms: float
    Fuel_Type: str
    Selling_type: str
    Transmission: str
    Owner: int
    Age_of_car: float
    Car_depreciation: float

@app.post("/api/prediction/{item_id}")
async def predict(
    item_id: int = Path(..., description="Идентификатор объекта"),
    request: PredictionRequest = ...
):
    """
    Endpoint для предсказания. Принимает item_id в URL и признаки в теле запроса.
    Возвращает item_id и предсказанное значение.
    """

    # Искусственно сгенерировать ошибку 500
    if item_id == 99999:
        raise RuntimeError("Искусственная ошибка 500")

    try:
        features_df = pd.DataFrame([{
            "Driven_kms": request.Driven_kms,
            "Fuel_Type": request.Fuel_Type,
            "Selling_type": request.Selling_type,
            "Transmission": request.Transmission,
            "Owner": request.Owner,
            "Age_of_car": request.Age_of_car,
            "Car_depreciation": request.Car_depreciation
        }])

        # Проверка количества признаков
        feature_names = handler.get_feature_names()
        if len(features_df.columns) != len(feature_names):
            raise HTTPException(
                status_code=400,
                detail=f"Ожидается {len(feature_names)} признаков: {feature_names}, получено {len(features_df)}."
            )

        # Предсказание
        prediction = handler.predict(features_df)
        prediction_histogram.observe(prediction)

        return {
            "item_id": item_id,
            "predict": prediction
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера. Проверьте логи.")

@app.get("/api/feature_names")
async def get_feature_names():
    return {"feature_names": handler.get_feature_names()}

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type="text/plain")