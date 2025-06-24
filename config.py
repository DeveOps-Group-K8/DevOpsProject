import os
from dotenv import load_dotenv
import secrets

load_dotenv()  # load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))

    # Use PROD_DATABASE_URL if set, else DATABASE_URL, else local default with port
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'PROD_DATABASE_URL',
        os.getenv('DATABASE_URL', 'postgresql://postgres:9257postgres@localhost:5432/numberdb')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DEBUG mode (default False)
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes']

    # Cookie security: use HTTPS only in production
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    REMEMBER_COOKIE_SECURE = os.getenv('REMEMBER_COOKIE_SECURE', 'True').lower() == 'true'

    # Logging
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
