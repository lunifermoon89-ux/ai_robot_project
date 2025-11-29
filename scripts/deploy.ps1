<#
Deployment helper script for Windows PowerShell.

USAGE:
1. Open PowerShell as a user with network access.
2. Edit the variables at the top of this file to set your GitHub owner/repo and optionally Docker Hub credentials.
3. Run: `.	asks\deploy.ps1` (or its path) from the repo root.

This script will:
- check prerequisites (git, gh, docker)
- optionally install `git` and `gh` via `winget` if missing
- initialize a git repo, commit, and create the GitHub repository via `gh`
- (optionally) set Docker Hub secrets in the GitHub repo
- (optionally) trigger the `publish-all.yml` workflow
#>

## === CONFIGURE THESE BEFORE RUNNING ===
$Owner = 'lunifermoon89-ux'
$Repo = 'ai_robot_project'
# Set DockerHub values if you want the script to add secrets (leave empty to skip)
$DockerHubUsername = ''
$DockerHubToken = ''

function Check-Command($cmd) {
    try {
        Get-Command $cmd -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

Write-Host "Checking prerequisites..."

if (-not (Check-Command git)) {
    Write-Host "git not found. You can install via: winget install --id Git.Git -e --source winget"
} else {
    git --version
}

if (-not (Check-Command gh)) {
    Write-Host "gh (GitHub CLI) not found. You can install via: winget install --id GitHub.cli -e --source winget"
} else {
    gh --version
}

if (-not (Check-Command docker)) {
    Write-Host "docker not found. Install Docker Desktop for Windows from https://www.docker.com/get-started"
} else {
    docker --version
}

Read-Host "Press Enter to continue (or Ctrl+C to abort)"

## Initialize git repo and push
if (-not (Test-Path .git)) {
    Write-Host "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: prepare deployable app"
    git branch -M main
} else {
    Write-Host ".git already exists; skipping init."
}

if (-not (Check-Command gh)) {
    Write-Host "gh CLI is not available; cannot create GitHub repo or set secrets. Install gh and re-run the script."
    exit 1
}

Write-Host "Creating GitHub repository (or verifying remote)..."
try {
    gh repo view $Owner/$Repo --json name --jq .name > $null 2>&1
    Write-Host "Repository already exists on GitHub: $Owner/$Repo"
    $remoteUrl = (gh repo view $Owner/$Repo --json url --jq .url)
    git remote remove origin -ErrorAction SilentlyContinue
    git remote add origin $remoteUrl
    git push -u origin main
} catch {
    Write-Host "Creating new repository on GitHub: $Owner/$Repo"
    gh repo create $Owner/$Repo --public --source=. --remote=origin --push
}

## Optionally add Docker Hub secrets
if ($DockerHubUsername -and $DockerHubToken) {
    Write-Host "Adding Docker Hub secrets to GitHub repository..."
    gh secret set DOCKERHUB_USERNAME --body $DockerHubUsername --repo $Owner/$Repo
    gh secret set DOCKERHUB_TOKEN --body $DockerHubToken --repo $Owner/$Repo
} else {
    Write-Host "Docker Hub credentials not configured in this script; skipping adding secrets."
}

## Trigger publish workflow
Write-Host "Triggering publish workflow (publish-all.yml)..."
gh workflow run publish-all.yml --repo $Owner/$Repo --ref main

Write-Host "Done. To check runs:"
Write-Host "  gh run list --repo $Owner/$Repo"
Write-Host "  gh run view <run-id> --repo $Owner/$Repo --log"

Write-Host "You can also build and run Docker locally:"
Write-Host "  docker build -t ai_robot_project:latest ."
Write-Host "  docker-compose up --build"

Write-Host "Deployment script finished."
