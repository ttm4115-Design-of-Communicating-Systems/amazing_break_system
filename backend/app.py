
from urllib import response
import flask
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin

from stmpy import Machine, Driver

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


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

@app.route("/post", methods=["POST"])
def update():
    if not request.json:
        print("INVALID MESSAGE")
        return; 

    message = request.json['message']
    wt = request.json['wt']
    bt = request.json['bt']
    print("MESSAGE RECEIVED:", message)
    print("wt RECEIVED:", wt)
    print("bt RECEIVED:", bt)

    obj.on_message(message, wt, bt)

    
    response = flask.jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/state', methods=["GET"])
def get_state():
    flag = obj.flag
    return flask.jsonify({
        'state': flag, 
        'wt': obj.worktime / 60000, 
        'bt': obj.breaktime / 60000
    })

class StmpyObj:
    def __init__(self) -> None:
        self.stm: Machine | None = None
        self.flag = "STANDBY"
        self.worktime = 1*60000
        self.breaktime = 1*60000
        self.waittime = 1 # not in use
    
    def on_message(self, msg, wt=25*60000, bt=5*60000):
        try:
            print("STM RECVD MSG", msg)
            
            if (self.stm == None):
                print("MACHINE NOT SET UP")
                return
            
            if msg == 'click_start_timer':
                self.stm.send('start_work')
            elif msg == 'click_abort':
                self.stm.send('abort')
            elif msg == 'dont_pause':
                self.stm.send('dont_pause')
            elif msg == 'accept_meeting':
                self.stm.send('accept_meeting')
            elif msg == 'update_dur':
                self.worktime = wt * 60000
                self.breaktime = bt * 60000
            else:
                print("NO ACTION DEFINED FOR MESSAGE:", msg)
        except KeyError:
            print("RECEIVED MALFORMED MESSAGE")
    
    def set_flag(self, flag):
        self.flag = flag
    
    def do_start_timer(self, name, duration=None):
        if not self.stm:
            return

        if duration:
            self.stm.start_timer(name, duration)
            return
        
        if name == "work_timer":
            self.stm.start_timer(name, self.worktime)
        elif name == "meeting_timer":
            self.stm.start_timer(name, self.breaktime)
        elif name == "timeout":
            self.stm.start_timer(name, self.waittime)
        else:
            print("INVALID TIMER")

ts = [{
        "source": "initial",
        "target": "s_standby"
    }, {
        "source": "s_standby",
        "target": "s_working",
        "trigger": "start_work",
    }, {
        "source": "s_working",
        "target": "s_standby",
        "trigger": "abort",
        "effect": "stop_timer('work_timer')"
    }, {
        "source": "s_working",
        "target": "s_meeting_notify",
        "trigger": "work_timer",
        "effect": "set_flag('WAITING')"
    }, {
        "source": "s_meeting_notify",
        "target": "s_working",
        "trigger": "dont_pause",
    }, {
        "source": "s_meeting_notify",
        "target": "s_neg_connection",
        "trigger": "accept_meeting",
    }, {
        "source": "s_neg_connection",
        "target": "s_meeting", # TEMPORARY - should go to standby
        "trigger": "timeout",
    }, {
        "source": "s_neg_connection",
        "target": "s_meeting",
        "trigger": "meeting_match",
    }, 
    {
        "source": "s_meeting",
        "target": "s_working",
        "trigger": "meeting_timer",
    },
    ]

ss = [{
        "name": "s_standby",
        "entry": "set_flag('STANDBY')"
    }, {
        "name": "s_working",
        "entry": "set_flag('WORKING'); do_start_timer('work_timer')"
    }, {
        "name": "s_neg_connection",
        "entry": "set_flag('SEARCHING'); do_start_timer('timeout')"
    }, {
        "name": "s_meeting",
        "entry": "set_flag('MEETING'); do_start_timer('meeting_timer')"
    }]

obj = StmpyObj()
stm = Machine(transitions=ts, states=ss, obj=obj, name="stm")
obj.stm = stm

driver = Driver()
driver.add_machine(stm)
driver.start()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)