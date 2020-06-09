from flask import Blueprint, render_template
from kaguya.users.forms import LoginForm

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)