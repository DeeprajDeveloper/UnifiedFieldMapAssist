from typing import Union
from datetime import datetime
import utilities.LOG.logger as cust_log
from flask import Blueprint, jsonify
from app.api import functionality as func

bp_api = Blueprint('bp_api', __name__, url_prefix='/api')


@bp_api.route('/health', methods=['GET'])
def health():
    cust_log.log_message(level='info', message='Calling Health', call_type='API')
    return jsonify({'status': 'healthy'}), 200


@bp_api.route('/v1/readAll')
def read_all_fields():
    cust_log.log_message(level='info', message='Calling endpoint /api/v1/readAll', call_type='API')
    return func.return_all_mapping_information()
