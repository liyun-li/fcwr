def create_app():
    from flask import Flask
    from app.stream import socketio
    from app.views import views
    from app.models import db

    app = Flask(__name__)

    # configure
    app.config.from_object('config.Config')

    # initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # initialize socketio
    socketio.init_app(app)

    app.register_blueprint(views)

    app.db = db
    app.socketio = socketio

    # secret key for session
    app.secret_key = 'super secret key'

    return app
