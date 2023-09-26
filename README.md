# AIforChildhoodHunger
Helping families in need access and navigate food programs and financial resources to reduce childhood hunger

## Ingest Data
To ingest the data from the trusted spreadsheet to Azure Storage Database, add spreadsheet AI for Childhood Hunger - Gov Eligibility Sources.xlsx to AIforChildhoodHunger folder.
```
python ingestdata.py
```

## Configure and Run Locally
In a .env file in the AIforChildhoodHunger directory, update the following values where appropriate.  You will definitely need to replace openai_endpoint, openai_api_key, and db_connection_string.  If Bing support is added, you will need to update bing_api_key.  You may need to update other fields as well.   

```python
# Constants for calling the Azure OpenAI service
openai_api_type = "azure"
openai_endpoint = "https://YOUR_AOAI_RESOURCE_NAME.openai.azure.com/"
openai_api_key = "<OpenAI Key>"
gpt_deployment_name = "gpt-35-turbo"

# Constants for Bing Search API
bing_endpoint = "https://api.bing.microsoft.com/v7.0/search"
bing_api_key = "<Bing Key>"

# Constants for Trusted Database
db_connection_string = "DefaultEndpointsProtocol=https;AccountName={ACCOUNTNAME};AccountKey={ACCOUNTKEY};EndpointSuffix=core.windows.net"
source_table = "stateeligibility"

```

Run the following commands in the AIforChildhoodHunger directory.
```
pip install -r requirements.txt
python hello.py
```

## Deployment
After you have tested locally, you can deploy to a website.  We will use Docker for this.  

1. Create an Azure Container Registry resource and note down the name you choose (you will need it in step 4): https://portal.azure.com/#create/Microsoft.ContainerRegistry

After creating this resource, you will also need to enable the admin user under the "Access Keys" section.  The username and password will be used in step 4 in the "docker login" command.  

2. Create an Azure web app: https://portal.azure.com/#create/Microsoft.WebSite

3. Download and launch [Docker Desktop](https://docs.docker.com/get-docker).  

4. Download and launch [Visual Studio Code](https://code.visualstudio.com/download).  Run the following commands in the Visual Studio Code terminal (replacing <NAME_FROM_STEP_1> with the actual name you used in step 1):

```
docker build -t sos-gradio-app .
docker run -it -d --name sos-app -p 7860:7860 -e GRADIO_SERVER_NAME=0.0.0.0 sos-gradio-app
docker login <NAME_FROM_STEP_1>.azurecr.io
docker tag sos-gradio-app <NAME_FROM_STEP_1>.azurecr.io/sos-gradio-app 
docker push <NAME_FROM_STEP_1>.azurecr.io/sos-gradio-app 
```

This is optional, but if you want to confirm what has been copied into the image, you can use this to launch an interactive shell and then use "ls" to check what's in the current directory:
```
docker run -it sos-gradio-app sh
```

5. Configure the web app that you created in step 2.  Navigate back to the App Service or Web App resource in the [Azure portal](https://portal.azure.com), and click on the "Deployment Center" section.  
+ Keep the Source as "Container Registry".  
+ Keep the Container type as "Single Container". 
+ Change the Registry source to "Azure Container Registry". 
+ Select the same Azure subscriptionID that you used in Step 1.  
+ Keep the Authentication as "Admin Credentials". 
+ Select the Registry that you created in step 1.  
+ Set the Image to "sos-gradio-app".  
+ Set the Tag to "latest".
+ Click "Save" at the top to save.  

Then, click the "Environment variables" section in the left-hand pane.  
+ Create an app setting with Name="WEBSITES_PORT" and Value="7860".  
+ Create an app setting with Name="GRADIO_SERVER_NAME" and Value="0.0.0.0".  
+ Click "Apply" to save.  

Then, click on the "App Service logs" section in the left-hand pane.  
+ Change "Application logging" from "Off" to "File system".  
+ Set the Quota and Retention period as appropriate.  
+ Click "Save" at the top to save.  docke

Finally, click the "Overview" section in the left-hand pane (it should be the top option).  Click on the "default domain" link and your app should be running!  