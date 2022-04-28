import time

import flask
from flask import Flask, Response
from flask_cors import CORS
from flask_socketio import send, SocketIO, emit, Namespace

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/", methods=["HEAD"])
def head():
    response = Response()
    response.headers.add("content-length", 1000000)  # todo: 100000 what?
    return response


@app.route("/", methods=["GET"])
def hello():
    response = flask.jsonify({"mutch": "oof"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

class STMPYHomeOfficeResponses:
    def __init__(self):
        pass

    def timer_done(self):
        pass

#
#  STM HOME OFFICE STMPY responses
#
def pause_timer_done():
    pass

def connection_issues():
    pass

def meeting_match_response():
    pass

def meeting_timer_done():
    pass



class CustomNamespace(Namespace):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.n = 0

    def on_connect(self, data):
        print("user connected", data)
        pass

    def on_disconnect(self, data):
        print("user disconnected", data)

    def on_message(self, data):
        print(data)
        print(f"received message: {data}")
        time.sleep(0.5)
        self.n += 1
        emit("message", '{"data": ' + f'"{self.n}"' + '}')
        print(f"sent resp:")

    #
    #  STM HOME OFFICE STMPY
    #

    def on_start_timer_clicked(self, data):
        pass

    def on_abort_pause_timer(self):
        pass

    def on_meeting_connection_request(self, data):
        pass



# @socketio.on("message", namespace="/ws_test")
# def handle_message(data):

socketio.on_namespace(CustomNamespace("/ws_test"))

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000)
