import time

import flask
from flask import Flask, Response
from flask_cors import CORS
from flask_socketio import send, SocketIO, emit, Namespace, join_room, leave_room, socketio

from stmpy import Machine, Driver

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)


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

ts = [{
        "source": "initial",
        "target": "s_standby"
    }, {
        "source": "s_standby",
        "target": "s_working",
        "trigger": "start_work",
        "effect": "send_message('wasap'); start_timer('work_timer', 600)" # 10min
    }, {
        "source": "s_working",
        "target": "s_standby",
        "trigger": "abort",
        "effect": "stop_timer('work_timer')"
    }, {
        "source": "s_working",
        "target": "s_meeting_notify",
        "trigger": "work_timer"
    }, {
        "source": "s_meeting_notify",
        "target": "s_working",
        "trigger": "dont_pause"
    }, {
        "source": "s_meeting_notify",
        "target": "s_neg_connection",
        "trigger": "accept_pause",
        "effect": "start_timer('timeout', 60)"
    }, {
        "source": "s_neg_connection",
        "target": "s_meeting",
        "trigger": "meeting_match",
        "effect": "start_timer('meeting_timer', 300)" # 5min
    }, 
    {
        "source": "s_meeting",
        "target": "user_working",
        "trigger": "meeting_timer",
        "effect": "send_message('back_to_work')"
    },
    {
        "source": "s_neg_connection",
        "target": "s_standby",
        "trigger": "timeout"
    }]


class CustomNamespace(Namespace):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.stm: Machine | None = None

        # for message de-duplication
        self.last_msg = None

    def on_connect(self):
        print("CONNECTED")
        emit("message", '{"data": "1234123"}')

    def on_disconnect(self):
        print("DISCONNECTED")

    def on_message(self, data):
        
        try:
            msg = data['data']['status']
            print("RECVD MSG", msg)
            if (self.stm == None):
                print("MACHINE NOT SET UP")
                return
            
            if (msg == self.last_msg):
                print(f"DEDUP {msg}")
                return
            
            self.last_msg = msg

            if msg == 'click_start_timer':
                self.stm.send('start_work')
            elif msg == 'click_abort':
                self.stm.send('abort')
            elif msg == 'dont_pause':
                self.stm.send('dont_pause')
            elif msg == 'accept_meeting':
                self.stm.send('accept_meeting')
        except KeyError:
            print("RECEIVED MALFORMED MESSAGE")

    def send_message(self, msg):
        print("SENDING MESSAGE", msg)
        emit("message", '{"data": "' + msg + '"}', broadcast=True)  # type: ignore

class StmpySingleton:
    instance = None

    @staticmethod
    def get_instance():
        if StmpySingleton.instance is None:
            StmpySingleton.instance = StmpySingleton()
        
        return StmpySingleton.instance

    def __init__(self) -> None:
        self.namespace = CustomNamespace("/ws_test")
        self.stm = Machine(transitions=ts, obj=self.namespace, name="stm")
        self.namespace.stm = self.stm
        
        driver = Driver()
        driver.add_machine(self.stm)
        driver.start()


# @socketio.on("message", namespace="/ws_test")
# def handle_message(data):

socketio.on_namespace(StmpySingleton.get_instance().namespace)

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000)