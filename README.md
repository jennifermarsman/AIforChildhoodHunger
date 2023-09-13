# AIforChildhoodHunger
Helping families in need access and navigate food programs and financial resources to reduce childhood hunger

## Setup
```
pip install -r requirements.txt
python prototype.py
```
## Ingest Data from  spreadsheet to Azure Storage Database
Update CONNECTION_STRING variable in ingestdata.py with connection string to Azure Storage Database.
Add spreadsheet AI for Childhood Hunger - Gov Eligibility Sources.xlsx to AIforChildhoodHunger folder.
Run python ingestdata.py