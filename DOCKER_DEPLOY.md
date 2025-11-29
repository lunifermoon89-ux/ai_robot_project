DOCKER DEPLOY — ai_robot_project

This document explains how to push the project Docker image to Docker Hub locally or via GitHub Actions.

Prerequisites
- Docker installed and running locally.
- A Docker Hub account.
- (CI) GitHub repository with secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` set.

Local push (PowerShell)

```powershell
# set environment variables (example)
$env:DOCKERHUB_USER = "your-dockerhub-username"
$env:DOCKERHUB_PASS = "your-dockerhub-access-token"

# run the helper script (from repo root)
.
\scripts\push-docker.ps1 -DockerHubUser $env:DOCKERHUB_USER -DockerHubPass $env:DOCKERHUB_PASS
```

Local push (bash)

```bash
export DOCKERHUB_USER=your-dockerhub-username
export DOCKERHUB_PASS=your-dockerhub-access-token
./scripts/push-docker.sh
```

GitHub Actions
- Workflow file: `.github/workflows/docker-publish.yml`
- Configure repository secrets:
  - `DOCKERHUB_USERNAME`: your Docker Hub username
  - `DOCKERHUB_TOKEN`: a Docker Hub access token or password
- Push to `main` (or `master`) or run the workflow manually via "Actions" -> "Run workflow".

Image naming
- CI will push tags:
  - `DOCKERHUB_USERNAME/ai_robot_project:latest`
  - `DOCKERHUB_USERNAME/ai_robot_project:<commit-sha>`

Next steps / notes
- If your app requires `traffic_predictor_model.pkl` or other artifacts, ensure they're present in the repo or generated during image build.
- If you want multi-arch images, update `docker/build-push-action` `platforms:` setting in the workflow.
