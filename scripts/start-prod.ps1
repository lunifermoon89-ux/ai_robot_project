# Build Docker image and run via docker-compose (requires Docker installed)
Write-Host "Building Docker image..."
docker build -t ai_robot_project:latest .

Write-Host "Running container via docker-compose..."
docker-compose up -d --build

Write-Host "App should be available at http://localhost:8080"
