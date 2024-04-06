from flask.views import MethodView
from flask_smorest import Blueprint

from crosscutting.dependency_injection import service
from models.comercializacao_response_schema import ComercializacaoResponseSchema
from models.exportacao_response_schema import ExportacaoResponseSchema
from models.importacao_response_schema import ImportacaoResponseSchema
from models.processamento_response_schema import ProcessamentoResponseSchema
from models.producao_response_schema import ProducaoResponseSchema

embrapa_controller = Blueprint("EmbrapaController", __name__, description="Embrapa API")


@embrapa_controller.route("/producao")
class ProducaoCollection(MethodView):
    @embrapa_controller.response(200, ProducaoResponseSchema(many=True))
    def get(self):
        return service.get_all_producao()


@embrapa_controller.route("/processamento")
class ProcessamentoCollection(MethodView):
    @embrapa_controller.response(200, ProcessamentoResponseSchema(many=True))
    def get(self):
        return service.get_all_processamento()


@embrapa_controller.route("/comercializacao")
class ComercializacaoCollection(MethodView):
    @embrapa_controller.response(200, ComercializacaoResponseSchema(many=True))
    def get(self):
        return service.get_all_comercializacao()


@embrapa_controller.route("/importacao")
class ImportacaoCollection(MethodView):
    @embrapa_controller.response(200, ImportacaoResponseSchema(many=True))
    def get(self):
        return service.get_all_importacao()


@embrapa_controller.route("/exportacao")
class ExportacaoCollection(MethodView):
    @embrapa_controller.response(200, ExportacaoResponseSchema(many=True))
    def get(self):
        return service.get_all_exportacao()
