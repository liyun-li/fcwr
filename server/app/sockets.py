from app.models import socketio
from flask_socketio import emit,send
from flask import session, request
from app.models import db, User

clients={}
usednum=[0,1111,1234]

@socketio.on('get_number')
def send_number(msg):
    open_id=msg['open_id']
    user = User.query.filter_by(open_id=open_id).first()
    if not user
        emit('response', {'data':'user not register'})
        return
    if user.number != None:
        emit('response', {'data':user.number})
        return
    user_matched = User.query.filter_by(number!=None and gender=user.like_gender).first()
    if not user_matched:
        temp = random.randint(0, 9999)
        while (temp in usednum):
            temp = random.randint(0, 9999)
        usednum.append(temp)
        user.number = temp
        db.session.add(user)
        db.session.commit()
        emit('response', {'data':temp})


# for test -----------------
@socketio.on('client_event')
def client_msg(msg):
    emit('server_response', {'data': msg['data']})

@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})

