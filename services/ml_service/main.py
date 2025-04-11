from typing import Union
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from api_handler import FastAPIHandler
import traceback
import pandas as pd

# Путь к модели
MODEL_PATH = "/models/model.pkl" #такой путь указан для сбора докера иначе он не находит путь (для локал апи нужен полный путь)


# Инициализация FastAPI и обработчика
app = FastAPI()
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

        return {
            "item_id": item_id,
            "predict": prediction
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера. Проверьте логи.")

@app.get("/api/feature_names")
async def get_feature_names():
    """
    Возвращает список всех признаков, которые модель использует для предсказания.
    """
    return {"feature_names": handler.get_feature_names()}