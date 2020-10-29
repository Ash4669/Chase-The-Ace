# chaseTheAce.py

from flask import Blueprint, render_template, redirect, url_for, session
import configparser
from ..auth import auth as auth_blueprint

config = configparser.ConfigParser()
config.read("card_games_website/settings.conf")

chase_the_ace = Blueprint('chase_the_ace',__name__)

@chase_the_ace.route('/play/chase_the_ace')
def chase_the_ace_index():
    fullName = session.get('userFullName')
    return render_template('games/chase_the_ace/index.html', fullName=fullName)

@chase_the_ace.route('/play/chase_the_ace/<roomId>')
def chase_the_ace_instance(roomId):

    # Saving the game id into the session.
    session['roomId'] = roomId
    return render_template('games/chase_the_ace/game.html', roomId=roomId)
