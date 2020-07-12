# App configuration settings#
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG_MODE = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # For security
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    FLASK_ADMIN_SWATCH = 'darkly' # theme for admin (https://bootswatch.com/3/)
    ADMIN_EMAIL = 'admin@admin.com'
    NUM_HOMEPAGE_REVIEWS = 6  # Number of review to display on homepage
    NUM_CAROUSEL_ANIME = 12   # Number of anime to display per carousel (4 items per slide, 3 slides)
    CURRENT_SEASON = "Fall 2004"
    UPCOMING_SEASON = "Spring 2005"
    NUM_REVIEWS_PER_PAGE = 6
    NUM_ANIME_PER_PAGE = 12
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'
