import os
import math
import joblib
import pandas as pd

from train_model_h import train_and_save_model_adapted
from predict_traffic_i import make_prediction


def test_train_and_predict(tmp_path):
    # Create a small CSV dataset
    df = pd.DataFrame({'Traffic_Score': [0.1, 0.2, 0.15, 0.3]})
    csv_path = tmp_path / "sample.csv"
    df.to_csv(csv_path, index=False)

    # Temporarily point the training script at this file by monkeypatching the constant
    import importlib
    tm = importlib.import_module('train_model_h')
    # Backup constant and set to our sample file
    old_cleaned = getattr(tm, 'CLEANED_FILE')
    tm.CLEANED_FILE = str(csv_path)

    try:
        # Train and save model to default MODEL_FILE
        train_and_save_model_adapted()

        # Assert model file exists
        from train_model_h import MODEL_FILE
        assert os.path.exists(MODEL_FILE)

        # Ensure the saved model can be loaded and the public prediction path runs
        results = joblib.load(MODEL_FILE)
        assert results is not None

        # Call the public prediction function to exercise the end-to-end flow.
        # The function prints output; here we only assert it runs without raising.
        make_prediction()

    finally:
        # restore constant
        tm.CLEANED_FILE = old_cleaned
        # cleanup artifact
        try:
            os.remove(MODEL_FILE)
        except Exception:
            pass
