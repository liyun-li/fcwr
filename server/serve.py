if __name__ == '__main__':
    from app import create_app
    from app.models import socketio
    import app.sockets
    app = create_app()
    socketio.init_app(app)
    socketio.run(app, debug=True, host='0.0.0.0', port=3000)
#app.run(host='0.0.0.0', port=3000)



