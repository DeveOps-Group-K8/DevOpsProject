from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import LoginManager, login_user, login_required, current_user
from models import User, db
import random

main = Blueprint('main', __name__)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Redirect to login page if not authenticated

# Home Page (Landing Page)
@main.route('/')
def home():
    return render_template('index.html')

# Register Page
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Try another one!", "danger")
            return redirect(url_for('main.register'))

        # Store hashed password
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful!", "success")
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

# Login Page
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check user credentials
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Log the user in using Flask-Login
            login_user(user)  # This will manage the session automatically
            flash("Login successful!", "success")
            return redirect(url_for('main.dashboard'))  # Redirect to the dashboard
        else:
            flash("Invalid credentials! Try again.", "danger")
    
    return render_template('login.html')

# Dashboard Page
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@main.route('/guess', methods=['POST'])
@login_required
def guess_number():
    guess = request.form['guess']
    attempts = session.get('attempts', 0)
    correct_number = session.get('random_number')

    if correct_number is None:
        return jsonify({'error': 'Game not started'}), 400

    result = ''
    if str(guess) == str(correct_number):
        current_user.score += 10
        db.session.commit()
        result = 'Correct!'
        session['game_status'] = 'win'
    else:
        session['attempts'] = attempts - 1
        result = 'Wrong guess.'

    if session['attempts'] <= 0:
        result = 'Game Over'
        session['game_status'] = 'loss'

    return jsonify({
        'result': result,
        'attempts': session['attempts'],
        'score': current_user.score
    })

    
    #return jsonify({'error': 'User not found'}), 404

# Game Page (Handles Easy, Medium, Hard)
@main.route('/play/<level>', methods=['GET', 'POST'])
@login_required  # This ensures the user is logged in
def play_game(level):
    # Define level ranges
    levels = {'easy': 100, 'medium': 200, 'hard': 500}
    if level not in levels:
        flash("Invalid level selected!", "danger")
        return redirect(url_for('main.dashboard'))

    # Get the current user
    user = current_user

    # Initialize session variables if they aren't set
    if 'random_number' not in session or 'attempts' not in session or 'game_status' not in session:
        session['random_number'] = random.randint(1, levels[level])
        session['attempts'] = 7  # Total number of attempts
        session['game_status'] = None  # Track the game status (win/loss)

    # Game variables
    correct_number = session['random_number']
    attempts = session['attempts']
    game_status = session['game_status']  # 'win' or 'loss'

    # Leaderboard fetching
    leaderboard = User.query.order_by(User.score.desc()).limit(10).all()
    leaderboard_dicts = [u.to_dict() for u in leaderboard]

    if request.method == 'POST' and game_status is None:  # Only process guesses if the game isn't over
        # Get the user's guess and ensure it's a valid integer
        guess = request.form.get('guess', type=int)
        
        if guess is None:
            flash("Invalid guess! Please enter a number.", "danger")
            return redirect(url_for('main.play_game', level=level))

        # Decrease the number of attempts
        session['attempts'] -= 1

        if guess == correct_number:
            # User wins the game
            user.score += 10  # Add score for winning
            db.session.commit()
            session['game_status'] = 'win'  # Set game status to win
            flash(f"🎉 Correct! You guessed the number in {7 - session['attempts']} attempts.", "success")
            # Reset session after win
            session.pop('random_number', None)
            session.pop('attempts', None)
        elif session['attempts'] == 0:
            # Game over: User lost
            session['game_status'] = 'loss'  # Set game status to loss
            flash(f"Game Over! The correct number was {correct_number}.", "danger")
            # Reset session after loss
            session.pop('random_number', None)
            session.pop('attempts', None)
        elif guess < correct_number:
            flash("⬆ Too low! Try again.", "info")
        else:
            flash("⬇ Too high! Try again.", "info")

    session['game_status'] = 'pending'  # or 'win' / 'loss' after each guess

    return render_template('game.html', 
                           level=level, 
                           attempts=session.get('attempts', 7), 
                           score=user.score, 
                           username=user.username,
                           leaderboard=leaderboard_dicts, 
                           correct_number=correct_number,
                           game_status=game_status)

# Leaderboard
@main.route('/leaderboard')
def leaderboard():
    leaderboard_data = User.query.order_by(User.score.desc()).all()
    leaderboard = [{"username": user.username, "score": user.score} for user in leaderboard_data]
    return render_template('leaderboard.html', leaderboard=leaderboard)


# Error Handling
@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
 

# Ensure login_manager is initialized with the Flask app
def init_app(app):
    login_manager.init_app(app)
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout Route
@main.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been logged out", "info")
    
    return redirect(url_for('main.login'))