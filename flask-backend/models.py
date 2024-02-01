from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)

class SpotifyHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endTime = db.Column(db.String(20))
    artistName = db.Column(db.String(100))
    trackName = db.Column(db.String(100))
    msPlayed = db.Column(db.Integer)