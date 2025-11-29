"""Orchestration script: train the model then run a prediction.

This script calls the training function from `train_model_h.py` then calls
the prediction function in `predict_traffic_i.py`. It's a convenience helper
for local verification / deployment smoke tests.
"""

from train_model_h import train_and_save_model_adapted
from predict_traffic_i import make_prediction


def main():
    print("=== Run all: training then prediction ===")
    train_and_save_model_adapted()
    make_prediction()


if __name__ == "__main__":
    main()
