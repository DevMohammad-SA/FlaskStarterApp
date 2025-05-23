from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from . import db, login_manager


class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False,)
    display_name = db.Column(db.String(20), unique=True, nullable=False,)
    email = db.Column(db.String(120), unique=True, nullable=False,)
    role = db.Column(db.String(20), nullable=False, default='user')
    image_file = db.Column(db.String(120), nullable=False,
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))
