from dependency_injector.wiring import inject, Provide
from flask_smorest import Blueprint

from app.di_container import DiContainer
from app.models.inference_request_schema import InferenceRequestSchema
from app.models.inference_request_schema import InferenceRequestQuerySchema
from app.models.inference_response_schema import InferenceResponseSchema

from app.services.inference_service import InferenceService

inference_controller = Blueprint("InferenceController", __name__, description="Inference API")

@inference_controller.post("/infer")
@inference_controller.arguments(InferenceRequestSchema)
@inference_controller.arguments(InferenceRequestQuerySchema, location="query")
@inference_controller.response(200, InferenceResponseSchema)
@inject
def post_infer(body, query, service: InferenceService = Provide[DiContainer.inference_service]):
    return InferenceResponseSchema().load({
        "model_name": query.get("name"),
        "model_id": query.get("id"),
        "output": service.infer(query.get("name"), query.get("id"), body.get('data'))
    })

@inference_controller.route("/warmup")
@inference_controller.response(200)
def get_warmup():
    return ""
