from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Todos
from flask_login import login_user, logout_user, current_user, login_required
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		user = User.query.filter_by(username=username).first()
		if user:
			if check_password_hash(user.password,password):
				flash('Logged in successfully!')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Incorrect password!!')
		else:
			flash('Username not found!!')

	return render_template('login.html', user = current_user, todos = Todos.query.all())

@auth.route('/sign-up', methods = ['POST', 'GET'])
def sign_up():
	if request.method == 'POST':
		username = request.form.get('username')
		email = request.form.get('email')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		email_exists = User.query.filter_by(email=email).first()
		username_exists = User.query.filter_by(username=username).first()
		print(email_exists)

		if email_exists:
			flash('email already exists!!')
		elif username_exists:
			flash('Username already exists!!')
		elif password1 != password2:
			flash('Error while confirming password!!')
		else:
			new_user = User(username=username, email=email, password=generate_password_hash(password2, method='sha256'))
			db.session.add(new_user)
			db.session.commit()
			flash('User created!')
			login_user(new_user, remember=True)
			return redirect(url_for('views.home'))

	return render_template('sign-up.html', user = current_user, todos = Todos.query.all())

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('views.home'))