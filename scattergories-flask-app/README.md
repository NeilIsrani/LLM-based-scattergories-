# Scattergories Flask App

This is a web application for the board game Scattergories, built using Flask. The application allows players to roll a 20-sided die, receive prompts, time their answers, and track scores over three games.

## Features

- Roll a 20-sided die to determine the starting letter for each round.
- Display prompts for players to answer based on the rolled letter.
- Implement a timer for each round to limit the time for answering.
- Track player scores across three games.
- User-friendly interface with responsive design.

## Project Structure

```
scattergories-flask-app
├── app
│   ├── __init__.py          # Initializes the Flask application
│   ├── routes.py            # Defines application routes
│   ├── models.py            # Contains data models for players and scores
│   ├── static
│   │   ├── css
│   │   │   └── styles.css   # Styles for the web application
│   │   └── js
│   │       └── scripts.js    # JavaScript for client-side interactions
│   ├── templates
│   │   ├── base.html        # Base template for the application
│   │   ├── index.html       # Landing page for starting/joining games
│   │   └── game.html        # Game interface for playing
│   └── utils.py             # Utility functions for game logic
├── instance
│   └── config.py            # Configuration settings for the application
├── tests
│   ├── __init__.py          # Initializes the test suite
│   ├── test_routes.py       # Unit tests for routes
│   └── test_models.py       # Unit tests for models
├── .gitignore                # Specifies files to ignore in version control
├── requirements.txt          # Lists project dependencies
└── README.md                 # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd scattergories-flask-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the configuration in `instance/config.py`.

5. Run the application:
   ```
   flask run
   ```

## Usage

- Navigate to the landing page to start a new game or join an existing one.
- Follow the prompts to play the game and submit your answers.
- Scores will be calculated and displayed at the end of each game.

## Contributing

Feel free to submit issues or pull requests to improve the application!