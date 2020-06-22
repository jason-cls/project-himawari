import os.path as op
from kaguya.models import User
from pathlib import Path
from flask import redirect, url_for
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

class UserView(ModelView):
    column_filters = ('id', 'username', 'email', 'role')
    column_searchable_list = ['id', 'username', 'email', 'image_file', 
        'datetime_created'] 
    column_list = ('id', 'username', 'email', 'image_file','role', 'datetime_created')
    page_size = 10

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_administrator()
        else:
            return False
    def inaccessible_callback(self):
        return redirect(url_for('users.login'))


class AnimeView(ModelView):
    column_searchable_list = ['title'] 
    column_filters = ('id', 'title', 'status')
    column_list = ('id', 'title', 'episodes', 'rating', 
        'status','premiered','image_file', 'datetime_created')
    page_size = 10

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_administrator()
        else:
            return False

    def inaccessible_callback(self):
        return redirect(url_for('users.login'))


class ReviewView(ModelView):
    column_list = ('user_id', 'anime_id', 'content', 'rating', 
        'datetime_created')
    column_filters = ('user_id', 'anime_id')
    page_size = 10

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_administrator()
        else:
            return False

    def inaccessible_callback(self):
        return redirect(url_for('users.login'))


class UserAnimeView(ModelView):
    column_list = ('id', 'user_id','anime_id', 'status', 'episodes_watched',
        'datetime_created')
    column_filters = ('user_id', 'anime_id')
    page_size = 10

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_administrator()
        else:
            return False
    def inaccessible_callback(self):
        return redirect(url_for('users.login'))


class StaticFileView(FileAdmin):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_administrator()
        else:
            return False

    def inaccessible_callback(self):
        return redirect(url_for('users.login'))
