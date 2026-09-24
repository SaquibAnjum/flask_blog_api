from flask import Flask

from dotenv import load_dotenv
load_dotenv()

from .config import Config
from .extensions import db, jwt

from .models import User

def create_app():

    app= Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    return app 