from flask import Flask
import os

from app.models import db
from app.config import Configuration
from app.views import blueprint as views_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    init_db(app)
    app.register_blueprint(views_blueprint)
    return app


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
