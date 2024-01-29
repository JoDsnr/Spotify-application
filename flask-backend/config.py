from dotenv import load_dotenv
import os

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CLIENT_SECRET"]
    SESSION_COOKIE_NAME = 'Spotify Cookie'
    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
<<<<<<< HEAD
    API_BASE_URL = "https://api.spotify.com/v1"

    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"
=======
    API_BASE_URL = "https://api.spotify.com/v1"
>>>>>>> f9670b91c89aadfd2cdb7bf4f9c3761bee5f4230
