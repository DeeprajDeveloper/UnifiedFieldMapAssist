import app.constants as const
import utilities.DB.data_query as dq
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


def calculate_pages():
    record_count_per_page = const.GuiConfigInformation.CONFIG_KEY_VALUE_MAPPING['rowCountPerPage']
    record_count_total = dq.fetch_all_rows(database=config.SQLITE_DB, sql_script=const.QueriesRead.DQL_TBL_GUI_RECORD_COUNT, return_list=True)[0]
    page_count = math.ceil(int(record_count_total) / int(record_count_per_page))
    return page_count
