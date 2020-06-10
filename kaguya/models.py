from datetime import datetime
from kaguya import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    datetime_created = db.Column(db.DateTime, nullable=False, 
        default=datetime.utcnow)

    def __repr__(self):
        return f"Book('username: {self.username}', 'email: {self.email}',\
        'datetime_created: {self.datetime_created}')"