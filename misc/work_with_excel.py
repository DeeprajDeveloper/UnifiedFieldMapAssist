import openpyxl as pyxl
import app.constants as const
import pandas as pd
import pandasql as pdsql

ROOT_DIRECTORY = r"D:\Learn Python\UnifiedFieldMapAssist"
excel_document_name = fr"{ROOT_DIRECTORY}\{const.FileSystemInformation.DATA_TEMPLATE_FOLDER}\{const.FileSystemInformation.DATA_TEMPLATE_FILENAME}"
print(excel_document_name)

workbook = pyxl.load_workbook(filename=excel_document_name, data_only=True)
worksheet = workbook['DataEntry']
data_table = worksheet.tables['DataTable']
table_range = data_table.ref

data = []
for row in worksheet[table_range]:
    data.append([cell.value for cell in row])

headers = data[0]
rows = data[1:]

# print("Headers:", headers)
# print("First row:", rows[0])

df = pd.DataFrame(rows, columns=headers)
print(df.head())
print(df.columns)



