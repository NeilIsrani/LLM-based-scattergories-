import os
from dotenv import load_dotenv
from app import create_app
# from app import socketio  # Comment out if present

print("Loading .env file...")
load_dotenv()
print("OPENAI_API_KEY present:", bool(os.getenv('OPENAI_API_KEY')))

app = create_app()

if __name__ == '__main__':
    # Change socketio.run(app) to app.run()
    app.run(debug=True) 