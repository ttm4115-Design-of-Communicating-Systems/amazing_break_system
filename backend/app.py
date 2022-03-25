import time

import flask
from flask import Flask, Response
from flask_cors import CORS
from flask_socketio import send, SocketIO, emit

app = Flask(__name__)
cors = CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app ,cors_allowed_origins="*")

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

@socketio.on('message', namespace="/ws_test")
def handle_message(data):
    print(f'received message: {data}')
    time.sleep(0.5)
    emit('message','{"data": "pong"}')
    print(f'sent resp:')



if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)