# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .. import models
from .. import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    else:
        return render_template('home/login.html')

@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    else:
        return render_template('home/signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')

    user = models.User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    newUser = models.User(email=email, username=username, password=generate_password_hash(password, method='sha256'), firstName=firstName, lastName=lastName, chaseTheAceWins=0)

    db.session.add(newUser)
    db.session.commit()

    loginUserAndSetNameAndId(user, False)

    return redirect(url_for('main.profile'))

@auth.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    keepMeSignedIn = True if request.form.get('keepMeSignedIn') else False

    user = models.User.query.filter_by(email=email).first()
    user2 = models.User.query.filter_by(username=email).first()

    if user or user2:
        if check_password_hash(user.password | user2.password, password):
            loginUserAndSetNameAndId(user, keepMeSignedIn)
            return redirect(url_for('main.profile'))
        else:
            flash('Username, Email or Password Incorrect')
            return redirect(url_for('auth.login'))
    else:
        flash('Username, Email or Password Incorrect')
        return redirect(url_for('auth.login'))

def loginUserAndSetNameAndId(user, remember):
    login_user(user, remember=remember)
    session['userFullName'] = current_user.firstName + ' ' + current_user.lastName
    session['userId'] = current_user.id