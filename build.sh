#/bin/bash

CONTAINER_NAME=kraken
IMAGE_NAME=$CONTAINER_NAME-image

docker rm -f $CONTAINER_NAME

docker build \
    --tag $IMAGE_NAME \
    .

docker run \
    --detach \
    --env-file=.env \
    --name $CONTAINER_NAME \
    --volume kraken-db:/opt/kraken/bot/db \
    --restart unless-stopped \
    $IMAGE_NAME