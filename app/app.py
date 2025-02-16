import sys
import os

print("CWD")
print(os.getcwd())
print("PATHS")
for i in sys.path:
    print(i)

from flask import Flask
from flask_smorest import Api
import polars as pl

from app.news_recommendation.news_recommendation_controller import news_recommendation_controller
from app.stock_price.stock_price_controller import stock_price_controller
from app.embrapa_proxy.embrapa_controller import embrapa_controller
from app.warmup.warm_up_controller import warm_up_controller
from app.crosscutting.di_container import DiContainer

pl.Config.set_tbl_cols(1000)
pl.Config.set_tbl_width_chars(500)
pl.Config.set_fmt_str_lengths(1500)
pl.Config.set_tbl_rows(40)
pl.Config.set_fmt_table_cell_list_len(100)
pl.Config.set_tbl_column_data_type_inline(True)
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

api.register_blueprint(warm_up_controller)
api.register_blueprint(embrapa_controller)
api.register_blueprint(stock_price_controller)
api.register_blueprint(news_recommendation_controller)


