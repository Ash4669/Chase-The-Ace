# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home/index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('home/profile.html', name = current_user.firstName)

@main.route('/play')
def play():
    return render_template('home/play.html')