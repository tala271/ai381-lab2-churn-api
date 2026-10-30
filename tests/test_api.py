from fastapi.testclient import TestClient

from src.app.main import app, get_model

client = TestClient(app)

VALID = {
    "tenure_months": 12,
    "monthly_charges": 70.5,
    "support_calls": 3,
    "contract": "Month-to-month",
    "internet_service": "Fiber optic",
}


def test_health_contract():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_model_loads():
    model = get_model()
    assert hasattr(model, "predict_proba")


def test_input_schema_rejects_negative_tenure():
    r = client.post("/predict", json={**VALID, "tenure_months": -5})
    assert r.status_code == 422


def test_edge_case_unknown_category_still_predicts():
    r = client.post("/predict", json={**VALID, "contract": "Never-seen-before"})
    assert r.status_code == 200
    assert 0.0 <= r.json()["churn_probability"] <= 1.0


def test_prediction_is_deterministic():
    r1 = client.post("/predict", json=VALID).json()
    r2 = client.post("/predict", json=VALID).json()
    assert r1 == r2