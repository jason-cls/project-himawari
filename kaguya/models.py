from datetime import datetime
from kaguya import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(100), unique=True, nullable=False)
    datetime_created = db.Column(db.DateTime, nullable=False,
                                 default=datetime.utcnow)

    def __repr__(self):
        return f"Book('username: {self.username}', 'email: {self.email}',\
        'datetime_created: {self.datetime_created}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))