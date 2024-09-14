from flask import Flask
from app.vlad.laba1 import laba1_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(laba1_bp)

    return app
