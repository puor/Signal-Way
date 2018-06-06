import os
import secrets
from functools import wraps
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message

# Self developed imports
from signalapp import app, db, bcrypt, mail
from signalapp.models import User, Button
from signalapp.forms import LoginForm


# Login Page
@app.route("/", methods=['GET', 'POST'])
def login():
	# Verifies user is logged out
	if (current_user.is_authenticated):
		return (url_for('home'))

	form = LoginForm()

	if (form.validate_on_submit()):
		user = User.query.filter_by(email=form.email.data).first()
		if (user and bcrypt.check_password_hash(user.password, form.password.data)):
			login_user(user, remember=form.remember.data)
			return (redirect(url_for('home')))
		else:
			flash('Login unsuccessful. Please check email and password')

	return (render_template('login.html', form=form))

# Logout
@app.route("/logout")
def logout():
	logout_user()
	return (redirect(url_for('login')))

# Home Page
@app.route("/home")
@login_required
def home():
	return (render_template('home.html'))

# Admin Panel
@app.route("/admin")
@login_required
def admin():
	if (User.get_user_role(current_user) != 'admin'):
		return (render_template('home.html'))

	return (render_template('admin.html'))


# User Invatation Page
@app.route("/invite")
@login_required
def invite():
	return (render_template('invite.html'))








