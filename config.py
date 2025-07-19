import os

# Getting base directory of the application
BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

# Application Configurations
APP_NAME = os.getenv("APP_NAME", "Unified-Field-Mapping-Assistant")
APP_ENV = os.getenv("APP_ENV", "dev")
APP_DEBUG_MODE = os.getenv("APP_DEBUG", "False").lower() in ("true", "1")
APP_PORT = os.getenv("APP_PORT", 1001)
APP_HOST = os.getenv("APP_HOST", '127.0.0.1')
APP_SECRET_KEY = ''
APP_LOGFILE = f'{BASE_DIRECTORY}/logs/logfile.log'

# SQLite3 Database
SQLITE_DB = fr"{BASE_DIRECTORY}/database/dev/{os.getenv("DB", "unified_field_mapping_db.db")}" if APP_ENV == 'dev' else fr"{BASE_DIRECTORY}/database/prod/{os.getenv("DB", "unified_field_mapping_db.db")}"

# API Documentation Configuration
SWAGGER_ENDPOINT = "/api/docs"
SWAGGER_API_URL = f"/swagger.json"
SWAGGER_CONFIG = {
    "app_name": "Flask project | API Doc",
    "layout": "BaseLayout",  # Options: "BaseLayout", "StandaloneLayout", "Topbar"
    "deepLinking": True,
    "displayOperationId": True,
    "defaultModelsExpandDepth": -1,
    "defaultModelRendering": "model",
}
