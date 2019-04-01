from app.models import socketio
from flask_socketio import emit,send
from flask import session, request
from app.models import db, User
from sqlalchemy import and_
import random

clients={}
usednum=[0,1111,1234]

@socketio.on('get_number')
def send_number(msg):
    open_id = session['open_id']
    user = User.query.filter(User.open_id==open_id).first()
    if user.gender == user.like_gender:
        return
    if not user:
        emit('response', {'data':'user not register'})
        return
    if user.number != None:
        emit('response', {'data':user.number})
        return
    clients[open_id] = request.sid
    user_matched = User.query.filter(User.number==None).filter(User.gender==user.like_gender).first()
    if user_matched != None:
        temp = random.randint(0, 9999)
        while (temp in usednum):
            temp = random.randint(0, 9999)
        usednum.append(temp)
        user.number = temp
        db.session.add(user)
        user_matched.number = temp
        db.session.add(user_matched)
        db.session.commit()
        emit('response', {'data':temp})
        emit('response', {'data':temp}, room=clients[user_matched.open_id])

# for test -----------------
@socketio.on('client_event')
def client_msg(msg):
    emit('server_response', {'data': msg['data']})

@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})

