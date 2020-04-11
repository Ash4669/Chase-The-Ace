# shed.py

from flask import Blueprint, render_template

shed = Blueprint('shed',__name__)

@shed.route('/play/shed')
def shed_index():
    return render_template('games/shed/index.html')
