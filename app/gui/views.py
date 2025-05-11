import os
from datetime import datetime
from flask import Blueprint, request, render_template, abort, flash, redirect, url_for
from werkzeug.exceptions import HTTPException
from app.gui import functionality as gui_func
from app.api import functionality as api_func
import utilities.LOG.logger as cust_log

bp_gui = Blueprint(
    'bp_gui'
    , __name__
    , url_prefix='/gui'
    , template_folder='templates'
    , static_folder=os.path.join(os.path.dirname(__file__), 'static')
    , static_url_path='/bp_gui/static'
)


@bp_gui.route('/', methods=['GET'])
@bp_gui.route('/home', methods=['GET'])
def index():
    return_data_extract = api_func.return_all_mapping_information(return_json_response=False)
    cust_log.log_message(level='info', message='Calling endpoint /gui', call_type='GUI')
    return render_template('index.html', display_data_extract=return_data_extract)


@bp_gui.route('/release', methods=['GET'])
def release():
    cust_log.log_message(level='info', message='Calling endpoint /gui/release', call_type='GUI')
    return render_template('release.html')


@bp_gui.errorhandler(HTTPException)
def display_error_page_404(error):
    error_short_description = "Something went wrong"
    error_message = error.description
    return render_template('error.html', error_short_desc=error_short_description, error_message=error_message), 404

