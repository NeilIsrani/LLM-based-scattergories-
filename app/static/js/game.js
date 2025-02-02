let gameTimer;
let currentGame = null;

// DOM Elements
const startGameBtn = document.getElementById('start-game');
const submitAnswersBtn = document.getElementById('submit-answers');
const timerElement = document.getElementById('timer');
const currentLetterElement = document.getElementById('current-letter');
const categoriesListElement = document.getElementById('categories-list');
const resultsContainer = document.getElementById('results');

startGameBtn.addEventListener('click', startNewGame);
submitAnswersBtn.addEventListener('click', submitAnswers);

async function startNewGame() {
    const response = await fetch('/api/new-game', {
        method: 'POST'
    });
    const gameData = await response.json();
    handleGameStart(gameData);
}

async function submitAnswers() {
    const answers = {};
    document.querySelectorAll('.answer-input').forEach(input => {
        answers[input.name] = input.value;
    });
    
    const response = await fetch('/api/submit-round', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            answers: answers,
            letter: currentLetterElement.textContent
        })
    });
    
    const results = await response.json();
    displayResults(results);
}