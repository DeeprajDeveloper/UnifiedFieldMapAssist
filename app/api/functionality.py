import math
from typing import Union
import app.constants as const
import config
import utilities.custom_app_logger as cust_log
import utilities.data_transformer as transform
from utilities import database_operations as db, json_response_builder as jbuild, custom_app_error as obj_error


def read_config(input_json_request, return_json_response: bool = True) -> Union[list, dict]:
    """
    The purpose of this function is to return configuration information.
    :param input_json_request: expected query parameters from request object
    :param return_json_response: boolean. indicates whether the return value is a JSON or not
    :return: returns a json response
    """
    try:
        search_parameter = input_json_request.args.get('searchParameter')
        obj_qry = db.QueryInformation(database=config.SQLITE_DB)
        # Static search keys from DB config table
        config_search_param = {'searchValue': search_parameter}
        config_api_resp_param = {'category': 'apiResponseKeys', 'paramKey': 'configInfoKeyList'}
        # Get config-details from DB
        valid_search_parameters = obj_qry.get_rows(sql_script=const.QryGetConfiguration.TABLE_GET_ALL_PARAM_KEYS)

        if search_parameter not in [None, ""]:
            if search_parameter not in valid_search_parameters:
                raise obj_error.InvalidSearchParameter(f'Query parameter provided is not valid. Query Parameter Key: "searchParameter", Applicable Values: {valid_search_parameters}')
            else:
                config_result_data = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_INFO_BY_PARAM_KEY, data_parameters=config_search_param)
                config_api_response_keys = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=config_api_resp_param, return_list=True)[0].split(',')
                result_data = jbuild.json_from_key_list(keys_list=config_api_response_keys, data_list=config_result_data, return_type='dict')
        else:
            config_result_data = obj_qry.get_rows(sql_script=const.QryGetConfiguration.TABLE_GET_ALL_INFO, return_list=False)
            config_api_response_keys = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=config_api_resp_param, return_list=True)[0].split(',')
            result_data = jbuild.json_from_key_list(keys_list=config_api_response_keys, data_list=config_result_data, return_type='list')

        if return_json_response:
            response_data = jbuild.build_response(success=True, message="Data retrieved successfully.", data=result_data)
            return response_data
        else:
            return config_result_data

    except obj_error.ErrorClass as err:
        cust_log.log_message(level='error', message=f'call to endpoint /api/v1/getConfig returned error {str(err)}', call_type='API')
        response_data = jbuild.build_response(success=False, message="Error retrieving data. Please see the error message.", status_code=400, error=err, display_error=True)
        return response_data


