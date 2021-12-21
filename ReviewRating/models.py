from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from ReviewRating import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): 
	id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.img_file}')"

class Movies(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
	movieName = db.Column(db.String(100), unique=True, nullable=False)
	description = db.Column(db.String(100), unique=False, nullable=False)
	rating = db.Column(db.Float(2, 1), nullable=False)
