from dotenv import load_dotenv

load_dotenv()

from flask import Flask

from .config import Config
from .extensions import db, jwt
from .models import User, Blog
from .routes import auth_bp, blog_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    with app.app_context():
        db.create_all()

    return app