# AIforChildhoodHunger
Helping families in need access and navigate food programs and financial resources to reduce childhood hunger

## Setup
Run the following commands in the AIforChildhoodHunger directory.
```
pip install -r requirements.txt
python prototype.py
```
Create a .config file in the AIforChildhoodHunger directory and include the following values and replace the appropriate fields:
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
### Ingest Data for LLM
This step ingests the data from a spreadsheet to Azure Storage Database. To do so, add spreadsheet AI for Childhood Hunger - Gov Eligibility Sources.xlsx to AIforChildhoodHunger folder, then run python ingestdata.py