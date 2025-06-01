import utilities.ERROR.custom as cError
import openpyxl as pyxl
import pandas as pd


def transform_to_boolean(list_data_input):
    response_list: list = []
    if 0 in list_data_input or 1 in list_data_input:
        for item in list_data_input:
            response_list.append(True if item == 1 else False)
    else:
        raise cError.InvalidData(message='Expecting binary values 0/1')
    return response_list


def xl_to_dataframe(input_excel_template_path, worksheet_name, excel_table_name):
    try:
        xl_workbook = pyxl.load_workbook(filename=input_excel_template_path, data_only=True)
        xl_worksheet = xl_workbook[worksheet_name]
        xl_data_table = xl_worksheet.tables[excel_table_name]
        xl_table_range = xl_data_table.ref

        xl_table_data = []
        for row in xl_worksheet[xl_table_range]:
            xl_table_data.append([cell.value for cell in row])

        xl_headers = xl_table_data[0]
        xl_rows = xl_table_data[1:]

        pd_dataframe = pd.DataFrame(xl_rows, columns=xl_headers)
        return pd_dataframe
    except Exception as err:
        raise cError.PandasDataframeError(f'An error has occurred while transforming the Excel data template into a workable Pandas Dataframe. \nPlease see the error message: {str(err)}')

