import os
from flask import Blueprint, request, render_template, flash, send_file, current_app
from werkzeug.exceptions import HTTPException
from app.api import functionality as api_func
import utilities.custom_app_logger as cust_log
# from app.constants import FileSystemInformation as fsi

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


# @bp_gui.route('/file/template', methods=['GET', 'POST'])
# def template_file():
#     template_path = fr'{os.path.join(current_app.root_path, fsi.DATA_TEMPLATE_FOLDER)}\{fsi.DATA_TEMPLATE_FILENAME}'
#     print(template_path)
#     cust_log.log_message(level='info', message='Calling endpoint /gui/file/template - Downloading template', call_type='GUI')
#     return send_file(path_or_file=template_path, as_attachment=True)


@bp_gui.route('/admin', methods=['GET'])
def admin():
    if request.args.get('download') == 'true':
        flash('Template downloaded successfully!', 'success')
        
    return_data_extract = api_func.return_all_mapping_information(return_json_response=False)
    cust_log.log_message(level='info', message='Calling endpoint /gui/admin', call_type='GUI')
    return render_template('admin.html', display_data_extract=return_data_extract)


@bp_gui.errorhandler(HTTPException)
def display_error_page_404(error):
    error_short_description = "Something went wrong"
    error_message = error.description
    return render_template('error.html', error_short_desc=error_short_description, error_message=error_message), 404

