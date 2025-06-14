 
    let secretNumber = Math.floor(Math.random() * 100) + 1;
    let attempts = 0;

    function checkGuess() {
        const userGuess = parseInt(document.getElementById("guess").value);
        const message = document.getElementById("message");

        if (isNaN(userGuess)) {
            message.innerHTML = "❌ Please enter a valid number!";
            message.style.color = "orange";
            return;
        }

        attempts++;

        if (userGuess === secretNumber) {
            message.innerHTML = `🎉 Congratulations! You guessed the number in ${attempts} attempts!`;
            message.style.color = "green";
            document.getElementById("submitBtn").disabled = true;
            launchConfetti();
        } else if (userGuess > secretNumber) {
            message.innerHTML = "📉 Too high! Try again.";
            message.style.color = "red";
        } else {
            message.innerHTML = "📈 Too low! Try again.";
            message.style.color = "red";
        }
    }

    function restartGame() {
        secretNumber = Math.floor(Math.random() * 100) + 1;
        attempts = 0;
        document.getElementById("message").innerHTML = "";
        document.getElementById("guess").value = "";
        document.getElementById("submitBtn").disabled = false;
    }

    function launchConfetti() {
        const confettiSettings = { particleCount: 100, spread: 70, origin: { y: 0.6 } };
        if (typeof confetti === "function") {
            confetti(confettiSettings);
        } else {
            console.warn("Confetti library not loaded.");
        }
    }

    function playCelebrationSound() {
        const topSound = new Audio("{{ url_for('static', filename='Winner.mp3') }}");
        topSound.play();
    }

    window.onload = function () {
        const firstPlace = document.querySelector('.leaderboard li');
        if (firstPlace && firstPlace.textContent.includes('🥇')) {
            playCelebrationSound();
        }
    };
 
    fetch('/dashboard', {
        method: 'GET',
        credentials: 'include', // Include cookies for session management
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const leaderboard = document.querySelector('.leaderboard');
        leaderboard.innerHTML = ''; // Clear existing leaderboard
        data.forEach(entry => {
        const li = document.createElement('li');
        li.textContent = `${entry.username}: ${entry.score}`;
        if (entry.rank === 1) {
            li.innerHTML = `🥇 ${li.textContent}`;
        } else if (entry.rank === 2) {
            li.innerHTML = `🥈 ${li.textContent}`;
        } else if (entry.rank === 3) {
            li.innerHTML = `🥉 ${li.textContent}`;
        }
        leaderboard.appendChild(li);
        });
    })
    .catch(error => console.error('Error fetching leaderboard:', error));

