import app.constants as const
import utilities.DB.data_query as dq
import utilities.DB.data_manipulate as dm
import utilities.JSON.json_builder as jbuild
import utilities.OTHER.transformer as transform
import utilities.ERROR.custom as cust_err
import utilities.LOG.logger as cust_log
import config
import math


def return_all_mapping_information(return_json_response: bool = True):
    result_data: list = []
    response_data: list = []
    try:
        gui_ids_list = dq.fetch_all_rows(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_TBL_GUI_ALL_IDS, return_list=True)
        for gui_id in gui_ids_list:
            gui_information = dq.fetch_all_rows_for_one_input(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_VW_GUI_INFO, data_input=gui_id, return_list=True)
            gui_json_info = jbuild.json_builder_from_list(keys_list=const.APIKeysList.GUI_INFO_KEYS, data_list=gui_information, return_type='dictionary')

            api_information = dq.fetch_all_rows_for_one_input(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_VW_API_INFO, data_input=gui_id, return_list=True)
            api_json_info = jbuild.json_builder_from_list(keys_list=const.APIKeysList.API_INFO_KEYS, data_list=api_information, return_type='dictionary')

            db_information = dq.fetch_all_rows_for_one_input(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_VW_DB_INFO, data_input=gui_id, return_list=False)
            db_json_info = jbuild.json_builder_from_list(keys_list=const.APIKeysList.DB_MAPPING_KEYS, data_list=db_information, return_type='list')

            api_exposure_information = transform.transform_to_boolean(dq.fetch_all_rows_for_one_input(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_TBL_API_EXPOSURE_INFO, data_input=gui_id, return_list=True))
            api_exposure_json_info = jbuild.json_builder_from_list(keys_list=const.APIKeysList.API_EXPOSURE_KEYS, data_list=api_exposure_information, return_type='dictionary')

            result_data.append({'guiFieldIdentifier': gui_id, "guiInformation": gui_json_info, "apiInformation": api_json_info, "databaseInformation": db_json_info, "apiExposureFlags": api_exposure_json_info})

        if return_json_response:
            response_data = jbuild.response_template(success=True, display_error=False, status_code=200, data=result_data, message="Data Retrieval Completed.")
            return response_data
        else:
            return result_data
    except cust_err.CustomError as err:
        cust_log.log_message(level='error', message=f'call to endpoint /api/v1/readAll returned error {str(err)}', call_type='API')
        response_data = jbuild.response_template(success=False, display_error=True, status_code=400, error=err, message="An error has occurred. Please refer the errorInformation section for details.")
        return response_data


def return_get_config(search_parameter, return_json_response: bool = True):
    try:
        if search_parameter != "":
            if search_parameter not in const.APIKeysList.VALID_CONFIG_SEARCH_KEYS:
                raise cust_err.InvalidSearchParameter(f'Query parameter provided is not valid. Query Parameter Key: "searchParameter", Applicable Values: {const.APIKeysList.VALID_CONFIG_SEARCH_KEYS}')
            else:
                config_result_data = const.GuiConfigInformation.CONFIG_KEY_VALUE_MAPPING[search_parameter]
                result_data = jbuild.json_builder_from_list(keys_list=const.APIKeysList.CONFIG_KEYS, data_list=[search_parameter, config_result_data], return_type='dictionary')

            if return_json_response:
                response_data = jbuild.response_template(success=True, display_error=False, status_code=200, data=result_data, message="Data Retrieval Completed.")
                return response_data
            else:
                return result_data
        else:
            raise cust_err.InputMissing('A search parameter is expected to be provided. Please retry the operation.')
    except cust_err.CustomError as err:
        cust_log.log_message(level='error', message=f'call to endpoint /api/v1/getConfig returned error {str(err)}', call_type='API')
        response_data = jbuild.response_template(success=False, display_error=True, status_code=400, error=err, message="An error has occurred. Please refer the errorInformation section for details.")
        return response_data


