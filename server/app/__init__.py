def create_app():
    from flask import Flask, Session
    from app.models import db

    app = Flask(__name__)
    return app
