from app.models import socketio
from flask_socketio import emit,send
from flask import session


@socketio.on('get_number')
def send_number(msg):
    emit('response', {'data': msg['data']})

# for test -----------------
@socketio.on('client_event')
def client_msg(msg):
    emit('server_response', {'data': msg['data']})

@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})

