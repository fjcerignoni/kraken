#!/bin/bash
set -euo pipefail

VERSION="0.1.0"
CONTAINER_NAME=kraken
IMAGE_NAME="${CONTAINER_NAME}-image:${VERSION}"
VOLUME_NAME="${CONTAINER_NAME}-db"

docker volume create --name "$VOLUME_NAME"

docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

docker build \
    --tag "$IMAGE_NAME" \
    .

docker run \
    --detach \
    --env-file=.env \
    --name "$CONTAINER_NAME" \
    --volume "$VOLUME_NAME":/opt/kraken/bot/db \
    --publish 8080:8080 \
    --restart unless-stopped \
    "$IMAGE_NAME"

echo "${IMAGE_NAME} running as '${CONTAINER_NAME}' (health: http://localhost:8080/health)"
