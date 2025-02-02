# filepath: /Users/khajjafar/Documents/Projects/scattergories/scattergories-flask-app/wsgi.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()