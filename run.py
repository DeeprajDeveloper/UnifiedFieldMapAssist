from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import logging
import config
from app.api.routes import bp_api
from app.auth.routes import bp_auth
from app.gui.views import bp_gui
from flask_sitemap import Sitemap

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = config.APP_SECRET_KEY
app.json.sort_keys = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.register_blueprint(bp_gui)
app.register_blueprint(bp_api)
app.register_blueprint(bp_auth)

swagger_document = get_swaggerui_blueprint(config.SWAGGER_ENDPOINT, config.SWAGGER_API_URL, config=config.SWAGGER_CONFIG)
app.register_blueprint(swagger_document, url_prefix=config.SWAGGER_ENDPOINT)


@app.route("/swagger.json")
def send_swagger():
    return send_from_directory("app/doc/static", "swagger.json")


if __name__ == "__main__":
    print(f"[{config.APP_NAME}] | STARTED {config.APP_HOST}:{config.APP_PORT} | DEBUG MODE [{'on' if config.APP_DEBUG_MODE else 'off'}]")
    app.run(debug=config.APP_DEBUG_MODE, port=config.APP_PORT, host=config.APP_HOST)
