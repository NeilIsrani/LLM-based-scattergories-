document.addEventListener('DOMContentLoaded', function() {
    // ... existing variables ...
    let currentGameId = null;  // Add this to track game ID

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
                currentGameId = gameData.game_id;  // Store the game ID
                
                // ... rest of your existing game setup code ...
                
                // Display die roll result
                dieResult.textContent = `Die Roll: ${gameData.die_roll}`;
            }
        } catch (error) {
            console.error('Error creating game:', error);
            alert('Failed to create game. Please try again.');
        }
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
                    game_id: currentGameId,  // Include game ID
                    answers: answers,
                    letter: currentLetter.textContent
                })
            });

            const result = await response.json();
            displayResults(result);
        } catch (error) {
            console.error('Error submitting answers:', error);
            alert('Failed to submit answers. Please try again.');
        }
    }
}); 