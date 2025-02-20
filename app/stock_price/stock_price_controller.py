from dependency_injector.wiring import inject, Provide
from flask_smorest import Blueprint

from app.crosscutting.di_container import DiContainer
from app.stock_price.schemas.stock_price_request_schema import StockPriceRequestSchema
from app.stock_price.schemas.stock_price_request_schema import StockPriceRequestQuerySchema
from app.stock_price.schemas.stock_price_response_schema import StockPriceResponseSchema

from app.stock_price.stock_price_service import StockPriceService

stock_price_controller = Blueprint("StockPriceInferenceController", __name__, description="Stock Price API")

@stock_price_controller.post("/stock-price/infer")
@stock_price_controller.arguments(StockPriceRequestSchema)
@stock_price_controller.arguments(StockPriceRequestQuerySchema, location="query")
@stock_price_controller.response(200, StockPriceResponseSchema)
@inject
def post_infer(body, query, service: StockPriceService = Provide[DiContainer.stock_price_service]):
    return StockPriceResponseSchema().load({
        "model_name": query.get("name"),
        "model_id": query.get("id"),
        "output": service.infer(query.get("name"), query.get("id"), body.get('data'))
    })

