from config import ApplicationConfig
import spotipy
from spotipy.exceptions import SpotifyException
from flask import Flask, request, url_for, session, redirect, Response
from flask.json import jsonify
from flask_cors import CORS 
from flask_bcrypt import Bcrypt
from flask_session import Session
from models import db, User, SpotifyHistory
from scripts.authentification import create_auth_url, get_token_from_code, get_token_from_session, set_token
from scripts.spotify_history import add_spotify_history_from_json
import requests
from collections import Counter


# initialize Flask app
app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

# Call the function to add Spotify history from JSON files
with app.app_context():
    db.create_all()
    # Check if the function has been called
    if not app.config.get('SPOTIFY_HISTORY_ADDED'):
        # Call the function to add Spotify history from JSON files
        add_spotify_history_from_json()

        # Set the flag to indicate that the function has been called
        app.config['SPOTIFY_HISTORY_ADDED'] = True


@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({
            "id": user.id,
            "email": user.email
        })
    else:
        return jsonify({"error": "User not found"}), 404
    
    
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
    top_artists = sp.current_user_top_artists(limit=5, time_range='short_term')

    # Extract relevant information including name and image
    top_artists_data = [
        {
            'name': artist['name'],
            'image': artist['images'][0]['url'] if artist['images'] else None,
            'genres': artist['genres']
        }
        for artist in top_artists['items']
    ] 

    # Fetch recently played albums
    recently_played = sp.current_user_recently_played(limit=50)

    recently_played_data = [
        {
            'album_name': item['track']['album']['name'],
            'artist_name': item['track']['artists'][0]['name'],
            'song_name': item['track']['name'],
            'image': item['track']['album']['images'][0]['url'] if item['track']['album']['images'] else None
        }
        for item in recently_played['items']
    ]   


    # Find the most listened albums based on frequency
    album_counts = Counter(album['album_name'] for album in recently_played_data)

    # Get unique albums with their play counts and image URLs
    unique_albums = [
        {
            'album_name': album_name,
            'play_count': album_counts[album_name],
            'image': next((album['image'] for album in recently_played_data if album['album_name'] == album_name), None)
        }
        for album_name in album_counts
    ]

    # Sort unique albums based on play count in descending order
    sorted_most_listened_albums = sorted(unique_albums, key=lambda x: x['play_count'], reverse=True)

    # Extract the most listened albums
    most_listened_albums = sorted_most_listened_albums

    return jsonify({'top_artists': top_artists_data, 'recently_played': recently_played_data, 'most_listened_albums': most_listened_albums})



@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)

