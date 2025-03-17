
document.addEventListener('DOMContentLoaded', function() {
    const rollDieButton = document.getElementById('roll-die');
    const dieResult = document.getElementById('die-result');
    const timerDisplay = document.getElementById('timer');
    const answerForm = document.getElementById('answer-form');
    const answerInput = document.getElementById('answer-input');
    const submitButton = document.getElementById('submit-answer');
    let timer;
    let timeLeft = 60; // 60 seconds for answers

    rollDieButton.addEventListener('click', function() {
        const result = rollDie();
        dieResult.textContent = `You rolled: ${result}`;
        startTimer();
    });

    function rollDie() {
        return Math.floor(Math.random() * 20) + 1;
    }

    function startTimer() {
        clearInterval(timer);
        timeLeft = 60;
        timerDisplay.textContent = timeLeft;

        timer = setInterval(function() {
            timeLeft--;
            timerDisplay.textContent = timeLeft;

            if (timeLeft <= 0) {
                clearInterval(timer);
                alert('Time is up! Please submit your answers.');
                answerForm.submit();
            }
        }, 1000);
    }

    answerForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const answer = answerInput.value.trim();
        if (answer) {
            // Submit the answer via AJAX or form submission
            console.log(`Answer submitted: ${answer}`);
            answerInput.value = '';
        } else {
            alert('Please enter an answer before submitting.');
        }
    });
});