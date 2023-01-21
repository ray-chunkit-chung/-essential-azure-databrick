# essential-azure-databricks

essential-azure-databricks using dockerhub desktop container dev env with vscode

 - <https://learn.microsoft.com/en-us/azure/databricks/getting-started/>

 - <https://learn.microsoft.com/en-us/azure/templates/Microsoft.Databricks/workspaces?pivots=deployment-language-arm-template>

 - <https://learn.microsoft.com/en-us/cli/azure/deployment/group?view=azure-cli-latest>

 - <https://learn.microsoft.com/en-us/azure/databricks/>

How to access azure storage from databricks by Service principles
<https://learn.microsoft.com/en-us/azure/databricks/external-data/azure-storage>

How to access azure storage from databricks by SAS
<https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview>

What is unity-catalog
<https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/get-started>

What is Streaming, auto load, delta lake
 - <https://www.databricks.com/spark/getting-started-with-apache-spark/streaming>

 - <https://docs.databricks.com/structured-streaming/production.html>

What is synapse
<https://docs.databricks.com/structured-streaming/synapse.html>

What are abfss vs wasbs
<https://docs.databricks.com/external-data/azure-storage.html>

How to read from different data sources
<https://learn.microsoft.com/en-us/azure/databricks/scenarios/databricks-connect-to-data-sources>

How to read from service bus
 - <https://stackoverflow.com/questions/70985859/moving-messages-received-from-azure-service-bus-to-azure-datalake-with-databrick>
 - <https://stackoverflow.com/questions/56078432/structured-streaming-with-azure-service-bus-topics>
 - <https://github.com/elastacloud/servicebusreceiver>

How to connect PowerBI using databrick queries
<https://learn.microsoft.com/en-us/azure/databricks/sql/get-started/user-quickstart>

## Step 1 Login azure

Install azure cli

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Set app variables by saving in .env file

```bash
export SUBSCRIPTION="xxx"
export TENANT="xxx"
export LOCATION="eastus"
export RESOURCE_GROUP="xxx"
export STORAGE_ACCOUNT="xxx"
export SKU_STORAGE="Standard_LRS"
export SERVICEBUS_NAMESPACE="xxx"
export SERVICEBUS_QUEUE="xxxx"
export SERVICEBUS_TOPIC="xxx"
export SERVICEBUS_SUBSCRIPTION="xx"
export COSMOS_NAME="xxx"
```

```bash
source .env
az login --tenant $TENANT
az account set -s $SUBSCRIPTION
```

## Step 2 Deploy databricks

```bash
az group create --subscription $SUBSCRIPTION \
                --name $RESOURCE_GROUP \
                --location $LOCATION
az deployment group create --subscription $SUBSCRIPTION \
                           --resource-group $RESOURCE_GROUP \
                           --name rollout01 \
                           --template-file ARMTemplate/Databricks/template.json \
                           --parameters ARMTemplate/Databricks/parameters.json
#                            --parameters @params.json \
#                            --parameters https://mysite/params.json \
#                            --parameters MyValue=This MyArray=@array.json
```

## Step 3 Login databricks to add users

Click Launch Workspace for the first time

![image](https://user-images.githubusercontent.com/26511618/213842664-ce48b51d-baa7-41c6-9f5e-607766171fa3.png)

<!-- ```bash
sudo apt-get install -y python3 python3-dev
sudo ln -sf /usr/bin/python3 /usr/bin/python
export PYTHONPATH=/usr/bin/python
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
``` -->

<!-- ```bash
az extension add --name databricks
``` -->

## Step 4 Deploy service bus and demo data

This is for creat

```bash
source .env
az deployment group create --subscription $SUBSCRIPTION \
                           --resource-group $RESOURCE_GROUP \
                           --name rollout01 \
                           --template-file ARMTemplate/ServiceBus/template.json \
                           --parameters ARMTemplate/ServiceBus/parameters.json
export PRIMARY_CONNECTION_STRING="$(az servicebus namespace authorization-rule keys list --resource-group $RESOURCE_GROUP --namespace-name $SERVICEBUS_NAMESPACE --name RootManageSharedAccessKey | jq '.primaryConnectionString' | tr -d '"')"
export SECONDARY_CONNECTION_STRING="$(az servicebus namespace authorization-rule keys list --resource-group $RESOURCE_GROUP --namespace-name $SERVICEBUS_NAMESPACE --name RootManageSharedAccessKey | jq '.secondaryConnectionString' | tr -d '"')"
```

Install python to run service bus demo data creation

```bash
sudo apt-get install -y python3 python3-dev python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

Send message to topic

```bash
source .env
python example/send_message_to_service_bus_topic.py
```

## Bonus A Integrate with azure event hubs

<https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/streaming-event-hubs>

<https://github.com/Azure/azure-event-hubs-spark/blob/master/README.md#latest-releases>

## Bonus B xxxx

<https://learn.microsoft.com/en-us/azure/event-grid/event-grid-event-hubs-integration>

## Bonus C Databricks example

- Create notebook <https://learn.microsoft.com/en-us/azure/databricks/getting-started/etl-quick-start>

- Auto Loader/Delta lake <https://learn.microsoft.com/en-us/azure/databricks/delta/>

- Gen2 and Blob Storage <https://learn.microsoft.com/en-us/azure/databricks/external-data/azure-storage>

- Service principle <https://learn.microsoft.com/en-us/azure/databricks/administration-guide/users-groups/service-principals>

- Structured-Streaming <https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/>

## Finally Delete resources

After experiment, delete all resources to avoid charging a lot of money

```bash
source .env
az group delete -y --name $RESOURCE_GROUP
```

There can be some managed resources to delete. Check them by

```bash
az group list --subscription $SUBSCRIPTION
```

Delete them by

```bash
source .env
az group delete --name $(az group list --subscription $SUBSCRIPTION | jq '.[].name' | tr -d '"')
```
