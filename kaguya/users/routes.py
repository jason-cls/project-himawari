from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from kaguya import db
from kaguya.models import User, UserAnime, Anime, Permission
from kaguya.decorators import permission_required
from kaguya.users.forms import (LoginForm, RegisterForm, UpdateAccountForm, 
    AnimeListFilterForm)
from kaguya.users.utils import save_picture
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # Wrong username or password
        if user is None or not user.check_password(form.password.data):
            return render_template('login.html', title='Login', form=form, 
                login_error='Invalid username or password')

        # Successful login
        else:
            flash('Logged in successfully!', 'success')
            login_user(user, remember=form.remember_me.data)

        # Check for safe redirects after login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.home'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect((url_for('main.home')))
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are now registered!", 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')


@users.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
        if form.new_password.data:
            current_user.set_password(form.new_password.data)
        elif (current_user.username == form.username.data) and \
            (current_user.email == form.email.data) and not(form.image_file.data):
            flash('No changes made to your account!', 'warning')
            return redirect(url_for('users.account'))
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.home'))

    elif request.method=="GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', form=form,
        title=current_user.username, image_file=image_file)

@users.route('/user/<int:user_id>/anime_list/<string:select_list>', methods=["GET", "POST"])
@users.route('/user/<int:user_id>/<string:user_url>/anime_list/<string:select_list>', methods=['GET', 'POST'])
@permission_required(Permission.REVIEW)
def anime_list(user_id, select_list="All", user_url=None):

    form = AnimeListFilterForm()
    # Only admin, mod, or list owner should be able to see the list
    anime_list={}

    if select_list == "All":
        statuses = ["Watching", "Untracked", "On Hold", "Plan to Watch",
            "Completed", "Dropped"]
    else:
        statuses = [str(select_list).replace("_"," ")]

    if user_id == current_user.id or (current_user.can(Permission.MODERATE)):
        anime_list = {} 
        for status in statuses:
            animelist = db.session\
            .query(Anime, UserAnime)\
            .outerjoin(Anime, UserAnime.anime_id==Anime.id)\
            .filter(UserAnime.user_id==user_id)\
            .filter(UserAnime.status==status)
            anime_list[status] = animelist
    else:
        return redirect(url_for('users.anime_list', user_id=current_user.id, select_list='All'))
    
    if request.method=="POST":
        select_list = form.select_list.data.replace(" ","_")

        return redirect(url_for('users.anime_list', user_id=current_user.id,
            select_list=select_list, user_url=current_user.username))
    
    elif request.method=="GET":
        form.select_list.data = select_list.replace(" ","_")

    return render_template('anime_list.html', title="My Anime List", animelist=anime_list, form=form)
