from flask import Blueprint, render_template, current_app
from flask_login import login_required
from kaguya.decorators import admin_required, permission_required
from kaguya.models import Anime, Review, UserAnime
from kaguya import db
from sqlalchemy import func, desc


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    n_reviews = current_app.config['NUM_HOMEPAGE_REVIEWS']
    n_anime = current_app.config['NUM_CAROUSEL_ANIME']
    current_season = current_app.config['CURRENT_SEASON']
    upcoming_season = current_app.config['UPCOMING_SEASON']

    seasonal_anime = Anime.query.filter_by(premiered=current_season).limit(n_anime).all()
    popular_anime = Anime.query.join(UserAnime) \
        .group_by(UserAnime.anime_id)\
        .order_by(desc(func.count(UserAnime.anime_id)))\
        .limit(n_anime).all()
    upcoming_anime = Anime.query.filter_by(premiered=upcoming_season).order_by(Anime.score.desc()) \
        .limit(n_anime).all()
    recent_reviews = Review.query.order_by(Review.datetime_created.desc()).limit(n_reviews).all()
    return render_template('home.html', title="Home Page",
                           seasonal_anime=seasonal_anime, popular_anime=popular_anime,
                           upcoming_anime=upcoming_anime, recent_reviews=recent_reviews)


@main.route('/about')
@admin_required  # Just example for how to use this admin decorator
def about():
    return render_template('base.html', title="Home Page")
