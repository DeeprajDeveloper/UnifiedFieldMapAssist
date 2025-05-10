from typing import Union
from flask import jsonify
import utilities.ERROR.custom as err


def _status_information(status_code, status_message, is_success):
    response_data = {
        'statusCode': status_code,
        'statusDescription': 'SUCCESS' if is_success else 'FAILURE',
        'statusMessageText': status_message
    }
    return response_data


def _error_information(error):
    response_data = {
        'errorCode': error.error_code if hasattr(error, 'error_code') else "UNKNOWN",
        'errorDescription': type(error).__name__,
        'errorStacktrace': str(error)
    }
    return response_data


def json_builder_from_list(keys_list: list, data_list: list, return_type: str) -> Union[list, dict]:
    """

    :param keys_list: List of keys in the JSON response
    :param data_list: List of values in the JSON response
    :param return_type: String with 2 values: list / dictionary
    :return: List of Dictionary
    """

    try:
        if return_type == 'list':
            response_data_list: list = []
            for item_id in range(len(data_list)):
                data_list_json: dict = {}
                for key_id in range(len(keys_list)):
                    data_list_json[keys_list[key_id]] = data_list[item_id][key_id]
                response_data_list.append(data_list_json)
            return response_data_list
        elif return_type == 'dictionary':
            response_data_dict: dict = {}
            if len(keys_list) == len(data_list):
                for item_id in range(0, len(data_list)):
                    response_data_dict[keys_list[item_id]] = data_list[item_id]
                return response_data_dict
        else:
            raise err.InvalidReturnType(message=f"Expected list or dictionary, got {return_type} instead.")
    except Exception as error:
        print(str(error))


def response_template(success=True, message="", data=None, error=None, status_code=200, display_error=False):
    if display_error:
        response_body = {
            "statusInformation": _status_information(status_code=status_code, status_message=message, is_success=success),
            "errorInformation": _error_information(error=error),
            "dataExtract": data
        }
    else:
        response_body = {
            "statusInformation": _status_information(status_code=status_code, status_message=message, is_success=success),
            "dataExtract": data
        }
    response_body = {key: value for key, value in response_body.items() if value is not None}
    return jsonify(response_body), status_code

