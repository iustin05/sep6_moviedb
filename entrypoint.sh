#!/bin/sh

if [ "$DEPLOYMENT_ENV" = "production" ]
then
    export APP_SETTINGS=config.ProductionConfig
else
    export APP_SETTINGS=config.DevelopmentConfig
fi

exec python run.py