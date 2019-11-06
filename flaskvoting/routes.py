import hashlib
from flask import render_template, url_for, flash, redirect, request
from flaskvoting import app, db
from flaskvoting.forms import LoginForm, RegistrationForm
from flaskvoting.models import User 
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')
	
@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashedpass = hashlib.sha256(form.password.data.encode()).hexdigest()
		user = User(username=form.username.data, email = form.email.data, password=hashedpass)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods = ['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		enteredPassHash = hashlib.sha256(form.password.data.encode()).hexdigest()
		if user and (enteredPassHash == user.password):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login1.html', title='Login', form = form)
	
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))
	
	
@app.route('/account')
@login_required
def account():
	return render_template('account.html',title='Account')