def update_config(parameter_id, update_payload):
    """
    The purpose of this function is to update config information in the database
    :param parameter_id: expected parameterId in the endpoint
    :param update_payload: Payload containing data to be updated.
    :return: returns a JSON response after the update.
    """
    try:
        obj_qry = db.QueryInformation(database=config.SQLITE_DB)
        obj_check = db.CheckIf(database=config.SQLITE_DB)
        obj_updt = db.DataManipulation(database=config.SQLITE_DB)
        read_data_sql_param = {'searchValue': parameter_id}

        if obj_check.data_exists(sql_script=const.QryGetConfiguration.TABLE_GET_INFO_BY_PARAMID, data_parameter=read_data_sql_param):
            update_payload_keys = list(update_payload.keys())
            # Static search keys from DB config table
            mandatory_sql_search_param = {'searchValue': 'configUpdate'}
            mandatory_payload_keys = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_UPDATE_PAYLOAD_KEYS, data_parameters=mandatory_sql_search_param, return_list=True)[0].split(',')
            if update_payload_keys.sort() != mandatory_payload_keys.sort():
                raise obj_error.MissingMandatoryKeys(message='Payload is missing mandatory keys. Please validate the payload and retry the operation.')
            else:
                action = update_payload.get('action')
                param_value_obj = update_payload.get('configParameterValue')
                if action != 'U':
                    raise obj_error.InvalidOperation(message='The action you are trying to perform is not allowed. Please verify the action and retry the operation.')
                else:
                    if list(param_value_obj.keys()) != ['oldValue', 'newValue']:
                        raise obj_error.MissingInput('Payload is expected to have oldValue & newValue to perform the operation.')
                    else:
                        param_old_value = param_value_obj.get('oldValue')
                        param_new_value = param_value_obj.get('newValue')
                        curr_val_sql_search = {'searchValue': parameter_id}
                        current_db_value = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAMID, data_parameters=curr_val_sql_search, return_list=True)[0]
                        if current_db_value != param_old_value:
                            raise obj_error.ValueMismatch(message="Provided oldValue & current value in the database does not match. Please verify the oldValue and retry the operation.")
                        else:
                            update_data_sql_param = {'updateValue': param_new_value, 'paramId': parameter_id}
                            obj_updt.update_data_with_param(sql_script=const.DataUpdateStatement.UPDATE_CONFIG_BY_PARAMID, data_parameters=update_data_sql_param)

                            config_api_resp_param = {'category': 'apiResponseKeys', 'paramKey': 'configInfoKeyList'}
                            config_result_data = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_INFO_BY_PARAMID, data_parameters=read_data_sql_param)
                            config_api_response_keys = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=config_api_resp_param, return_list=True)[0].split(',')
                            updated_result_data = jbuild.json_from_key_list(keys_list=config_api_response_keys, data_list=config_result_data, return_type='dict')

                            response_data = jbuild.build_response(success=True, message="Data Updated successfully.", data=updated_result_data)
                            return response_data
        else:
            raise obj_error.NoContent('The provided parameterId is missing. Please verify the parameterId and retry the operation.')
    except obj_error.ErrorClass as err:
        cust_log.log_message(level='error', message=f'call to endpoint /api/v1/updateConfig returned error {str(err)}', call_type='API')
        response_data = jbuild.build_response(success=False, message="Error retrieving data. Please see the error message.", status_code=400, error=err, display_error=True)
        return response_data


