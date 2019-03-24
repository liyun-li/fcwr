def create_app():
    from flask import Flask
    from app.models import db
    from app.views import views

    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    # configure
    app.config.from_object('config.Config')

    # initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(views)

    app.db = db

    return app
