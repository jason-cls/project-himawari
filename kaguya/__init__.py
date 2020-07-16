from kaguya.config import Config
from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from elasticsearch import Elasticsearch


# Extensions
db = SQLAlchemy()
admin = Admin(name='kaguya', template_mode='bootstrap3')
login_manager = LoginManager()


def create_app(create_db=False):
    # Creation of Flask-App
    app = Flask(__name__)

    # Set configuration
    app.config.from_object(Config)

    # Init admin
    admin.init_app(app)

    # Register Blueprint
    # Need to put blueprint imports here to avoid circular import error
    from kaguya.admins.routes import admin_bp
    from kaguya.anime.routes import anime
    from kaguya.main.routes import main
    from kaguya.users.routes import users
    from kaguya.errors.handlers import errors
    app.register_blueprint(admin_bp)
    app.register_blueprint(anime)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    # Search engine setup
    app.elasticsearch = Elasticsearch([app.config['SEARCHBOX_URL']]) \
        if app.config['SEARCHBOX_URL'] else None

    # Login functionality
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # DB setup
    db.init_app(app)
    if create_db:
        with app.app_context():
            db.create_all()

    migrate = Migrate(app, db)

    return app
