# App configuration settings#
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG_MODE = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # For security
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'