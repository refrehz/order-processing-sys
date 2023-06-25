#!/bin/bash -ex

docker build -t app-test --target test .

docker run \
    --rm \
    -it \
    --network=host \
    app-test