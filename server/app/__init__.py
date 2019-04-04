def create_app():
    from flask import Flask
    from app.stream import socketio
    from app.views import views
    from app.models import db

    app = Flask(__name__)

    # register blueprints
    app.register_blueprint(views)

    # configure
    app.config.from_object('config.Config')

    # initialize database
    db.init_app(app)
    with app.app_context():
        if app.config['DEBUG']:
            db.drop_all()
        db.create_all()
    app.db = db

    # initialize socketio
    socketio.init_app(app)
    app.socketio = socketio

    return app
