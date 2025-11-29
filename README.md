# ai_robot_project

![CI](https://github.com/lunifermoon89-ux/ai_robot_project/actions/workflows/ci.yml/badge.svg)

Tiny ML utility that trains a single-feature OLS model to predict `Traffic_Score` from `final_feature_set.csv` and runs a simple prediction.

Quick start

1) Install dependencies (PowerShell):

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2) Train the model (creates `traffic_predictor_model.pkl`):
# ai_robot_project

![CI](https://github.com/lunifermoon89-ux/ai_robot_project/actions/workflows/ci.yml/badge.svg)

Tiny ML utility that trains a single-feature OLS model to predict `Traffic_Score` from `final_feature_set.csv` and runs a simple prediction.

Quick start (PowerShell):

Install dependencies:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Train the model:
```powershell
python train_model_h.py
```

Run a prediction (CLI):

```powershell
python predict_traffic_i.py
```

Or run both (train then predict):

```powershell
python run_all.py
```

Notes and conventions:
- The training script expects `final_feature_set.csv` to contain a `Traffic_Score` column. The code constructs the single numeric feature `X_Feature` from the DataFrame index (`df.index.values`).
- Both training and prediction use `sm.add_constant(...)` from `statsmodels` to include an intercept. Keep this consistent if adding features.
- The trained model is saved to `traffic_predictor_model.pkl` using `joblib` and the saved object is a `statsmodels` `RegressionResults` instance which is used directly at prediction time.


Deployment
----------

Publish to GitHub Container Registry (GHCR)
- This repository includes workflows under `.github/workflows/` to build and push the Docker image to GHCR.
- After a successful run the image will be available as `ghcr.io/lunifermoon89-ux/ai_robot_project:latest`.

Publish to Docker Hub (optional)
- Add two repository secrets if you want Docker Hub publishing:
  - `DOCKERHUB_USERNAME` — your Docker Hub username
  - `DOCKERHUB_TOKEN` — a Docker Hub access token

How to add the Docker Hub secrets
1. Go to `Settings` → `Secrets and variables` → `Actions` in your GitHub repository.
2. Create `DOCKERHUB_USERNAME` with your Docker Hub username.
3. Create `DOCKERHUB_TOKEN` with a Docker Hub personal access token (create it on Docker Hub — do not use your password).

How to publish an image (recommended)
1. Push to `main`: the `publish-all.yml` workflow will run and publish to GHCR automatically.
2. If you've added Docker Hub secrets, the same workflow will also publish to Docker Hub.

How to pull the image
- From GHCR:
  - `docker pull ghcr.io/lunifermoon89-ux/ai_robot_project:latest`

API docs
--------

After the app is running (locally or in container), view the interactive API docs:

- `http://localhost:8080/docs` — Swagger UI (loads `/openapi.json`).

Client examples
---------------

- Python client (uses `requests`) — `scripts/client_predict.py`:
  - Example: `python scripts/client_predict.py 400`
- curl example:
  - `curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d "{\"X_Feature\":400}"`

Serving locally
---------------

- Windows (PowerShell helper):

```powershell
# start (detached, writes logs + server.pid)
.\scripts\start-server.ps1 -Action start

# stop
.\scripts\start-server.ps1 -Action stop
```

- POSIX (Linux / macOS):

```bash
# start (detached)
./scripts/start-server.sh start

# stop
./scripts/start-server.sh stop
```

Direct run (development):

```powershell
& .venv\Scripts\python.exe serve.py
```

Notes
-----
- The server helper scripts start `serve.py`, which will prefer `waitress` if available and otherwise fall back to Flask's development server.
- The trained model file is `traffic_predictor_model.pkl` and must be present in the repository root for the server to load the model at runtime.

Publishing badge
----------------

![Publish](https://github.com/lunifermoon89-ux/ai_robot_project/actions/workflows/publish-all.yml/badge.svg)

How to publish an image (recommended)

