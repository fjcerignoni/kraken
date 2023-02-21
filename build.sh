#/bin/bash

CONTAINER_NAME=kraken
IMAGE_NAME=$CONTAINER_NAME-image

docker rm -f $CONTAINER_NAME

docker build \
    --tag $IMAGE_NAME \
    .

docker run \
    --detach \
    --name $CONTAINER_NAME \
    --volume $(pwd)/bot/db:/opt/kraken/bot/db \
    $IMAGE_NAME