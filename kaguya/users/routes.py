from flask import Blueprint, render_template, redirect, request, url_for
from kaguya import db
from kaguya.models import User
from kaguya.users.forms import LoginForm, RegisterForm


users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('register.html', form=form, title='Register')