import json
from app import app


def test_health():
    client = app.test_client()
    r = client.get('/health')
    assert r.status_code == 200
    data = r.get_json()
    assert 'status' in data


def test_predict_no_payload():
    client = app.test_client()
    r = client.post('/predict', data=json.dumps({}), content_type='application/json')
    assert r.status_code == 400


def test_predict_with_value(monkeypatch, tmp_path):
    # Train small model and ensure MODEL file exists for the app to load
    import pandas as pd
    from train_model_h import train_and_save_model_adapted, CLEANED_FILE, MODEL_FILE
    df = pd.DataFrame({'Traffic_Score': [0.1, 0.2, 0.15, 0.3]})
    csv_path = tmp_path / "sample.csv"
    df.to_csv(csv_path, index=False)

    import importlib
    tm = importlib.import_module('train_model_h')
    old_cleaned = getattr(tm, 'CLEANED_FILE')
    tm.CLEANED_FILE = str(csv_path)
    try:
        train_and_save_model_adapted()
        client = app.test_client()
        r = client.post('/predict', data=json.dumps({'X_Feature': 10}), content_type='application/json')
        assert r.status_code == 200
        d = r.get_json()
        assert 'predicted_traffic_score' in d
    finally:
        tm.CLEANED_FILE = old_cleaned
        try:
            import os
            os.remove(MODEL_FILE)
        except Exception:
            pass
