from flask import (Flask, jsonify)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    return jsonify(status=200, message='hello world')


@app.route('/develop', methods=['GET', 'POST'])
def hello2():
    return jsonify(status=200, message='develop')
