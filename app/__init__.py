import os
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import load_dotenv

# טען משתני סביבה מה-.env
load_dotenv()

# אתחול שירותים חיצוניים
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # התחלת החיבורים
    db.init_app(app)
    jwt.init_app(app)

    # חיבור Flasgger (Swagger UI)
    Swagger(app)

    # רישום Blueprints
    from .routes.agents import agents_bp
    from .routes.properties import properties_bp
    from .routes.chat import chat_bp

    app.register_blueprint(agents_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(chat_bp)

    return app
