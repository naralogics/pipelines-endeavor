#!/bin/bash

if [ "$ENV_DAGSTER_MODE" == 'dagit' ]
then
    cp ../build/dagster.yaml $DAGSTER_HOME
    python ../build/dagster-database-setup.py

    mkdir -p ~/.aws
    echo "[${ENV_AWS_PROFILE}]" > ~/.aws/credentials
    echo "aws_access_key_id=${AWS_ACCESS_KEY_ID}" >> ~/.aws/credentials
    echo "aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}" >> ~/.aws/credentials
    echo "region=${ENV_AWS_REGION}" >> ~/.aws/credentials
    chmod 700 ~/.aws
    chmod 600 ~/.aws/credentials

    exec dagit --path-prefix=/pipelines --port "3000" --host 0.0.0.0 -f $ENV_DAGSTER_CATALOG_PATH

elif [ "$ENV_DAGSTER_MODE" == 'dagster-daemon' ]
then
    sleep 20

    mkdir -p ~/.aws
    echo "[${ENV_AWS_PROFILE}]" > ~/.aws/credentials
    echo "aws_access_key_id=${AWS_ACCESS_KEY_ID}" >> ~/.aws/credentials
    echo "aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}" >> ~/.aws/credentials
    echo "region=${ENV_AWS_REGION}" >> ~/.aws/credentials
    chmod 700 ~/.aws
    chmod 600 ~/.aws/credentials

    exec dagster-daemon run -f $ENV_DAGSTER_CATALOG_PATH

elif [ "$ENV_DAGSTER_MODE" == 'jupyter-lab' ]
then
    python -c "from jupyter_server.auth import passwd; pwd = passwd('$ENV_ENGINE_CLIENT_SECRET'); print(f'c.ServerApp.password = u\'{pwd}\'')" > ~/jupyter_server_config.py
    mkdir -p ~/.ipython/profile_default/startup
    cp ../build/jupyter-startup/* ~/.ipython/profile_default/startup/
    jupyter-lab --ip=0.0.0.0 --config ~/jupyter_server_config.py --allow-root --ServerApp.base_url=/jupyterlab

else
    echo "ENV_DAGSTER_MODE environment variable must have a value of \"dagit\", \"dagster-daemon\", or \"jupyter-lab\""
    exit 1
fi
