from datetime import datetime
from kaguya import db, login_manager
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Many-2-Many Table for User<->Anime
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.id'), primary_key=True))

class Permission:
    REVIEW = 1
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.REVIEW],
            'Moderator': [Permission.REVIEW, Permission.MODERATE],
            'Administrator': [Permission.REVIEW, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(20), unique=False, nullable=False, 
        default="profile-default.png")
    email = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)
    anime_list = db.relationship('UserAnime', backref='user', lazy=True)
    liked_animes = db.relationship('Anime', secondary=likes, lazy='dynamic',
        backref=db.backref('users', lazy=True))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()    

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('username: {self.username}', 'email: {self.email}',\
        'datetime_created: {self.datetime_created}')"


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser

class UserAnime(db.Model):
    # many to one with users
    # many to one with anime
    id = db.Column(db.Integer, primary_key=True)
    datetime_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    status = db.Column(db.String(15), nullable=False, default='Untracked')
    episodes_watched = db.Column(db.Integer, nullable=False, default=0)
    favorite = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), nullable=False)

    def __repr__(self):
        return f"UserAnime('id: {self.id}', 'status: {self.status}',\
        'user_id: {self.user_id}', 'anime_id: {self.anime_id}'\
        'datetime_created: {self.datetime_created}')"


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    title = db.Column(db.String(100), unique=False, nullable=False)
    title_japanese = db.Column(db.String(100), unique=False)
    type = db.Column(db.String(10), nullable=True, default='TV')
    episodes = db.Column(db.Integer, nullable=True, default=0)
    rating = db.Column(db.String(50), nullable=True)
    score = db.Column(db.Float, nullable=True, default=0.)
    status = db.Column(db.String(20), default='Finished')
    premiered = db.Column(db.String(), nullable=True)
    broadcast = db.Column(db.String(), nullable=True)
    genres = db.Column(db.String(), nullable=True)
    synopsis = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default="anime-default.jpg")
    reviews = db.relationship('Review', backref='anime', lazy=True)
    user_animes = db.relationship('UserAnime', backref='anime', lazy=True)

    def __repr__(self):
        return f"Anime('title: {self.title}', 'rating: {self.rating}',\
        'datetime_created: {self.datetime_created}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), nullable=False)

    def __repr__(self):
        return f"Review('content: {self.content}', 'rating: {self.rating}',\
        'anime_id: {self.anime_id}', datetime_created: {self.datetime_created}')"