def read_mapping_information(input_request_json, return_json_response: bool = True):
    """
    The purpose of this function is to return mapping information.
    :param input_request_json: expected query parameters from request object containing pageNumber.
    :param return_json_response: boolean. indicates whether the return value is a JSON or not
    :return: returns a json response
    """
    result_data: list = []
    response_data: list = []

    gui_key_sql_param = {'category': 'apiResponseKeys', 'paramKey': 'guiInfoKeyList'}
    api_key_sql_param = {'category': 'apiResponseKeys', 'paramKey': 'apiInfoKeyList'}
    db_key_sql_param = {'category': 'apiResponseKeys', 'paramKey': 'dbInfoKeyList'}
    flag_key_sql_param = {'category': 'apiResponseKeys', 'paramKey': 'flagInfoKeyList'}

    try:
        obj_qry = db.QueryInformation(database=config.SQLITE_DB)

        gui_resp_keys = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=gui_key_sql_param, return_list=True)[0].split(',')
        api_resp_keys = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=api_key_sql_param, return_list=True)[0].split(',')
        db_resp_keys = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=db_key_sql_param, return_list=True)[0].split(',')
        flag_resp_keys = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=flag_key_sql_param, return_list=True)[0].split(',')

        if input_request_json.args.get('pageNumber') is None:
            gui_ids_list = obj_qry.get_rows(sql_script=const.QryGetGuiInfo.TABLE_GET_ALL_IDS, return_list=False)
        elif 1 <= int(input_request_json.args.get('pageNumber')) <= _calculate_pages():
            page_number = int(input_request_json.args.get('pageNumber'))
            rec_count_param = {'category': 'dataConfig', 'paramKey': 'rowCountPerPage'}
            record_count_per_page = int(obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=rec_count_param)[0])
            range_start = ((page_number - 1) * record_count_per_page) + 1 if page_number > 1 else 1
            range_end = page_number * record_count_per_page
            gui_id_sql_param = {'startValue': range_start, 'endValue': range_end}
            gui_ids_list = obj_qry.get_rows_with_param(sql_script=const.QryGetGuiInfo.TABLE_GET_ALL_IDS_BTW_RANGE, data_parameters=gui_id_sql_param, return_list=False)
        else:
            raise obj_error.PageNumberOutOfRange(f'Page number is out of range. Minimum = 1 / Maximum = {_calculate_pages()}.')

        for gui_id in gui_ids_list:
            gui_id_sql_param = {'searchValue': gui_id[0]}
            gui_information = obj_qry.get_rows_with_param(sql_script=const.QryGetGuiInfo.VIEW_GET_INFO_BY_ID, data_parameters=gui_id_sql_param, return_list=True)
            api_information = obj_qry.get_rows_with_param(sql_script=const.QryGetApiInfo.VIEW_GET_INFO_BY_GUI_ID, data_parameters=gui_id_sql_param, return_list=True)
            db_information = obj_qry.get_rows_with_param(sql_script=const.QryGetDbInfo.VIEW_GET_INFO_BY_GUI_ID, data_parameters=gui_id_sql_param, return_list=True)
            flag_information = transform.transform_to_boolean(obj_qry.get_rows_with_param(sql_script=const.QryGetFlagsInfo.TABLE_GET_INFO_BY_GUI_ID, data_parameters=gui_id_sql_param, return_list=True))

            gui_resp_json_info = jbuild.json_from_key_list(keys_list=gui_resp_keys, data_list=gui_information, return_type='dict')
            api_json_info = jbuild.json_from_key_list(keys_list=api_resp_keys, data_list=api_information, return_type='dict')
            db_json_info = jbuild.json_from_key_list(keys_list=db_resp_keys, data_list=db_information, return_type='dict')
            flag_json_info = jbuild.json_from_key_list(keys_list=flag_resp_keys, data_list=flag_information, return_type='dict')

            result_data.append({'guiFieldIdentifier': gui_id[0], "guiInformation": gui_resp_json_info, "apiInformation": api_json_info, "databaseInformation": db_json_info, "apiExposureFlags": flag_json_info})

        if return_json_response:
            response_data = jbuild.build_response(success=True, message="Data retrieved successfully.", data=result_data)
            return response_data
        else:
            return result_data
    except obj_error.ErrorClass as err:
        cust_log.log_message(level='error', message=f'call to endpoint /api/v1/getMapping returned error {str(err)}', call_type='API')
        response_data = jbuild.build_response(success=False, message="Error retrieving data. Please see the error message.", status_code=400, error=err, display_error=True)
        return response_data


