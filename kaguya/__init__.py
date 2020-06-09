from flask import Flask
from kaguya.admins.routes import admins
from kaguya.anime.routes import anime
from kaguya.main.routes import main
from kaguya.users.routes import users
from config import Config


def create_app():
    # Creation of Flask-App
    app = Flask(__name__)

    # Set configuration
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(admins)
    app.register_blueprint(anime)
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