def return_mapping_information_by_page(page_number: int, return_json_response: bool = True):
    result_data: list = []
    response_data: list = []
    try:

        if 1 <= page_number <= calculate_pages():
            record_count = const.GuiConfigInformation.CONFIG_KEY_VALUE_MAPPING['rowCountPerPage']
            range_start = ((page_number - 1) * record_count) + 1 if page_number > 1 else 1
            range_end = page_number * record_count
            gui_ids_list = dq.fetch_all_rows_for_range(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_TBL_GUI_RANGE_IDS, range_start=range_start, range_end=range_end, return_list=True)
            for gui_id in gui_ids_list:
                gui_information = dq.fetch_all_rows_for_one_input(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_VW_GUI_INFO, data_input=gui_id, return_list=True)
                gui_json_info = jbuild.json_builder_from_list(keys_list=const.APIKeysList.GUI_INFO_KEYS, data_list=gui_information, return_type='dictionary')

                api_information = dq.fetch_all_rows_for_one_input(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_VW_API_INFO, data_input=gui_id, return_list=True)
                api_json_info = jbuild.json_builder_from_list(keys_list=const.APIKeysList.API_INFO_KEYS, data_list=api_information, return_type='dictionary')

                db_information = dq.fetch_all_rows_for_one_input(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_VW_DB_INFO, data_input=gui_id, return_list=False)
                db_json_info = jbuild.json_builder_from_list(keys_list=const.APIKeysList.DB_MAPPING_KEYS, data_list=db_information, return_type='list')

                api_exposure_information = transform.transform_to_boolean(dq.fetch_all_rows_for_one_input(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_TBL_API_EXPOSURE_INFO, data_input=gui_id, return_list=True))
                api_exposure_json_info = jbuild.json_builder_from_list(keys_list=const.APIKeysList.API_EXPOSURE_KEYS, data_list=api_exposure_information, return_type='dictionary')

                result_data.append({'guiFieldIdentifier': gui_id, "guiInformation": gui_json_info, "apiInformation": api_json_info, "databaseInformation": db_json_info, "apiExposureFlags": api_exposure_json_info})

            if return_json_response:
                response_data = jbuild.response_template(success=True, display_error=False, status_code=200, data=result_data, message="Data Retrieval Completed.")
                return response_data
            else:
                return result_data
        else:
            raise cust_err.PageNumberOutOfRange(f'Maximum number of pages allowed is between 1 & {calculate_pages()}. Please correct the page number and retry the operation.')
    except cust_err.CustomError as err:
        cust_log.log_message(level='error', message=f'call to endpoint /api/v1/readAll returned error {str(err)}', call_type='API')
        response_data = jbuild.response_template(success=False, display_error=True, status_code=400, error=err, message="An error has occurred. Please refer the errorInformation section for details.")
        return response_data


def return_loading_data_to_db(data_file_name):
    input_file = rf"{const.FileSystemInformation.UPLOAD_FOLDER}\{data_file_name}"
    input_dataframe = transform.xl_to_dataframe(input_excel_template_path=input_file, worksheet_name=const.TemplateInformation.WORKSHEET_NAME, excel_table_name=const.TemplateInformation.EXCEL_TABLE_NAME)

    for df_idx in range(0, len(input_dataframe)):
        gui_dataframe = input_dataframe[const.TemplateInformation.XL_COLUMNS_GUI]
        api_dataframe = input_dataframe[const.TemplateInformation.XL_COLUMNS_API]
        flag_dataframe = input_dataframe[const.TemplateInformation.XL_COLUMNS_FLAGS]

        gui_insert_scripts = dataframe_to_db_insert(dataframe=gui_dataframe, dataframe_columns=const.TemplateInformation.XL_COLUMNS_GUI, insert_sql_script=const.SQLInsert.DML_INSERT_GUI_INFO, column_key_mapping=const.MappingMatrix.XL_COLUMNS_KEYS_GUI_MAPPING)
        for gui_idx in range(0, len(gui_insert_scripts)):
            dm.dml_execute_script(database=config.SQLITE_DB, sql_script=gui_insert_scripts[gui_idx])


def calculate_pages():
    record_count_per_page = const.GuiConfigInformation.CONFIG_KEY_VALUE_MAPPING['rowCountPerPage']
    record_count_total = dq.fetch_all_rows(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_TBL_GUI_RECORD_COUNT, return_list=True)[0]
    page_count = math.ceil(int(record_count_total) / int(record_count_per_page))
    return page_count


def description_to_id(key_name, input_value):
    sql_query = const.MappingMatrix.DESCRIPTION_TO_CODE_QRY_MAPPING[key_name]
    data_response = dq.dql_fetch_one_row_for_one_input(database=config.SQLITE_DB, data_input=input_value, sql_script=sql_query)
    return data_response


def dataframe_to_db_insert(dataframe, dataframe_columns, insert_sql_script, column_key_mapping):
    data_tuple_list = []
    for data_row in dataframe.itertuples(index=True):
        row_dict_item = {col: getattr(data_row, col) for col in dataframe_columns}
        data_row.append(row_dict_item)

    sql_scripts = []
    for idx in range(0, len(data_tuple_list)):
        sql_script = insert_sql_script
        for key, item in data_tuple_list[idx].items():
            query_data_key = str(column_key_mapping[key]['sqlKey'])
            data_item = item if key not in const.MappingMatrix.DESCRIPTION_TO_CODE_KEYS else description_to_id(key_name=key, input_value=item)
            sql_script = sql_script.replace(query_data_key, str(data_item))
        sql_scripts.append(sql_script)
    return sql_scripts

