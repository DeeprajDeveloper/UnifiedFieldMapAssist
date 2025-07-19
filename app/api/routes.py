import utilities.custom_app_logger as obj_logger
from flask import Blueprint, jsonify, request
from app.api import functionality as func

bp_api = Blueprint('bp_api', __name__, url_prefix='/api')


@bp_api.route('/health', methods=['GET'])
def health():
    obj_logger.log_message(level='info', message='Calling Health', call_type='API')
    return jsonify({'status': 'healthy'}), 200


@bp_api.route('/v1/readConfig', methods=['GET'])
def get_config():
    response_data = func.read_config(input_json_request=request)
    obj_logger.log_message(level='info', message='Calling endpoint /api/v1/getConfig', call_type='API')
    return response_data


@bp_api.route('/v1/updateConfig/<int:parameter_id>', methods=['PUT'])
def update_config(parameter_id):
    update_payload = request.get_json()
    response_data = func.update_config(parameter_id=parameter_id, update_payload=update_payload)
    obj_logger.log_message(level='info', message='Calling endpoint /api/v1/updateConfig', call_type='API')
    return response_data


@bp_api.route('/v1/readMapping', methods=['GET'])
def get_mapping():
    response_json = func.read_mapping_information(input_request_json=request)
    obj_logger.log_message(level='info', message='Calling endpoint /api/v1/getMapping', call_type='API')
    return response_json


@bp_api.route('/v1/updateMapping', methods=['PUT'])
def update_mapping():
    response_json = func.update_mapping_information(query_parameters=request, update_payload=request.get_json())
    obj_logger.log_message(level='info', message='Calling endpoint /api/v1/getMapping', call_type='API')
    return response_json


@bp_api.route('/v1/addMapping/<string:component_type>', methods=['POST'])
def add_mapping(component_type):
    response_json = func.add_mapping_information(input_request_form=request, component_type=component_type)
    obj_logger.log_message(level='info', message='Calling endpoint /api/v1/addMapping', call_type='API')
    return response_json


@bp_api.route('/v1/loadData', methods=['GET', 'POST'])
def load_data_from_template():
    template_name = request.args.get('templateName')
    if template_name:
        response_json = []
    else:
        response_json = func.return_mapping_information()
    cust_log.log_message(level='info', message='Calling endpoint /api/v1/loadData', call_type='API')
    return response_json



