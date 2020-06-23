from flask import Blueprint, render_template
from kaguya.models import Anime, Review



anime = Blueprint('anime_bp', __name__)


@anime.route('/anime/<anime_id>')
def anime_gen(anime_id):
    q_anime = Anime.query.filter_by(id=anime_id).first_or_404()
    reviews = Review.query.filter_by(anime_id=anime_id).order_by(Review.datetime_created.desc())
    return render_template('anime.html', anime=q_anime, reviews=reviews)
