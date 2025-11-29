# Release Draft

Version: v1.0.0

Highlights
- Initial deployable release: training, prediction API, Docker image, CI, and publish workflows.

Changes
- Add Flask API with `/predict`, `/health`, `/ready`, `/metrics`, and `/docs`.
- Add Dockerfile and docker-compose for containerized deployment.
- Add CI tests, publish workflows for GHCR and Docker Hub.

Notes
- To publish images automatically, add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets to the repository.

Changelog
- initial: created basic model training and prediction, API, containerization, and CI.
