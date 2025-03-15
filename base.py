# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

googleKey = "AIzaSyCco0U7c9RmqgINw0xxqBC_TgK80L2X0UE"

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/traffic')
@login_required
def traffic():
    return render_template('traffic.html',googleKey=googleKey)
    
@main.route('/parking')
@login_required
def parking():
    return render_template('parking.html')

@main.route('/scooter')
@login_required
def scooter():
    return render_template('scooter.html')    
