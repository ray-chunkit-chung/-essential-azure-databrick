# essential-azure-databricks

essential-azure-databricks

https://learn.microsoft.com/en-us/azure/databricks/getting-started/

https://learn.microsoft.com/en-us/azure/templates/Microsoft.Databricks/workspaces?pivots=deployment-language-arm-template

https://learn.microsoft.com/en-us/cli/azure/deployment/group?view=azure-cli-latest

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
# az account set -s $SUBSCRIPTION
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


## Finally Delete resources

After experiment, delete all resources to avoid charging a lot of money

```bash
source .env
az group delete -y --name $RESOURCE_GROUP
```
