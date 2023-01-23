# essential-azure-databricks

essential-azure-databricks using dockerhub desktop container dev env with vscode

- <https://learn.microsoft.com/en-us/azure/databricks/getting-started/>
- <https://learn.microsoft.com/en-us/azure/templates/Microsoft.Databricks/workspaces?pivots=deployment-language-arm-template>
- <https://learn.microsoft.com/en-us/cli/azure/deployment/group?view=azure-cli-latest>
- <https://learn.microsoft.com/en-us/azure/databricks/>
- Databrick cli

How to access azure storage from databricks by Service principles

- <https://learn.microsoft.com/en-us/azure/databricks/security/aad-storage-service-principal>
- <https://learn.microsoft.com/en-us/azure/databricks/external-data/azure-storage>
- <https://learn.microsoft.com/en-us/azure/databricks/sql/admin/data-access-configuration>
- <https://learn.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes>

How to access azure storage from databricks by SAS

- <https://docs.databricks.com/external-data/azure-storage.html>
- <https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview>

Azure Vault, RBAC permissions model, Multitenancy best practices

- <https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide?tabs=azure-cli>
- <https://learn.microsoft.com/en-us/azure/key-vault/general/best-practices>
- <https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/key-vault>

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

### Step 1.1 Create a service principle

<https://learn.microsoft.com/en-us/azure/databricks/security/aad-storage-service-principal>

Login portal > Azure Active Directory > New > App registration > Add client secret

### Step 1.2 Add the service principle to a subscription

sSubscription > Access control (IAM) > Role Assignment > Contributor > Select member > Search the app name

### Step 1.3 Set app variables

Save the following variables in .env file

```bash
export SUBSCRIPTION="xxx"
export APP_ID="xxxx"
export SECRET_VALUE="xxxxx"
export TENANT_ID="xxxxx"
export LOCATION="eastus"
export RESOURCE_GROUP="xxx"
export STORAGE_ACCOUNT="xxx"
export SKU_STORAGE="Standard_LRS"
export SERVICEBUS_NAMESPACE="xxx"
export SERVICEBUS_QUEUE="xxxx"
export SERVICEBUS_TOPIC="xxx"
export SERVICEBUS_SUBSCRIPTION="xx"
export COSMOS_NAME="xxx"
export DATABRICKS_WORKSPACE="xxx"
export DATABRICKS_SECRET_SCOPE="xxxx"
export KEYVAULT_NAME="xxxx"
```

### Step 1.4 Install azure cli and login

```bash
source .env
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# az login --tenant $TENANT
az login --service-principal -u $APP_ID -p $SECRET_VALUE --tenant $TENANT_ID
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

## Step 4 Access demo data in service bus from databricks

### Step 4.1 Deploy service bus

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

### Step 4.2 Install python to create demo data in service bus

```bash
sudo apt-get install -y python3 python3-dev python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Step 4.2 Send data to service bus topic

```bash
source .env
python example/send_message_to_service_bus_topic.py
```

PRIMARY_CONNECTION_STRING is required.

### Step 4.3 xxxx

## Step5 Access demo data in storage from databricks

<https://learn.microsoft.com/en-us/azure/databricks/security/aad-storage-service-principal>

### Step5.1 Create a key vault for cross-resource access

```bash
source .env
az keyvault create --location $LOCATION --name $KEYVAULT_NAME --resource-group $RESOURCE_GROUP
az keyvault set-policy --name $KEYVAULT_NAME --key-permissions all --spn $APP_ID
```

### Step5.2 Install databricks-cli

Create an Azure Key Vault-backed secret scope using the Databricks CLI

- <https://learn.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes>
- <https://learn.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/aad/user-aad-token>
- <https://learn.microsoft.com/en-us/azure/databricks/sql/admin/data-access-configuration>

Install databricks-cli

```bash
pip install --upgrade databricks-cli
az extension add --name databricks
```

Configure databricks cli by adding Azure AD token (AAD_TOKEN) for users using the Azure CLI. Do not change 2ff814a6-3304-4ab8-85cb-cd0e6f879c1d, as it is the app id of databricks software itself.

```bash
# Get config values
export DATABRICKS_AAD_TOKEN=$(az account get-access-token \
--resource 2ff814a6-3304-4ab8-85cb-cd0e6f879c1d \
--query "accessToken")
export WORKSPACE_ID=$(az databricks workspace show --name $DATABRICKS_WORKSPACE --resource-group $RESOURCE_GROUP | jq '.workspaceId' | tr -d '"')
export WORKSPACE_URL="https://$(az databricks workspace show --name $DATABRICKS_WORKSPACE --resource-group $RESOURCE_GROUP | jq '.workspaceUrl' | tr -d '"')"

# Check values
echo $DATABRICKS_AAD_TOKEN
echo $WORKSPACE_ID
echo $WORKSPACE_URL

# Configure databricks cli
source .venv/bin/activate
echo $WORKSPACE_URL | databricks configure --aad-token
```

### Step5.3 Create key-vault backed secret scope for storage access

Create databricks workspace secret scope backed by Azure key vault that we will add the service principle client secret into

```bash
# Get config values
export KEYVAULT_RESOURCE_ID=$(az keyvault show --name $KEYVAULT_NAME --resource-group $RESOURCE_GROUP  | jq '.id' | tr -d '"')
export KEYVAULT_DNS="https://$KEYVAULT_NAME.vault.azure.net/"

# Check values
echo $KEYVAULT_RESOURCE_ID
echo $KEYVAULT_DNS

databricks secrets create-scope --scope $DATABRICKS_SECRET_SCOPE --scope-backend-type AZURE_KEYVAULT --resource-id $KEYVAULT_RESOURCE_ID --dns-name $KEYVAULT_DNS --initial-manage-principal users
```

TODO: debug
```bash
Error: b'<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>\n<title>Error 400 io.jsonwebtoken.security.SignatureException: JWT signature does not match locally computed signature. JWT validity cannot be asserted and should not be trusted.</title>\n</head>\n<body><h2>HTTP ERROR 400</h2>\n<p>Problem accessing /api/2.0/secrets/scopes/create. Reason:\n<pre>    io.jsonwebtoken.security.SignatureException: JWT signature does not match locally computed signature. JWT validity cannot be asserted and should not be trusted.</pre></p>\n</body>\n</html>\n'
```

### Step 5.4 Direct access using ABFS URI for Blob Storage or Azure Data Lake Storage Gen2

```python
# Configure authentication
service_credential = dbutils.secrets.get(scope="<scope>",key="<service-credential-key>")
spark.conf.set("fs.azure.account.auth.type.<storage-account>.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.<storage-account>.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.<storage-account>.dfs.core.windows.net", "<application-id>")
spark.conf.set("fs.azure.account.oauth2.client.secret.<storage-account>.dfs.core.windows.net", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.<storage-account>.dfs.core.windows.net", "https://login.microsoftonline.com/<directory-id>/oauth2/token")

# Read Databricks Dataset IoT Devices JSON
df = spark.read.json("/databricks-datasets/iot/iot_devices.json")

# Write Delta table to external path
df.write.save("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<path-to-data>")


# List filesystem
dbutils.fs.ls("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<path-to-data>")

# Read IoT Devices JSON from ADLS Gen2 filesystem
df2 = spark.read.load("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<path-to-data>")
display(df2)
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
