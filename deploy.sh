#!/usr/bin/env bash
# Troque APP pelo nome unico (so letras minusculas, numeros e hifen)
APP="tarefas-api-SEUNOME"
RG="rg-tarefas-api"
LOCAL="brazilsouth"   # se o F1 nao estiver disponivel, tente eastus2

az login
az group create --name $RG --location $LOCAL
az appservice plan create --name plan-tarefas --resource-group $RG --sku F1 --is-linux
az webapp create --name $APP --resource-group $RG --plan plan-tarefas --runtime "PYTHON:3.12"
az webapp config set --name $APP --resource-group $RG \
  --startup-file "gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app"
az webapp config appsettings set --name $APP --resource-group $RG \
  --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

zip -r app.zip app.py requirements.txt
az webapp deploy --name $APP --resource-group $RG --src-path app.zip --type zip

echo "URL: https://$APP.azurewebsites.net/docs"
# Ao terminar a entrega: az group delete --name $RG --yes
