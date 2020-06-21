# App configuration settings#
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG_MODE = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # For security
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    FLASK_ADMIN_SWATCH = 'darkly' # theme for admin (https://bootswatch.com/3/)
    ADMIN_EMAIL = 'admin@admin.com'