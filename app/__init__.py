from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # register blueprints
    from .routes.agents import agents_bp
    from .routes.properties import properties_bp
    from .routes.chat import chat_bp

    app.register_blueprint(agents_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(chat_bp)

    return app
