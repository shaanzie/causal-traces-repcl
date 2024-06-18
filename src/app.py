# Web imports

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'repviz'
socketio = SocketIO(app)

trace_store = []


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init', methods = ['POST'])
def init():
    initParams = json.loads(request.get_json())
    socketio.emit('init', initParams)
    return jsonify({"status": 200})

@app.route('/add', methods = ['POST'])
def add_event():
    event = json.loads(request.get_json())

    trace_store.append(event)
    if(event["event_type"] == "SEND"):
        add_send_event_to_graph(event)
    else:
        add_recv_event_to_graph(event)

    return jsonify({"status": 200})

def add_send_event_to_graph(event):
    socketio.emit('update', event)

def add_recv_event_to_graph(event):
    socketio.emit('update', event)

if __name__ == '__main__':
    app.run(debug=True)