from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from kaguya.models import Anime, Review, UserAnime
from kaguya.anime.forms import ReviewForm, EmptyForm
from kaguya import db


anime = Blueprint('anime_bp', __name__)


@anime.route('/anime/<anime_id>', methods=['GET', 'POST'])
def anime_gen(anime_id):
    q_anime = Anime.query.filter_by(id=anime_id).first_or_404()
    reviews = Review.query.filter_by(anime_id=anime_id).order_by(Review.datetime_created.desc())
    if current_user.is_anonymous:
        flash('Sign in to track anime and leave reviews.', 'info')
        return render_template('anime.html', anime=q_anime, reviews=reviews)
    else:
        form = ReviewForm()
        emptyForm = EmptyForm()
        if form.validate_on_submit():
            review = Review(content=form.review.data, user=current_user, anime_id=anime_id)
            db.session.add(review)
            db.session.commit()
            flash('Your review has been posted!', 'info')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        return render_template('anime.html', anime=q_anime, reviews=reviews, user_anime=user_anime,
                               form=form, emptyForm=emptyForm)


@anime.route('/favorite/<anime_id>', methods=['POST'])
@login_required
def favorite(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            flash('Unable to favorite - anime was not found in the database.', 'warning')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        user_anime.favorite = True
        db.session.commit()
        flash('Added anime to favorites!', 'success')
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/unfavorite/<anime_id>', methods=['POST'])
@login_required
def unfavorite(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            flash('Unable to unfavorite - anime was not found in the database.', 'warning')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        user_anime.favorite = False
        db.session.commit()
        flash('Removed anime from favorites.', 'success')
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/watching/<anime_id>', methods=['POST'])
@login_required
def watching(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            flash('Unable to set status - anime was not found in the database.', 'warning')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        user_anime.status = 'Watching'
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/completed/<anime_id>', methods=['POST'])
@login_required
def completed(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            flash('Unable to set status - anime was not found in the database.', 'warning')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        user_anime.status = 'Completed'
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/onhold/<anime_id>', methods=['POST'])
@login_required
def onhold(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            flash('Unable to set status - anime was not found in the database.', 'warning')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        user_anime.status = 'On Hold'
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/dropped/<anime_id>', methods=['POST'])
@login_required
def dropped(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            flash('Unable to set status - anime was not found in the database.', 'warning')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        user_anime.status = 'Dropped'
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/plantowatch/<anime_id>', methods=['POST'])
@login_required
def plantowatch(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            flash('Unable to set status - anime was not found in the database.', 'warning')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        user_anime.status = 'Plan to Watch'
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))