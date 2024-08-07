#/bin/bash

CONTAINER_NAME=kraken
IMAGE_NAME=$CONTAINER_NAME-image
VLOLUME_NAME=$CONTAINER_NAME-db

docker volume create --name $VOLUME_NAME

docker rm -f $CONTAINER_NAME

docker build \
    --tag $IMAGE_NAME \
    .

docker run \
    --detach \
    --env-file=.env \
    --name $CONTAINER_NAME \
    --volume $VOLUME_NAME:/opt/kraken/bot/db \
    --restart unless-stopped \
    $IMAGE_NAME
