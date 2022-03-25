import flask
from flask import Flask, Response

app = Flask(__name__)


@app.route('/', methods=['HEAD'])
def head():
    response = Response()
    response.headers.add('content-length', 1000000)# todo: 100000 what?
    return response

@app.route('/', methods=["GET"])
def hello():
    response = flask.jsonify({"mutch": "oof"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)