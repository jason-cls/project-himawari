from flask import Blueprint, render_template
from flask_login import login_required
from kaguya.decorators import admin_required, permission_required

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title="Home Page")

@main.route('/about')
@admin_required # Just example for how to use this admin decorater
def about():
    return render_template('base.html', title="Home Page")
