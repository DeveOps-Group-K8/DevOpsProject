import os
import pytest
from flask import Flask, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from app import app as flask_app, db, User  # Import your app and models
from app import create_app, db
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
from models import User  # Adjust the import to your project structure

# Initialize Flask app and database
 

# Test configuration
@pytest.fixture
def test_app():
    # Set up Flask app for testing
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9257postgres@localhost:5432/test_db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['TESTING'] = True
    app.config['DEBUG'] = False

    with app.app_context():
        yield app  # This is the fixture returning the app object

# Test client fixture
@pytest.fixture
def client(test_app):
    return test_app.test_client()

# Test database setup
@pytest.fixture
def init_db(test_app):
    with test_app.app_context():
        db.create_all()  # Make sure tables are created in the test database
        
        # Add a test user if needed
        user = User(username="testuser")
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
        
        yield db  # Test phase
        
        db.session.remove()
        db.drop_all()  # Clean up after test


# Test Home Page
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Check for some content in the page

# Test Register Route (valid and invalid cases)
def test_register_valid(client):
    response = client.post('/register', data={'username': 'newuser', 'password': 'newpassword'}, follow_redirects=True)
    assert response.status_code == 200  # Should redirect after successful registration
    assert b'Registration successful!' in response.data

def test_register_existing_user(client, init_db):
    response = client.post('/register', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
    
    assert response.status_code == 200  # Should redirect
    assert b'Username already exists' in response.data

# Test Login Route (valid and invalid cases)
def test_login_valid(client, init_db):
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
    
    # Check that login redirects to the dashboard
    assert response.status_code == 200
    #assert b'Login successful!' in response.data
    assert b'Welcome, testuser' in response.data  # User's name should be in the dashboard
    
   
    
def test_login_invalid(client, init_db):
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpassword'}, follow_redirects=True)
    
    # Check that invalid login shows an error message
    assert response.status_code == 200

    assert b'Invalid credentials! Try again.' in response.data


# Test Dashboard Route (requires login)
def test_dashboard_logged_in(client, init_db):
    # First, log the user in
    client.post('/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Welcome, testuser' in response.data  # User's name should be in the dashboard

# Test Logout Route
def test_logout(client, init_db):
    client.post('/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
    response = client.get('/logout')
    #assert response.status_code == 200
    assert response.status_code == 302  # Should redirect after logout
    response = client.get('/logout', follow_redirects=True)

    assert b'You have been logged out' in response.data
 

    #assert b'You have been logged out' in response.data

# Test Game Play (Basic functionality)
def test_game_play(client, init_db):
    client.post('/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
    
    # Play easy level
    response = client.get('/play/easy')
    assert response.status_code == 200
    assert b'Guess the number' in response.data  # Check if the game page loads

    # Make a guess
    response = client.post('/play/easy', data={'guess': '50'}, follow_redirects=True)
    assert response.status_code == 200
    assert (b'Too high!' or b'Too low!') in response.data  # Make sure we get a response about the guess

# Test Leaderboard
def test_leaderboard(client, init_db):
    client.post('/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
    response = client.get('/leaderboard')
    assert response.status_code == 200
    assert b'Leaderboard' in response.data  # Check if leaderboard content exists

# Test Guessing Number (Game logic)
def test_guess_number(client, init_db):
    # Simulate logged in user
    client.post('/login', data=dict({'username': 'testuser', 'password': 'testpassword'}), follow_redirects=True)
    
    # Start a game at easy level
    response = client.get('/play/easy')
    assert response.status_code == 200

    # Guess a number
    response = client.post('/guess', data={'guess': '50'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Correct!' in response.data or b'Wrong guess.' in response.data
