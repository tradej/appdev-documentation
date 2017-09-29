#!/usr/bin/env bash

if ! docker info; then
    if ! sudo docker info; then

        if ! sudo service docker start; then
            # Mac OS
            open -a --hide --background Docker
        else
            echo "Can not start the Docker daemon. Please start manually. Exiting..."
            exit 1
        fi
    fi
fi

if sudo CICO_LOCAL=1 ${SCRIPT_SRC}/../cico_build_deploy.sh; then
    sudo docker run -p 80:8080 -it appdev-documentation-deploy:latest
else
    echo Build Failed.
fi

