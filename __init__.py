# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from functools import wraps
import logging


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    # Test Log levels
    app.logger.debug("debug log info")
    app.logger.info("Info log information")
    app.logger.warning("Warning log info")
    app.logger.error("Error log info")
    app.logger.critical("Critical log info")
    
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

    db.init_app(app)
    with app.app_context():
        db.create_all()
	    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    def role_required(role):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if current_user.is_authenticated and current_user.role == role:
                    return func(*args, **kwargs)
                else:
                    flash('You do not have permission to access this page.', 'danger')
                    return redirect(url_for('index'))  # Redirect to some page if not authorized
            return wrapper
        return decorator
    
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .base import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
  
    if __name__ == "__main__":
        app.run(debug=True)
