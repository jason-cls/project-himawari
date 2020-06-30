from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from kaguya.models import Anime, Review, UserAnime
from kaguya.anime.forms import ReviewForm, EmptyForm, EpisodeForm
from kaguya import db
from wtforms.validators import NumberRange


anime = Blueprint('anime_bp', __name__)


@anime.route('/anime/<anime_id>', methods=['GET', 'POST'])
def anime_gen(anime_id):
    q_anime = Anime.query.filter_by(id=anime_id).first_or_404()
    reviews = Review.query.filter_by(anime_id=anime_id).order_by(Review.datetime_created.desc())
    if current_user.is_anonymous:
        flash('Sign in to track anime and leave reviews.', 'info')
        return render_template('anime.html', anime=q_anime, reviews=reviews)

    else:
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        form = ReviewForm()
        emptyForm = EmptyForm()
        episodeForm = EpisodeForm()
        episodeForm.eps_count.validators = [NumberRange(min=0, max=q_anime.episodes)]

        if form.validate_on_submit():
            review = Review(content=form.review.data, user=current_user, anime_id=anime_id, rating=user_anime.rating)
            db.session.add(review)
            db.session.commit()
            flash('Your review has been posted!', 'info')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))

        if episodeForm.validate_on_submit():
            if user_anime is None:
                user_anime = UserAnime(
                    status='Untracked',
                    episodes_watched=episodeForm.eps_count.data,
                    rating=None,
                    favorite=False,
                    user_id=current_user.id,
                    anime_id=anime_id)
                db.session.add(user_anime)
            else:
                user_anime.episodes_watched = episodeForm.eps_count.data
            db.session.commit()
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
        elif len(episodeForm.eps_count.errors) != 0:
            flash('Invalid episode input.', 'warning')
            return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))

        return render_template('anime.html', anime=q_anime, reviews=reviews, user_anime=user_anime,
                               form=form, emptyForm=emptyForm, episodeForm=episodeForm)


@anime.route('/favorite/<anime_id>', methods=['POST'])
@login_required
def favorite(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                        status='Untracked',
                        episodes_watched=0,
                        rating=None,
                        favorite=True,
                        user_id=current_user.id,
                        anime_id=anime_id)
            db.session.add(user_anime)
        else:
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
            user_anime = UserAnime(
                        status='Untracked',
                        episodes_watched=0,
                        rating=None,
                        favorite=False,
                        user_id=current_user.id,
                        anime_id=anime_id)
            db.session.add(user_anime)
        else:
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
            user_anime = UserAnime(
                        status='Watching',
                        episodes_watched=0,
                        rating=None,
                        favorite=False,
                        user_id=current_user.id,
                        anime_id=anime_id)
            db.session.add(user_anime)
        else:
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
            user_anime = UserAnime(
                status='Completed',
                episodes_watched=0,
                rating=None,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
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
            user_anime = UserAnime(
                status='On Hold',
                episodes_watched=0,
                rating=None,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
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
            user_anime = UserAnime(
                status='Dropped',
                episodes_watched=0,
                rating=None,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
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
            user_anime = UserAnime(
                status='Plan to Watch',
                episodes_watched=0,
                rating=None,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.status = 'Plan to Watch'
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate0/<anime_id>', methods=['POST'])
@login_required
def rate0(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=0,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 0
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate1/<anime_id>', methods=['POST'])
@login_required
def rate1(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=1,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 1
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate2/<anime_id>', methods=['POST'])
@login_required
def rate2(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=2,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 2
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate3/<anime_id>', methods=['POST'])
@login_required
def rate3(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=3,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 3
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate4/<anime_id>', methods=['POST'])
@login_required
def rate4(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=4,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 4
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate5/<anime_id>', methods=['POST'])
@login_required
def rate5(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=5,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 5
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate6/<anime_id>', methods=['POST'])
@login_required
def rate6(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=6,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 6
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate7/<anime_id>', methods=['POST'])
@login_required
def rate7(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=7,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 7
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate8/<anime_id>', methods=['POST'])
@login_required
def rate8(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=8,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 8
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate9/<anime_id>', methods=['POST'])
@login_required
def rate9(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=9,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 9
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/rate10/<anime_id>', methods=['POST'])
@login_required
def rate10(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=0,
                rating=10,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.rating = 10
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
    else:
        return redirect(url_for('main.home'))


@anime.route('/plusEpisode/<anime_id>', methods=['POST'])
@login_required
def plusEpisode(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        if user_anime is None:
            user_anime = UserAnime(
                status='Untracked',
                episodes_watched=1,
                rating=None,
                favorite=False,
                user_id=current_user.id,
                anime_id=anime_id)
            db.session.add(user_anime)
        else:
            user_anime.episodes_watched = user_anime.episodes_watched + 1
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))


@anime.route('/minusEpisode/<anime_id>', methods=['POST'])
@login_required
def minusEpisode(anime_id):
    form = EmptyForm()
    if form.validate_on_submit():
        user_anime = UserAnime.query.filter_by(anime_id=anime_id, user_id=current_user.id).first()
        user_anime.episodes_watched = user_anime.episodes_watched - 1
        db.session.commit()
        return redirect(url_for('anime_bp.anime_gen', anime_id=anime_id))
