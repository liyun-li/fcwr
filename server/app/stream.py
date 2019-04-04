from flask_socketio import SocketIO, emit
from flask import session, request

from app.utils import get_user

socketio = SocketIO()


@socketio.on('get_queue')
def send_queue(data):
    open_id = session.get('open_id') or request.args.get('open_id')

    if open_id:
        user = get_user(open_id)
        if user:
            emit('waitlist', {'queue': user.queue})
        else:
            emit('waitlist', {'error': 'User not found'})
    else:
        emit('waitlist', {'error': 'Oh no. No open id'})
