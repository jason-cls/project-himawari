from flask import Blueprint
from kaguya import db, admin
from kaguya.models import User, Anime, UserAnime, Review
from kaguya.admins.views import UserView, AnimeView, ReviewView, UserAnimeView

admin_bp = Blueprint('admin_bp', __name__)

admin.add_view(UserView(User, db.session))
admin.add_view(AnimeView(Anime, db.session))
admin.add_view(UserAnimeView(UserAnime, db.session))
admin.add_view(ReviewView(Review, db.session))