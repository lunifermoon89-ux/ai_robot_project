#!/usr/bin/env bash
set -euo pipefail

DOCKERHUB_USER="${DOCKERHUB_USER:-}"
DOCKERHUB_PASS="${DOCKERHUB_PASS:-}"
REPO="${DOCKERHUB_USER}/ai_robot_project"
TAG="${TAG:-latest}"

if [ -z "$DOCKERHUB_USER" ] || [ -z "$DOCKERHUB_PASS" ]; then
  echo "Set DOCKERHUB_USER and DOCKERHUB_PASS environment variables."
  exit 1
fi

IMAGE="$REPO:$TAG"

echo "Logging in to Docker Hub as $DOCKERHUB_USER"
echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin

echo "Building image: $IMAGE"
docker build -t "$IMAGE" .

echo "Pushing image: $IMAGE"
docker push "$IMAGE"

echo "Done. Image pushed: $IMAGE"
