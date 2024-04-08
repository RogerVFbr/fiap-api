from dependency_injector.wiring import inject, Provide
from flask_smorest import Blueprint

from di_container import DiContainer
from models.comercializacao_response_schema import ComercializacaoResponseSchema
from models.exportacao_response_schema import ExportacaoResponseSchema
from models.importacao_response_schema import ImportacaoResponseSchema
from models.processamento_response_schema import ProcessamentoResponseSchema
from models.producao_response_schema import ProducaoResponseSchema
from services.embrapa_service import EmbrapaService

embrapa_controller = Blueprint("EmbrapaController", __name__, description="Embrapa API")


@embrapa_controller.route("/producao")
@embrapa_controller.response(200, ProducaoResponseSchema(many=True))
@inject
def get_all_producao(embrapa_service: EmbrapaService = Provide[DiContainer.embrapa_service]):
    return embrapa_service.get_all_producao()


@embrapa_controller.route("/processamento")
@embrapa_controller.response(200, ProcessamentoResponseSchema(many=True))
@inject
def get_all_processamento(embrapa_service: EmbrapaService = Provide[DiContainer.embrapa_service]):
    return embrapa_service.get_all_processamento()


@embrapa_controller.route("/comercializacao")
@embrapa_controller.response(200, ComercializacaoResponseSchema(many=True))
@inject
def get_all_comercializacao(embrapa_service: EmbrapaService = Provide[DiContainer.embrapa_service]):
    return embrapa_service.get_all_comercializacao()


@embrapa_controller.route("/importacao")
@embrapa_controller.response(200, ImportacaoResponseSchema(many=True))
@inject
def get_all_importacao(embrapa_service: EmbrapaService = Provide[DiContainer.embrapa_service]):
    return embrapa_service.get_all_importacao()


@embrapa_controller.route("/exportacao")
@embrapa_controller.response(200, ExportacaoResponseSchema(many=True))
@inject
def get_all_exportacao(embrapa_service: EmbrapaService = Provide[DiContainer.embrapa_service]):
    return embrapa_service.get_all_exportacao()
