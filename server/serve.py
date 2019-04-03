from app import create_app

app = create_app()

if __name__ == '__main__':
    from flask_socketio import SocketIO

    app.config['SECRET_KEY'] = '823rFF43j2f\x5585htf@#%*'

    socketio = SocketIO(app)
    socketio.run(app, host='0.0.0.0', port=3000)
