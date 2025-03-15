# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/charactersheet')
@login_required
def charactersheet():
    return render_template('charactersheet.html')
    
@main.route('/inventorymanagement')
@login_required
def inventorymanagement():
    return render_template('inventorymanagement.html')

@main.route('/playerstats')
@login_required
def playerstats():
    return render_template('playerstats.html')    
