# Copilot / Agent Instructions — ai_robot_project

Short, actionable guidance to help AI coding agents be productive in this repository.

1) Big-picture architecture
- Purpose: lightweight ML pipeline for a single regression model that predicts a "Traffic_Score" from a simple feature set stored in `final_feature_set.csv`.
- Major components:
  - `train_model_h.py`: reads `final_feature_set.csv`, constructs a single feature `X_Feature` (using the DataFrame index), fits an OLS model using `statsmodels.api`, and saves the fitted `results` object via `joblib` to `traffic_predictor_model.pkl`.
  - `predict_traffic_i.py`: loads `traffic_predictor_model.pkl`, constructs a new input DataFrame with `X_Feature`, adds an intercept using `sm.add_constant`, and calls `results.predict(...)` to return a single Traffic Score.
  - Data flow: CSV (`final_feature_set.csv`) -> `train_model_h.py` -> saved model (`traffic_predictor_model.pkl`) -> `predict_traffic_i.py` for inference.

2) Key files and conventions to reference in code edits
- `final_feature_set.csv`: canonical cleaned dataset; training script expects a `Traffic_Score` column and uses the DataFrame index as the numeric feature `X_Feature`.
- `train_model_h.py`:
  - Uses `sm.add_constant(...)` to create the intercept term before fitting OLS.
  - Dumps the `results` object (the fitted `RegressionResults`) via `joblib.dump(results, MODEL_FILE)`.
  - Reports R-squared as the primary performance metric.
- `predict_traffic_i.py`:
  - Loads the entire `RegressionResults` object with `joblib.load(MODEL_FILE)` and calls `.predict(X_new)`.
  - Expects `X_new` to include the same columns (including the intercept) as were used in training.

3) Project-specific patterns and gotchas
- Single-feature model: training sets `df['X_Feature'] = df.index.values`. New features or changes to this pattern must be applied consistently in both training and prediction.
- Always include the intercept with `sm.add_constant(...)` before training and before prediction — omission will change model behavior.
- Model object type: `statsmodels` `RegressionResults` is saved and used directly; callers expect that object API (e.g., `.predict(...)`, `.rsquared`). Do not replace with a different object format without updating both scripts.
- Filenames are constants in the scripts (`CLEANED_FILE`, `MODEL_FILE`). When refactoring, update the constant rather than hardcoding new names in multiple places.
- Error/UX style: scripts print short emoji-prefixed status messages. Keep new CLI output compact and user-oriented.

4) How to run / reproduce locally (powershell)
Install dependencies (from repository root):
```powershell
python -m pip install --upgrade pip
python -m pip install pandas numpy statsmodels joblib
```
Train the model (writes `traffic_predictor_model.pkl`):
```powershell
python train_model_h.py
```
Run a simple prediction (uses `traffic_predictor_model.pkl`):
```powershell
python predict_traffic_i.py
```

5) Integration & external dependencies
- Uses Python packages: `pandas`, `numpy`, `statsmodels`, and `joblib` (no other external services).
- Data is local CSV files in the repo root. There are no network calls or DB integrations.

6) Editing guidance for AI agents (concise rules)
- Preserve the `sm.add_constant(...)` + `X_Feature` pattern unless you update both training and prediction scripts together and add tests/examples demonstrating equivalence.
- When changing file names for dataset or model, update the top-level constants (`CLEANED_FILE`, `MODEL_FILE`) rather than scattering string literals.
- Keep outputs human-readable (status lines + short interpretation). Follow the existing emoji-prefixed messages for consistency.
- If adding features or columns to the CSV, include a short example in `train_model_h.py` showing how features are constructed and how the input to `.predict(...)` should be built.

7) Tests & CI
- No automated tests or CI configuration found in the repository. If you add tests, place them in a `tests/` folder and use `pytest` for consistency.

8) Examples to reference when generating code
- Example: to add a new numeric feature `speed_limit` you would:
  1. Update `final_feature_set.csv` to include a `speed_limit` column.
  2. In `train_model_h.py` add `X = sm.add_constant(df[['X_Feature','speed_limit']])` and re-run training.
  3. In `predict_traffic_i.py` construct `new_data = pd.DataFrame({'X_Feature':[v], 'speed_limit':[s]})` then `X_new = sm.add_constant(new_data)` before `predict`.

9) When to ask the human
- Ask for clarification when changes touch the model persisted format, add/remove features, or change the meaning of `Traffic_Score` (because downstream consumers may rely on the numeric range or interpretation).

If anything important is missing or you'd like conventions tightened (tests, CI, Python version pinning), tell me what to add and I'll iterate.
