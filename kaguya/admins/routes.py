import os.path as op
from pathlib import Path
from flask import Blueprint
from kaguya import db, admin
from kaguya.models import User, Anime, UserAnime, Review
from kaguya.admins.views import (UserView, AnimeView, UserAnimeView,
    ReviewView, StaticFileView)
from flask_admin.contrib.fileadmin import FileAdmin
#from flask_admin.contrib.fileadmin.s3 import S3FileAdmin

admin_bp = Blueprint('admin_bp', __name__)

# Path to static dir
path = Path(op.dirname(__file__)).parent
path = op.join(path, 'static')

admin.add_view(UserView(User, db.session))
admin.add_view(AnimeView(Anime, db.session))
admin.add_view(UserAnimeView(UserAnime, db.session))
admin.add_view(ReviewView(Review, db.session))
admin.add_view(StaticFileView(path, '/static/', name='Static Files'))

