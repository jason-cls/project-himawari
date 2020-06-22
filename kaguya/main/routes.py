from flask import Blueprint, render_template
from flask_login import login_required
from kaguya.decorators import admin_required, permission_required
from kaguya.models import Anime, Review, UserAnime
from kaguya import db
from sqlalchemy import func, desc

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    n_reviews = 6  # Number of review to display on homepage
    n_anime = 12  # Number of anime to display per carousel
    current_season = "Spring 2019"
    upcoming_season = "Summer 2019"

    seasonal_anime = Anime.query.filter_by(premiered=current_season).limit(n_anime).all()
    popular_anime = db.session.query(UserAnime.anime_id, func.count(UserAnime.anime_id).label("popular_count")) \
        .join(Anime) \
        .group_by(UserAnime.anime_id) \
        .order_by(desc("popular_count")) \
        .limit(n_anime).all()
    upcoming_anime = Anime.query.filter_by(premiered=upcoming_season).order_by(Anime.score.desc()) \
        .limit(n_anime).all()
    recent_reviews = Review.query.order_by(Review.datetime_created.desc()).limit(n_reviews).all()
    return render_template('home.html', title="Home Page", n_anime=n_anime,
                           seasonal_anime=seasonal_anime, popular_anime=popular_anime,
                           upcoming_anime=upcoming_anime, recent_reviews=recent_reviews)


@main.route('/about')
@admin_required  # Just example for how to use this admin decorator
def about():
    return render_template('base.html', title="Home Page")