def update_mapping_information(query_parameters, update_payload):
    """
    The purpose of this function is to update mapping information.
    :param query_parameters:
    :param update_payload:
    :return: returns a json response
    """
    result_data: list = []
    response_data: list = []

    query_param_sql_param = {'category': 'queryParams', 'paramKey': 'mappingUpdate'}
    entity_type_sql_param = {'category': 'dataConfig', 'paramKey': 'entityTypes'}

    try:
        obj_qry = db.QueryInformation(database=config.SQLITE_DB)
        obj_chk = db.CheckIf(database=config.SQLITE_DB)
        obj_updt = db.DataManipulation(database=config.SQLITE_DB)

        valid_query_param_keys = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=query_param_sql_param, return_list=True)[0].split(',')
        valid_entity_types = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=entity_type_sql_param, return_list=True)[0].split(',')
        input_query_param_keys = list(query_parameters.keys())

        if input_query_param_keys.sort() != valid_query_param_keys.sort():
            raise obj_error.MissingMandatoryKeys('One or more mandatory parameters are missing. Please make sure to send in all the required parameters.')
        else:
            identifier_value = int(query_parameters.args.get('identifier'))
            entity_type_value = query_parameters.args.get('entityType')

            if entity_type_value not in valid_entity_types:
                raise obj_error.InvalidSearchParameter(f'entityType provided is not valid. Acceptable values: {valid_entity_types}')
            else:
                if entity_type_value == 'gui':
                    _perform_mapping_update(entity_type_value=entity_type_value, update_payload=update_payload, identifier_value=identifier_value, obj_chk=obj_chk, obj_qry=obj_qry, obj_updt=obj_updt)
                elif entity_type_value == 'api':
                    _perform_mapping_update(entity_type_value=entity_type_value, update_payload=update_payload, identifier_value=identifier_value, obj_chk=obj_chk, obj_qry=obj_qry, obj_updt=obj_updt)
                elif entity_type_value == 'db':
                    _perform_mapping_update(entity_type_value=entity_type_value, update_payload=update_payload, identifier_value=identifier_value, obj_chk=obj_chk, obj_qry=obj_qry, obj_updt=obj_updt)
                elif entity_type_value == 'flag':
                    _perform_mapping_update(entity_type_value=entity_type_value, update_payload=update_payload, identifier_value=identifier_value, obj_chk=obj_chk, obj_qry=obj_qry, obj_updt=obj_updt)
                else:
                    raise obj_error.InvalidPayload('Provided entityType is not valid. Acceptable values: gui/api/db/flag')
        return None
    except obj_error.ErrorClass as err:
        cust_log.log_message(level='error', message=f'call to endpoint /api/v1/updateMapping returned error {str(err)}', call_type='API')
        response_data = jbuild.build_response(success=False, message="Error retrieving data. Please see the error message.", status_code=400, error=err, display_error=True)
        return response_data


def add_mapping_information(input_request_form, component_type):
    response_data = []
    result_list = {}
    data_key_value_list = {}
    try:
        display_dev_info = input_request_form.headers['displayDevInfo']
        obj_qry = db.QueryInformation(database=config.SQLITE_DB)
        input_form_keys = list(input_request_form.form)

        if component_type == 'all':
            valid_keys_sql_param = {'category': 'validKeys', 'paramKey': f'uiTagNamesForGUI'}
            valid_form_keys_list = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=valid_keys_sql_param, return_list=True)[0].split(',')
            component_type_override= 'gui'
            result_list['guiSqlParameters'] = _generate_data_sql_parameters(
                component_type=component_type_override
                , obj_qry=obj_qry
                , mapping_sql_query=const.QryMappingMatrix.MATRIX_UI_TAG_SQL_QUERY[component_type_override]
                , input_request_form=input_request_form
                , display_dev_info=display_dev_info
                , input_form_keys=input_form_keys
                , valid_keys_sql_param=valid_keys_sql_param
                , valid_form_keys_list=valid_form_keys_list
            )

            valid_keys_sql_param = {'category': 'validKeys', 'paramKey': f'uiTagNamesForAPI'}
            valid_form_keys_list = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=valid_keys_sql_param, return_list=True)[0].split(',')
            component_type_override = 'api'
            result_list['apiSqlParameters'] = _generate_data_sql_parameters(
                component_type=component_type_override
                , obj_qry=obj_qry
                , mapping_sql_query=const.QryMappingMatrix.MATRIX_UI_TAG_SQL_QUERY[component_type_override]
                , input_request_form=input_request_form
                , display_dev_info=display_dev_info
                , input_form_keys=input_form_keys
                , valid_keys_sql_param=valid_keys_sql_param
                , valid_form_keys_list=valid_form_keys_list
            )

            valid_keys_sql_param = {'category': 'validKeys', 'paramKey': f'uiTagNamesForDB'}
            valid_form_keys_list = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=valid_keys_sql_param, return_list=True)[0].split(',')
            component_type_override = 'db'
            result_list['dbSqlParameters'] = _generate_data_sql_parameters(
                component_type=component_type_override
                , obj_qry=obj_qry
                , mapping_sql_query=const.QryMappingMatrix.MATRIX_UI_TAG_SQL_QUERY[component_type_override]
                , input_request_form=input_request_form
                , display_dev_info=display_dev_info
                , input_form_keys=input_form_keys
                , valid_keys_sql_param=valid_keys_sql_param
                , valid_form_keys_list=valid_form_keys_list
            )

            valid_keys_sql_param = {'category': 'validKeys', 'paramKey': f'uiTagNamesForFLAG'}
            valid_form_keys_list = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=valid_keys_sql_param, return_list=True)[0].split(',')
            component_type_override = 'flag'
            result_list['flagSqlParameters'] = _generate_data_sql_parameters(
                component_type=component_type_override
                , obj_qry=obj_qry
                , mapping_sql_query=const.QryMappingMatrix.MATRIX_UI_TAG_SQL_QUERY[component_type_override]
                , input_request_form=input_request_form
                , display_dev_info=display_dev_info
                , input_form_keys=input_form_keys
                , valid_keys_sql_param=valid_keys_sql_param
                , valid_form_keys_list=valid_form_keys_list
            )
            return result_list
        else:
            valid_keys_sql_param = {'category': 'validKeys', 'paramKey': f'uiTagNamesFor{component_type.upper()}'}
            valid_form_keys_list = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=valid_keys_sql_param, return_list=True)[0].split(',')
            mapping_sql_query = const.QryMappingMatrix.MATRIX_UI_TAG_SQL_QUERY[component_type]
            result_list = _generate_data_sql_parameters(
                component_type=component_type
                , obj_qry=obj_qry
                , mapping_sql_query=mapping_sql_query
                , input_request_form=input_request_form
                , display_dev_info=display_dev_info
                , input_form_keys=input_form_keys
                , valid_keys_sql_param=valid_keys_sql_param
                , valid_form_keys_list=valid_form_keys_list
            )
            return result_list

    except obj_error.ErrorClass as err:
        cust_log.log_message(level='error', message=f'call to endpoint /api/v1/addMapping returned error {str(err)}', call_type='API')
        response_data = jbuild.build_response(success=False, message="Error retrieving data. Please see the error message.", status_code=400, error=err, display_error=True)
        return response_data


