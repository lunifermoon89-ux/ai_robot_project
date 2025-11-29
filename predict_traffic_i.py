import joblib
import pandas as pd
import statsmodels.api as sm

MODEL_FILE = 'traffic_predictor_model.pkl'


def load_model(model_file=MODEL_FILE):
    """Load and return the trained statsmodels RegressionResults object.

    Raises FileNotFoundError if the model file does not exist.
    """
    return joblib.load(model_file)


def predict_value(new_feature_value, model_file=MODEL_FILE):
    """Return a numeric prediction for a single `new_feature_value`.

    This function is intended for programmatic use (APIs, tests).
    """
    trained_model_results = load_model(model_file)

    new_data = pd.DataFrame({'X_Feature': [new_feature_value]})
    X_new = sm.add_constant(new_data, has_constant='add')
    try:
        exog_names = trained_model_results.model.exog_names
        X_new = X_new[exog_names]
    except Exception:
        pass

    predictions = trained_model_results.predict(X_new)
    return float(predictions[0])


def make_prediction():
    """CLI helper kept for backward compatibility: prints a prediction for a fixed input."""
    print("🧠 Loading the trained AI model...")
    try:
        new_feature_value = 400
        predicted_score = predict_value(new_feature_value)

        print("✅ Prediction Successful!")
        print(f"   Input New Feature Value: {new_feature_value}")
        print(f"   Predicted Traffic Score (0.0 to 1.0): {predicted_score:.5f}")

        if predicted_score > 0.7:
            print("\n📈 Interpretation: The model predicts a VERY HIGH relative traffic score for this input.")
        else:
            print("\n📉 Interpretation: The model predicts a MODERATE/LOW relative traffic score for this input.")

    except FileNotFoundError:
        print(f"❌ Error: Model file '{MODEL_FILE}' not found. Did you run 'train_model_h.py'?")
    except Exception as e:
        print(f"❌ Critical Error during prediction: {e}")


if __name__ == "__main__":
    make_prediction()
