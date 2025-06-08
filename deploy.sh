#!/bin/bash

# Configuration
APP_NAME="fruits-api-app"
RESOURCE_GROUP="fruits-api-rg"
RUNTIME="PYTHON:3.11"

echo "Checking app settings..."
az webapp config appsettings list \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

echo "Setting up app configuration..."
az webapp config appsettings set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    WEBSITES_PORT=8000 \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true \
    POST_BUILD_COMMAND="pip install -r requirements.txt"

echo "Deploying application..."
az webapp up \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --runtime $RUNTIME \
  --sku B1

echo "Setting startup command..."
az webapp config set \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --generic-configurations "{'customStartupCommand': 'gunicorn app.main:app --config gunicorn.conf.py'}"

echo "Restarting the app..."
az webapp restart \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

echo "Checking application logs..."
az webapp log tail \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP 