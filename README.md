# essential-azure-databricks

essential-azure-databricks

https://learn.microsoft.com/en-us/azure/databricks/getting-started/

https://learn.microsoft.com/en-us/azure/templates/Microsoft.Databricks/workspaces?pivots=deployment-language-arm-template

https://learn.microsoft.com/en-us/cli/azure/deployment/group?view=azure-cli-latest

https://learn.microsoft.com/en-us/azure/databricks/

using dockerhub desktop container dev env with vscode

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

image.png

**(Optional)** Warm up by studying the following:

 - Create notebook https://learn.microsoft.com/en-us/azure/databricks/getting-started/etl-quick-start

 - Auto Loader/Delta lake https://learn.microsoft.com/en-us/azure/databricks/delta/

 - Gen2 and Blob Storage https://learn.microsoft.com/en-us/azure/databricks/external-data/azure-storage

 - Service principle https://learn.microsoft.com/en-us/azure/databricks/administration-guide/users-groups/service-principals

 - Structured-Streaming https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/

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


## Bonus A Integrate with azure event hubs

https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/streaming-event-hubs


## Bonus B xxxx

https://learn.microsoft.com/en-us/azure/event-grid/event-grid-event-hubs-integration


## Finally Delete resources

After experiment, delete all resources to avoid charging a lot of money
```bash
source .env
az group delete -y --name $RESOURCE_GROUP
```

There can be more managed resources to delete. Check them by
```bash
az group list --subscription $SUBSCRIPTION
```

Delete them by
```bash
source .env
az group delete --name $(az group list --subscription $SUBSCRIPTION | jq '.[].name' | tr -d '"')
```