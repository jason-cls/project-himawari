from flask import Blueprint, render_template
from kaguya.models import Anime


anime = Blueprint('anime_bp', __name__)


# For layout testing
@anime.route('/anime')
def anime_gen():
    return render_template('anime.html')


# @anime.route('/anime/<anime_id>')
# def anime_gen(anime_id):
#     q_anime = Anime.query.filter_by(id=anime_id).first_or_404()
#     return render_template('anime.html', anime=q_anime)
