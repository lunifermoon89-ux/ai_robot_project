param(
    [string]$DockerHubUser = $env:DOCKERHUB_USER,
    [string]$DockerHubPass = $env:DOCKERHUB_PASS,
    [string]$Repo = "$($env:DOCKERHUB_USER)/ai_robot_project",
    [string]$Tag = "latest"
)

if (-not $DockerHubUser) {
    Write-Error "Set DOCKERHUB_USER env var or pass -DockerHubUser"
    exit 1
}
if (-not $DockerHubPass) {
    Write-Error "Set DOCKERHUB_PASS env var or pass -DockerHubPass"
    exit 1
}

$Image = "$Repo:$Tag"
Write-Host "Building image: $Image"
docker build -t $Image .

Write-Host "Logging in to Docker Hub as $DockerHubUser"
# Pipe the password to docker login
$DockerHubPass | docker login --username $DockerHubUser --password-stdin

Write-Host "Pushing image: $Image"
docker push $Image

Write-Host "Done. Image pushed: $Image"