def return_loading_data_to_db(data_file_name):
    input_file = rf"{const.FileSystemInformation.UPLOAD_FOLDER}\{data_file_name}"
    input_dataframe = transform.xl_to_dataframe(input_excel_template_path=input_file, worksheet_name=const.TemplateInformation.WORKSHEET_NAME, excel_table_name=const.TemplateInformation.EXCEL_TABLE_NAME)

    for df_idx in range(0, len(input_dataframe)):
        gui_dataframe = input_dataframe[const.TemplateInformation.XL_COLUMNS_GUI]
        api_dataframe = input_dataframe[const.TemplateInformation.XL_COLUMNS_API]
        flag_dataframe = input_dataframe[const.TemplateInformation.XL_COLUMNS_FLAGS]

        gui_insert_scripts = _dataframe_to_db_insert(dataframe=gui_dataframe, dataframe_columns=const.TemplateInformation.XL_COLUMNS_GUI, insert_sql_script=const.SQLInsert.DML_INSERT_GUI_INFO, column_key_mapping=const.MappingMatrix.XL_COLUMNS_KEYS_GUI_MAPPING)
        for gui_idx in range(0, len(gui_insert_scripts)):
            dm.dml_execute_script(database=config.SQLITE_DB, sql_script=gui_insert_scripts[gui_idx])


def _calculate_pages():
    obj_qry = db.QueryInformation(database=config.SQLITE_DB)
    rec_count_param = {'category': 'dataConfig', 'paramKey': 'rowCountPerPage'}
    record_count_per_page = obj_qry.get_rows_with_param(sql_script=const.QryGetConfiguration.TABLE_GET_PARAM_VALUES_BY_PARAM_CATEGORY, data_parameters=rec_count_param)[0]
    record_count_total = obj_qry.get_rows(sql_script=const.QryGetGuiInfo.TABLE_REC_COUNT)[0]
    page_count = math.ceil(int(record_count_total) / int(record_count_per_page))
    return page_count


