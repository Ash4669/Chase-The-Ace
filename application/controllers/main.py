# main.py

from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from .. import db
from .. import models

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home/index.html')

@main.route('/profile')
@login_required
def profile():
    userId = session.get('userId')
    chaseTheAceWins = models.Users.query.filter_by(id=userId).first().chaseTheAceWins
    return render_template('home/profile.html', name=current_user.firstName, chaseTheAceWins=chaseTheAceWins)

@main.route('/play')
def play():
    return render_template('home/play.html')
