import os
import random
import secrets
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db  # Import the User model and db from the models module
import routes # Replace with the actual routes you need
from routes import main, init_app  # Import the main blueprint from routes

# Initialize Flask App and other components
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

              
# Create App Factory Function
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configuration from config.py@app.before_request

    def check_session():
        if 'user_id' not in session:
            print("User is not logged in!")
    # Set app configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:9257postgres@localhost:5432/numberdb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    SECRET_KEY = os.getenv('SECRET_KEY', '9fb5385369890ee6e709cae9d14306fff716fd81d5338058392c322e99204a3a')
    app.config['SECRET_KEY'] = SECRET_KEY
    
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'

    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevents JavaScript access to cookies
     
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes']


    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Import routes after app is initialized to avoid circular imports
    
    app.register_blueprint(main)  # Register the main blueprint
    init_app(app)  # Initialize the app with routes

   # app.register_blueprint(routes.auth)  # Register the auth blueprint

    return app


# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Run the application
if __name__ == "__main__":
    app = create_app()  # Use the app factory
    # Only run this in development, not in production.
    if app.config['DEBUG']:
        with app.app_context():
            db.create_all()  # Create all tables (only in development)

    app.run(host='0.0.0.0', port=5000)

