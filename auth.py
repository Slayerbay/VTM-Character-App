# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired, Length 

auth = Blueprint('auth', __name__)

class MyForm(FlaskForm):
    name = StringField('name', [validators.DataRequired(), Length(min=5, max=100, message='Name must be in 5 to 100 characters')])
    password = PasswordField('password', [validators.DataRequired(), Length(min=5, max=30, message='Password must be in 5 to 30 characters')])


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['GET', 'POST'])
def login_post():

    if request.method == "GET":
        return render_template('login.html')
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()
    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    form = MyForm()
    return render_template('signup.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():
    if request.method == "GET":
        return render_template('signup.html')
    form = MyForm()

    if form.validate_on_submit():
        name = form.name.data 
        password = form.password.data 
            
        user = User.query.filter_by(name=name).first() # if this returns a user, then the email already exists in database
    
        if user: # if a user is found, we want to redirect back to signup page so user can try again  
            flash('Account already exists')
            return redirect(url_for('auth.signup'))
    
        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(name=name, password=generate_password_hash(password, method='scrypt'), role='3')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
       flash('Invalid Entry')
       return redirect(url_for('auth.signup', form=form))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    
@auth.route('/api/users')
def usercount():
    num_users = User.query.count()
    return jsonify(num_users)

