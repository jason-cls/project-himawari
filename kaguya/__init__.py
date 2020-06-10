from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from kaguya.config import Config

# Extentions
db = SQLAlchemy()


def create_app(create_db=False):
    # Creation of Flask-App
    app = Flask(__name__)

    # Set configuration
    app.config.from_object(Config)



    #Register Blueprint
    # Need to put blueprint imports here to avoid circular import error
    from kaguya.admins.routes import admins
    from kaguya.anime.routes import anime
    from kaguya.main.routes import main
    from kaguya.users.routes import users
    app.register_blueprint(admins)
    app.register_blueprint(anime)
    app.register_blueprint(main)
    app.register_blueprint(users)

    # DB stuff
    db.init_app(app)
    if create_db:
        with app.app_context():
            db.create_all()

    return app