def description_to_id(key_name, input_value):
    sql_query = const.MappingMatrix.DESCRIPTION_TO_CODE_QRY_MAPPING[key_name]
    data_response = dq.dql_fetch_one_row_for_one_input(database=config.SQLITE_DB, data_input=input_value, sql_script=sql_query)
    return data_response


def _dataframe_to_db_insert(dataframe, dataframe_columns, insert_sql_script, column_key_mapping):
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


def _perform_mapping_update(entity_type_value, update_payload, identifier_value, obj_chk, obj_qry, obj_updt):
    id_search_param = {'searchValue': identifier_value}
    if not (obj_chk.data_exists(sql_script=const.QryGetGuiInfo.TABLE_GET_INFO_BY_ID, data_parameter=id_search_param)):
        raise obj_error.NoContent('The data you are trying to update does not exist. Please provide a valid identifier')
    else:
        json_obj_keys = list(update_payload.keys())
        json_obj_keys.remove('action')
        action = update_payload.get('action')
        if action != 'U':
            raise obj_error.InvalidOperation(message='The action you are trying to perform is not allowed. Please verify the action and retry the operation.')
        else:
            for idx in range(len(json_obj_keys)):
                mapping_param = {'entityType': entity_type_value, 'keyName': update_payload.get(json_obj_keys[idx])}
                old_value = update_payload.get(json_obj_keys[idx]).get('oldValue')
                new_value = update_payload.get(json_obj_keys[idx]).get('newValue')
                current_db_value = obj_qry.get_rows_with_param(sql_script=const.QryGetGuiInfo.TABLE_GET_INFO_BY_ID, data_parameters=id_search_param, return_list=True)[0]
                if current_db_value != old_value:
                    raise obj_error.ValueMismatch(message="Provided oldValue & current value in the database does not match. Please verify the oldValue and retry the operation.")
                else:
                    update_query = obj_qry.get_rows_with_param(sql_script=const.QryGetUpdateQueryMapping.TABLE_QRY_MAPPING_BY_KEY, data_parameters=mapping_param, return_list=True)[0]
                    update_sql_param = {'newValue': new_value, 'id': identifier_value}
                    obj_updt.update_data_with_param(sql_script=update_query, data_parameters=update_sql_param)


def _generate_data_sql_parameters(component_type, obj_qry, display_dev_info, input_form_keys, mapping_sql_query, valid_keys_sql_param, valid_form_keys_list, input_request_form):
    result_list = {}
    data_key_value_list = {}
    if display_dev_info in [True, 'True', 'true']:
        result_list['devInfo_uiElementCount'] = len(input_form_keys)
        result_list['devInfo_sqlQuery'] = mapping_sql_query
        result_list['devInfo_sqlQuerySearchParameters'] = valid_keys_sql_param

    if set(input_form_keys).issubset(set(valid_form_keys_list)):
        for idx in range(len(input_form_keys)):
            get_name_search_param = {"uiTagName": input_form_keys[idx]}
            sql_tag_name = obj_qry.get_rows_with_param(sql_script=mapping_sql_query, data_parameters=get_name_search_param, return_list=True)[0]
            data_key_value_list[sql_tag_name] = input_request_form.form.get(valid_form_keys_list[idx])
        result_list[component_type] = data_key_value_list
        return result_list
    elif set(input_form_keys).issuperset(set(valid_form_keys_list)):
        # print(component_type)
        for idx in range(len(valid_form_keys_list)):
            get_name_search_param = {"uiTagName": valid_form_keys_list[idx]}
            sql_tag_name = obj_qry.get_rows_with_param(sql_script=mapping_sql_query, data_parameters=get_name_search_param, return_list=True)[0]
            data_key_value_list[sql_tag_name] = input_request_form.form.get(valid_form_keys_list[idx])
            # print(data_key_value_list)
        result_list[component_type] = data_key_value_list
        return result_list
    else:
        raise obj_error.MissingMandatoryKeys(f'Values provided do not match the template. \nFields Count: {len(valid_form_keys_list)} - Must contain {valid_form_keys_list}')
