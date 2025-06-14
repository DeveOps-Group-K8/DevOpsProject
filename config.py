import os
from dotenv import load_dotenv
import secrets

# Load environment variables from a .env file if available
load_dotenv()

class Config:
    # SECRET_KEY for session management and security
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))  # Environment variable with fallback


    # Database URI configuration
    # Fetch the URI from environment variables or fallback to a default value for local development
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:9257postgres@localhost:5432/number_db')

    # Disable SQLAlchemy modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable or disable debugging (turn it off in production)
    DEBUG = False

    # Additional security settings for production
    SESSION_COOKIE_SECURE = True  # Ensures the session cookie is sent only over HTTPS
    REMEMBER_COOKIE_SECURE = True  # Ensures the remember cookie is sent only over HTTPS

    # Set up logging to capture production-level logs
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT')  # Capture logs and direct them to STDOUT for cloud services
    LOG_LEVEL = 'INFO'  # Or 'ERROR' based on your needs

    # Production database URI
        # Use the production database URI if available
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL')


    