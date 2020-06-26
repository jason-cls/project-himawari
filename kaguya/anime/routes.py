from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from kaguya.models import Anime, Review, UserAnime
from kaguya.anime.forms import ReviewForm
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
        if form.validate_on_submit():
            review = Review(content=form.review.data, user=current_user, anime_id=anime_id)
            db.session.add(review)
            db.session.commit()
            flash('Your review has been posted!', 'info')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        return render_template('anime.html', anime=q_anime, reviews=reviews, user_anime=user_anime, form=form)
