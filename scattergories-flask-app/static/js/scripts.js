document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const createGameBtn = document.getElementById('create-game');
    const dieResult = document.getElementById('die-result');
    const timerDisplay = document.getElementById('timer');
    const answerForm = document.getElementById('answer-form');
    const currentLetter = document.getElementById('current-letter');
    const promptsList = document.getElementById('prompts-list');
    
    let timer;
    let timeLeft = 60;
    let currentGameId = null;

    // Event Listeners
    createGameBtn.addEventListener('click', createNewGame);
    answerForm.addEventListener('submit', function(event) {
        event.preventDefault();
        submitAnswers();
    });

    async function createNewGame() {
        try {
            const response = await fetch('/api/new-game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const gameData = await response.json();
            
            if (gameData.status === 'success') {
                currentGameId = gameData.game_id;
                
                // Update UI
                dieResult.textContent = `Die Roll: ${gameData.die_roll}`;
                currentLetter.textContent = gameData.letter;
                
                // Display prompts
                displayPrompts(gameData.prompts);
                
                // Start timer
                startTimer();
                
                // Enable answer form
                answerForm.classList.remove('d-none');
                createGameBtn.disabled = true;
            }
        } catch (error) {
            console.error('Error creating game:', error);
            alert('Failed to create game. Please try again.');
        }
    }

    function displayPrompts(prompts) {
        promptsList.innerHTML = '';
        const answersContainer = document.getElementById('answers-container');
        answersContainer.innerHTML = '';

        prompts.forEach(prompt => {
            // Add to prompts list
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = prompt.category;
            promptsList.appendChild(li);

            // Create answer input
            const inputDiv = document.createElement('div');
            inputDiv.className = 'mb-3';
            inputDiv.innerHTML = `
                <label for="answer-${prompt.category}" class="form-label">${prompt.category}</label>
                <input type="text" class="form-control answer-input" 
                       id="answer-${prompt.category}" 
                       name="${prompt.category}" 
                       placeholder="Enter your answer...">
            `;
            answersContainer.appendChild(inputDiv);
        });
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
                submitAnswers();
            }
        }, 1000);
    }

    async function submitAnswers() {
        const answers = {};
        document.querySelectorAll('.answer-input').forEach(input => {
            answers[input.name] = input.value.trim();
        });

        try {
            const response = await fetch('/api/submit-round', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    game_id: currentGameId,
                    answers: answers,
                    letter: currentLetter.textContent
                })
            });

            const result = await response.json();
            displayResults(result);
            
            // Reset game state
            createGameBtn.disabled = false;
            clearInterval(timer);
        } catch (error) {
            console.error('Error submitting answers:', error);
            alert('Failed to submit answers. Please try again.');
        }
    }

    function displayResults(results) {
        const resultsContainer = document.getElementById('results-container');
        resultsContainer.innerHTML = `
            <div class="mt-4">
                <h4>Results</h4>
                <p>Total Score: ${results.score}</p>
                ${Object.entries(results.results).map(([category, result]) => `
                    <div class="card mb-2 ${result.valid ? 'border-success' : 'border-danger'}">
                        <div class="card-body">
                            <h5 class="card-title">${category}</h5>
                            <p class="card-text">Score: ${result.valid ? '1' : '0'}</p>
                            <p class="card-text">${result.reason}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        resultsContainer.classList.remove('d-none');
    }
});