 
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
 
