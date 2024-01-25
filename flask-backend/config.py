from dotenv import load_dotenv
import os

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CLIENT_SECRET"]
    REDIRECT_URI = os.environ["REDIRECT_URI"]
    SESSION_COOKIE_NAME = 'Spotify Cookie'
