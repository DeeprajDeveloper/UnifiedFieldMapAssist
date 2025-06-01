import config
import utilities.OTHER.transformer as transform
import utilities.DB.data_query as dq
import app.constants as const


def description_to_id(key_name, input_value):
    sql_query = const.MappingMatrix.DESCRIPTION_TO_CODE_QRY_MAPPING[key_name]
    data_response = dq.dql_fetch_one_row_for_one_input(database=config.SQLITE_DB, data_input=input_value, sql_script=sql_query)
    return data_response


template_name = rf"{const.FileSystemInformation.DATA_TEMPLATE_FOLDER}\{const.FileSystemInformation.DATA_TEMPLATE_FILENAME}"
input_dataframe = transform.xl_to_dataframe(input_excel_template_path=template_name, worksheet_name=const.TemplateInformation.WORKSHEET_NAME, excel_table_name=const.TemplateInformation.EXCEL_TABLE_NAME)

api_dataframe = input_dataframe[const.TemplateInformation.XL_COLUMNS_API]
gui_dataframe = input_dataframe[const.TemplateInformation.XL_COLUMNS_GUI]
flag_dataframe = input_dataframe[const.TemplateInformation.XL_COLUMNS_FLAGS]
row_dict = []

for gui_row in input_dataframe.itertuples(index=True):
    row_dict_item = {col: getattr(gui_row, col) for col in const.TemplateInformation.XL_COLUMNS_ALL}
    print(row_dict_item)



# for gui_row in gui_dataframe.itertuples(index=True):
#     row_dict_item = {col: getattr(gui_row, col) for col in const.TemplateInformation.XL_COLUMNS_GUI}
#     row_dict.append(row_dict_item)
#
# sql_scripts = []
# for idx in range(0, len(row_dict)):
#     sql_script = const.SQLInsert.DML_INSERT_GUI_INFO
#     for key, item in row_dict[idx].items():
#         query_data_key = str(const.MappingMatrix.XL_COLUMNS_KEYS_GUI_MAPPING[key]['sqlKey'])
#         data_item = item if key not in const.MappingMatrix.DESCRIPTION_TO_CODE_KEYS else description_to_id(key_name=key, input_value=item)
#         sql_script = sql_script.replace(query_data_key, str(data_item))
#     sql_scripts.append(sql_script)
# print(sql_scripts)


