from datetime import datetime
from kaguya import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Many-2-Many Table for User<->Anime
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.id'), primary_key=True))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(20), unique=False, nullable=False, 
        default="profile-default.png")
    email = db.Column(db.String(100), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)
    anime_list = db.relationship('UserAnime', backref='user', lazy=True)
    liked_animes = db.relationship('Anime', secondary=likes, lazy='dynamic',
        backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('username: {self.username}', 'email: {self.email}',\
        'datetime_created: {self.datetime_created}')"


class UserAnime(db.Model):
    # many to one with users
    # many to one with anime
    id = db.Column(db.Integer, primary_key=True)
    datetime_created = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    status = db.Column(db.String(15), nullable=False, default='Watch List')
    episodes_watched = db.Column(db.Integer, nullable=False, default=0)
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
    title = db.Column(db.String(60), unique=True, nullable=False)
    type = db.Column(db.String(10), nullable=True, default='TV')
    episodes = db.Column(db.Float, nullable=True, default=0.)
    rating = db.Column(db.String(50), nullable=True)
    score = db.Column(db.Float, nullable=True, default=0.)
    status = db.Column(db.String(20), default='Finished')
    premiered = db.Column(db.String(), nullable=True)
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
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), nullable=False)

    def __repr__(self):
        return f"Review('content: {self.content}', 'rating: {self.rating}',\
        'anime_id: {self.anime_id}', datetime_created: {self.datetime_created}')"
