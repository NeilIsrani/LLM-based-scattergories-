# LLM-based Scattergories

## Overview
LLM-based Scattergories is a web-based game that brings the classic party game Scattergories to life using a Large Language Model (LLM). Players are given a letter and a set of categories, and they must come up with words that fit each category while starting with the given letter. The project leverages AI and real-time web technologies to enhance gameplay and engagement.

## Features
- **Interactive Multiplayer Gameplay**: Play with friends in real time.
- **AI-Powered Validation**: Uses an LLM to validate responses.
- **Dynamic Category Generation**: Generates unique categories each round.
- **Real-Time Scoring & Sessions**: Automatic score calculation and session tracking.
- **WebSockets for Multiplayer**: Supports live game interactions.

## Tech Stack
- **Frontend**: React.js
- **Backend**: Python Flask with WebSockets
- **AI Integration**: OpenAI API (LLM)
- **Deployment**: AWS EC2 with GitHub Actions (CI/CD)

## Installation
### Prerequisites
- Python (Flask) and Node.js installed
- OpenAI API key (for LLM integration)
- AWS EC2 instance (for deployment, optional)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/NeilIsrani/LLM-based-scattergories.git
   cd LLM-based-scattergories
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

4. Set up environment variables:
   - Create a `.env` file in the backend directory and add:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     FLASK_APP=app.py
     ```

5. Start the backend server:
   ```bash
   cd backend
   flask run
   ```

6. Start the frontend server:
   ```bash
   cd ../frontend
   npm start
   ```

7. Open the app in your browser at `http://localhost:3000`.

## Usage
1. Log in or create an account.
2. Start a new game session.
3. Receive a random letter and category list.
4. Enter words for each category within the time limit.
5. AI validates and scores responses.
6. Compare scores and start a new round!

## Deployment
The project is deployed on AWS EC2 with GitHub Actions for CI/CD. To deploy manually:
```bash
ssh user@your-ec2-instance
cd LLM-based-scattergories
sudo docker-compose up --build -d
```

## Contact
For any inquiries, you can email **neilisrani1@gmail.com**.


