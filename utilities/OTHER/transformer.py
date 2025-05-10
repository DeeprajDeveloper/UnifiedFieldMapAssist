import utilities.ERROR.custom as cError


def transform_to_boolean(list_data_input):
    response_list: list = []
    if 0 in list_data_input or 1 in list_data_input:
        for item in list_data_input:
            response_list.append(True if item == 1 else False)
    else:
        raise cError.InvalidData(message='Expecting binary values 0/1')
    return response_list
