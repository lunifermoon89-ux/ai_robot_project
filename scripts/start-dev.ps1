# Activate venv and run the Flask app in development mode
if (-not (Test-Path -Path .venv)) {
    Write-Host "Creating virtual environment .venv..."
    python -m venv .venv
}

Write-Host "Activating venv and installing dev requirements..."
. .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt

Write-Host "Starting Flask development server (debug)..."
set "FLASK_APP=app.py"
set "FLASK_ENV=development"
python -m flask run --host=0.0.0.0 --port=8080
