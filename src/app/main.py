import os
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/model.joblib"))

app = FastAPI(title="Churn API")
_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


class CustomerIn(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_charges: float = Field(ge=0)
    support_calls: int = Field(ge=0)
    contract: str = Field(min_length=1)
    internet_service: str = Field(min_length=1)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(customer: CustomerIn):
    try:
        model = get_model()
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="model not found")
    row = pd.DataFrame([customer.model_dump()])
    proba = float(model.predict_proba(row)[0, 1])
    return {"churn_probability": round(proba, 4), "churn": proba > 0.5}