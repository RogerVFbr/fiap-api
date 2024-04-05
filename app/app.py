from flask import (Flask, jsonify)

from repositories.embrapa_repository import EmbrapaRepository
from services.embrapa_service import EmbrapaService

app = Flask(__name__)

repo = EmbrapaRepository()
service = EmbrapaService(repo)


@app.get('/producao')
def get_all_producao():
    return jsonify(status=200, message='producao', payload=service.get_all_producao())


@app.get('/processamento')
def get_all_processamento():
    return jsonify(status=200, message='processamento', payload=service.get_all_processamento())


@app.get('/comercializacao')
def get_all_comercializacao():
    return jsonify(status=200, message='comercializacao', payload=service.get_all_comercializacao())


@app.get('/importacao')
def get_all_importacao():
    return jsonify(status=200, message='importacao', payload=service.get_all_importacao())


@app.get('/exportacao')
def get_all_exportacao():
    return jsonify(status=200, message='exportacao', payload=service.get_all_exportacao())

