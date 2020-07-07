from flask import Blueprint, render_template, current_app, request, url_for, session, redirect
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


@main.route('/reviews', methods=['GET', 'POST'])
def reviews():
    n_reviews_per_page = current_app.config['NUM_REVIEWS_PER_PAGE']
    page = request.args.get('page', 1, type=int)
    q_reviews = Review.query.order_by(Review.datetime_created.desc())

    # Filter queries
    if request.method == 'POST':
        session['filterForm'] = request.form.to_dict(flat=False)

    if session.get('filterForm'):
        q_reviews = Review.query
        ratingFilter = session['filterForm'].get('ratingRadios')[0]

        if ratingFilter == 'lowest rating':
            q_reviews = q_reviews.order_by(Review.rating)
        elif ratingFilter == 'highest rating':
            q_reviews = q_reviews.order_by(Review.rating.desc())

        timeFilter = session['filterForm'].get('timeRadios')[0]
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
    first_url = url_for('main.reviews', page=1)
    last_url = url_for('main.reviews', page=q_reviews.pages)

    activeFilters = session.get('filterForm')
    if not activeFilters:
        activeFilters = {}

    return render_template('reviews.html', title='User Reviews', reviews=q_reviews.items, activeFilters=activeFilters,
                           prev_url=prev_url, next_url=next_url, first_url=first_url, last_url=last_url)


@main.route('/explore', methods=['GET', 'POST'])
def explore():
    n_anime_per_page = current_app.config['NUM_ANIME_PER_PAGE']
    page = request.args.get('page', 1, type=int)
    q_anime = Anime.query.order_by(Anime.id)

    # Get tags
    tags = {'genres': [],
            'year': [],
            'season': ['Winter','Spring','Summer','Fall'],
            'status': ['Finished Airing','Currently Airing','Not yet aired'],
            'type': ['Movie','Music','TV','Special','ONA','OVA','Unknown']}
    genres_col = Anime.query.with_entities(Anime.genres).distinct().all()
    for row in genres_col:
        genres = row[0].strip('[]').replace("'", "").split(',')
        for genre in genres:
            if genre.strip() not in tags['genres']:
                tags['genres'].append(genre.strip())
    tags['genres'].sort()

    premiered_col = Anime.query.with_entities(Anime.premiered).distinct().all()
    for row in premiered_col:
        if row[0] != None:
            year = row[0].split()[1]
            if year not in tags['year']:
                tags['year'].append(year)
    tags['year'].sort()


    # Filter queries
    if request.method == 'POST':
        session['filterForm'] = request.form.to_dict(flat=False)

    if session.get('filterForm'):
        # Tags
        q_anime = Anime.query
        if session['filterForm'].get('genreCheckboxes'):
            for genre in session['filterForm'].get('genreCheckboxes'):
                q_anime = q_anime.filter(Anime.genres.contains(genre))
        year_subqueries = []
        if session['filterForm'].get('yearCheckboxes'):
            for year in session['filterForm'].get('yearCheckboxes'):
                q = q_anime.filter(Anime.premiered.contains(year))
                year_subqueries.append(q)
            q_anime = year_subqueries[0]
            for q in year_subqueries[1:]:
                q_anime = q_anime.union(q)
        season_subqueries = []
        if session['filterForm'].get('seasonCheckboxes'):
            for season in session['filterForm'].get('seasonCheckboxes'):
                q = q_anime.filter(Anime.premiered.contains(season))
                season_subqueries.append(q)
            q_anime = season_subqueries[0]
            for q in season_subqueries[1:]:
                q_anime = q_anime.union(q)
        status_subqueries = []
        if session['filterForm'].get('statusCheckboxes'):
            for status in session['filterForm'].get('statusCheckboxes'):
                q = q_anime.filter(Anime.status.contains(status))
                status_subqueries.append(q)
            q_anime = status_subqueries[0]
            for q in status_subqueries[1:]:
                q_anime = q_anime.union(q)
        type_subqueries = []
        if session['filterForm'].get('typeCheckboxes'):
            for formatType in session['filterForm'].get('typeCheckboxes'):
                q = q_anime.filter(Anime.type.contains(formatType))
                type_subqueries.append(q)
            q_anime = type_subqueries[0]
            for q in type_subqueries[1:]:
                q_anime = q_anime.union(q)

        # Ordering
        ratingFilter = session['filterForm'].get('ratingRadios')[0]
        if ratingFilter == 'lowest rating':
            q_anime = q_anime.order_by(Anime.score)
        elif ratingFilter == 'highest rating':
            q_anime = q_anime.order_by(Anime.score.desc())

        timeFilter = session['filterForm'].get('timeRadios')[0]
        if timeFilter == 'oldest':
            q_anime = q_anime.order_by(Anime.datetime_created)
        elif timeFilter == 'recent':
            q_anime = q_anime.order_by(Anime.datetime_created.desc())

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
    first_url = url_for('main.explore', page=1)
    last_url = url_for('main.explore', page=q_anime.pages)

    activeFilters = session.get('filterForm')
    if not activeFilters:
        activeFilters = {}

    return render_template('explore.html', title="Browse Anime", animes=q_anime.items,
                           tags=tags.items(), activeFilters=activeFilters,
                           first_url=first_url, last_url=last_url, prev_url=prev_url, next_url=next_url)


@main.route('/clearFilters', methods=['GET', 'POST'])
def clearFilters():
    if session.get('filterForm'):
        session.pop('filterForm')
    return redirect(url_for('main.explore'))
