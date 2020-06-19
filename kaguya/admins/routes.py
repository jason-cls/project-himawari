from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from kaguya import db, admin
from kaguya.models import User, Anime, UserAnime, Review
from kaguya.admins.views import UserView, AnimeView

admin_bp = Blueprint('admin_bp', __name__)

admin.add_view(UserView(User, db.session))
admin.add_view(AnimeView(Anime, db.session))
admin.add_view(ModelView(UserAnime, db.session))
admin.add_view(ModelView(Review, db.session))