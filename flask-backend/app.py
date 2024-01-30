from config import ApplicationConfig
import spotipy
from spotipy.exceptions import SpotifyException
from flask import Flask, request, url_for, session, redirect, Response
from flask.json import jsonify
from flask_cors import CORS 
from flask_bcrypt import Bcrypt
from flask_session import Session
from models import db, User
from scripts.authentification import create_auth_url, get_token_from_code, get_token_from_session, set_token
import requests


# initialize Flask app
app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'


@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 

@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    session["user_id"] = new_user.id

    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_auth_url()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "spotifyAuthorizationUrl": auth_url
    })




@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })



@app.route('/redirect')
def callback() -> Response:
    session.clear()
    if 'error' in request.args:
        # Handle authorization errors
        error_message = request.args['error']
        return jsonify({'error': error_message}), 400  
    elif 'code' in request.args:
        # Authorization code received, proceed with token exchange
        try:
            token_info = get_token_from_code(code=request.args['code'])
            set_token(token_info)
            # return redirect(url_for('dashboard_viz', _external=True))
            return redirect('http://localhost:3000/dashboard')
        
        except requests.exceptions.HTTPError as http_err:
            return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
        except SpotifyException as spot_err:
            return jsonify({'error': f'Spotify API error occurred: {spot_err}'}), 500
        except Exception as err:
            return jsonify({'error': f'Unexpected error occurred: {err}'}), 500

# route to dashboard data 

@app.route('/dashboard')
def dashboard_viz():
    try: 
        # get the token info from the session
        token_info = get_token_from_session()

    except:
        print('User not logged in')
        return redirect("/login")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
    # top_artists_names = [artist['name'] for artist in (top_artists['items'])]

    # Extract relevant information including name and image
    top_artists_data = [
        {
            'name': artist['name'],
            'image': artist['images'][0]['url'] if artist['images'] else None
        }
        for artist in top_artists['items']
    ] 

    # Fetch recently played albums
    recently_played = sp.current_user_recently_played(limit=20)
    recently_played_data = [
        {
            'album_name': item['track']['album']['name'],
            'artist_name': item['track']['artists'][0]['name'],
            'image': item['track']['album']['images'][0]['url'] if item['track']['album']['images'] else None
        }
        for item in recently_played['items']
    ]   

    return jsonify({'top_artists': top_artists_data, 'recently_played': recently_played_data})



@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)

