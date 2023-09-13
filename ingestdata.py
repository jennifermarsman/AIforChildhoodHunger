import openpyxl
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.common import AzureConflictHttpError

# Read data from Excel file
storage_table_name = 'stateeligibility'
excel_file = 'AI for Childhood Hunger - Gov Eligibility Sources.xlsx'
sheet_name = 'State-Territories'
partitionKey = "State"
CONNECTION_STRING = "<DefaultEndpointsProtocol=https;AccountName=accountname;AccountKey=key;EndpointSuffix=core.windows.net>"

def get_cell_value(cell):
   if cell is None:
      return None
   elif cell.hyperlink is not None:
      return clean(cell.hyperlink.target)
   else:
      return clean(cell.value)
   
def clean(val):
   if val is None:
      return None
   else:
      return str(val).strip()

workbook = openpyxl.load_workbook(excel_file, data_only=True)
sheet = workbook[sheet_name]
table_service = TableService(connection_string=CONNECTION_STRING)
row_number = 0
for cell in sheet.iter_rows(max_col=5):
     row_number += 1
     if row_number <= 2:
        continue
     rowKey = get_cell_value(cell[0])
     entity = {
        'PartitionKey': partitionKey,
        'RowKey': rowKey,
        'EligibilityWebsite': get_cell_value(cell[1]),
        'SnapScreener': get_cell_value(cell[2]),
        'EligibilityPDF': get_cell_value(cell[3]),
        'OnlineApplication': get_cell_value(cell[4])
     }
     try:
        print(f"Inserting data with PartitionKey={partitionKey} and RowKey={rowKey}")
        table_service.insert_entity(storage_table_name, entity)
     except AzureConflictHttpError as e:
        print(f"Data with PartitionKey={partitionKey} and RowKey={rowKey} already exists so updating..")
        table_service.update_entity(storage_table_name, entity)




