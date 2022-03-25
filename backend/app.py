import flask
from flask import Flask
app = Flask(__name__)
print("\n\n\n\nwaaaaaaaaaaaaaaaa\n\n\n")

@app.route('/test')
def hello():
    response = flask.jsonify({"mutch": "oof"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)