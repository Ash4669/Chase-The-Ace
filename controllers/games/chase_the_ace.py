# chase_the_ace.py

from flask import Blueprint, render_template

chase_the_ace = Blueprint('chase_the_ace',__name__)

@chase_the_ace.route('/play/chase_the_ace')
def chase_the_ace_index():
    return render_template('games/chase_the_ace.html')

@chase_the_ace.route('/play/chase_the_ace/<int:game_id>')
def chase_the_ace_instance(game_id):
    return render_template('games/chase_the_ace.html', id = game_id)
