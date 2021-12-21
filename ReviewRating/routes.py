from re import search
from flask import render_template, url_for, flash, redirect, request, abort, session
from ReviewRating import app, bcrypt, db
from ReviewRating.forms import LoginForm, SignupForm, SearchForm, ReviewForm
from ReviewRating.models import Movies, User
from flask_login import login_user, current_user, logout_user, login_required
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from ReviewRating.ml import RecommenderNet
from ReviewRating.ml import Output

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)		
			return redirect(url_for('home'))
	return render_template('login.html', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = SignupForm()
	print(form.username.data, form.email.data, form.password.data)
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('signup.html', form=form)

@app.route("/movie", methods=['GET', 'POST'])
@login_required
def movie():
	return render_template('movie.html')

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
	return render_template('home.html')

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route("/review/<id>", methods=['GET', 'POST'])
@login_required
def review(id):
	movie = Movies.query.get_or_404(id)
	form = ReviewForm()
	rating = round(movie.rating, 2)
	img_file = url_for('static', filename='movie_pics/' + id + '.jpg')
	if form.validate_on_submit():
		model_test = load_model('finalized_model.h5')
		with open('tokenizer.pickle', 'rb') as handle:
			tokenizer_test = pickle.load(handle)

		return redirect(url_for('home'))
	return render_template('review.html', movie=movie, form=form, rating=rating, img_file=img_file)

@app.route("/recommendations",methods=['GET','POST'])
@login_required
def recommendations():
	o = Output()
	recommended,top,user_id = o.result()
	recommended = pd.DataFrame(recommended)
	top = pd.DataFrame(top)
	return render_template('review.html',recommended=recommended,top=top,user_id = user_id)

@app.route("/aboutUs",methods=['GET','POST'])
@login_required
def about():
	return render_template('about.html')

