from flask import Blueprint, render_template, current_app, request, url_for
from flask_login import login_required
from kaguya.decorators import admin_required, permission_required
from kaguya.models import Anime, Review, UserAnime
from kaguya import db
from sqlalchemy import func, desc
from werkzeug.exceptions import BadRequestKeyError, HTTPException


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


@main.route('/reviews', methods=['GET', 'POST'])
def reviews():
    n_reviews_per_page = current_app.config['NUM_REVIEWS_PER_PAGE']
    page = request.args.get('page', 1, type=int)
    q_reviews = Review.query.order_by(Review.datetime_created.desc())

    # Filter queries
    if len(request.form) != 0:
        q_reviews = Review.query
        ratingFilter = request.form.get('ratingRadios')

        if ratingFilter == 'lowest rating':
            q_reviews = q_reviews.order_by(Review.rating)
        elif ratingFilter == 'highest rating':
            q_reviews = q_reviews.order_by(Review.rating.desc())

        timeFilter = request.form.get('timeRadios')
        if timeFilter == 'oldest':
            q_reviews = q_reviews.order_by(Review.datetime_created)
        elif timeFilter == 'recent':
            q_reviews = q_reviews.order_by(Review.datetime_created.desc())

    # Pagination
    q_reviews = q_reviews.paginate(page, n_reviews_per_page, True)
    if q_reviews.has_prev:
        prev_url = url_for('main.reviews', page=q_reviews.prev_num)
    else:
        prev_url = None
    if q_reviews.has_next:
        next_url = url_for('main.reviews', page=q_reviews.next_num)
    else:
        next_url = None
    return render_template('reviews.html', title='User Reviews', reviews=q_reviews.items,
                           prev_url=prev_url, next_url=next_url)


@main.route('/explore')
@admin_required  # Just example for how to use this admin decorator
def explore():
    n_anime_per_page = 12
    page = request.args.get('page', 1, type=int)
    q_anime = Anime.query.order_by(Anime.id)

    # Pagination
    q_anime = q_anime.paginate(page, n_anime_per_page, True)
    if q_anime.has_prev:
        prev_url = url_for('main.explore', page=q_anime.prev_num)
    else:
        prev_url = None
    if q_anime.has_next:
        next_url = url_for('main.explore', page=q_anime.next_num)
    else:
        next_url = None
    return render_template('explore.html', title="Browse Anime", animes=q_anime.items,
                           prev_url=prev_url, next_url=next_url)
