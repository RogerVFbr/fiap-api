from flask import Flask
from flask_smorest import Api

from controllers.embrapa_controllers import embrapa_controller
from di_container import DiContainer

app = Flask(__name__)

app.container = DiContainer()

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Embrapa API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(embrapa_controller)


