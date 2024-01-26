from config import ApplicationConfig
import spotipy
from spotipy.exceptions import SpotifyException
from flask import Flask, request, url_for, session, redirect, Response
from flask.json import jsonify
from flask_cors import CORS 
from flask_bcrypt import Bcrypt
from scripts.authentification import create_auth_url,get_token_from_code, get_token_from_session, set_token
import requests


# initialize Flask app
app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app)

@app.route('/')
def hello():
    return redirect(url_for('login', _external=True))

@app.route('/login')
def login():
    auth_url = create_auth_url()
    return redirect(auth_url)

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
            return redirect(url_for('dashboard_viz', _external=True))
        
        except requests.exceptions.HTTPError as http_err:
            return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
        except SpotifyException as spot_err:
            return jsonify({'error': f'Spotify API error occurred: {spot_err}'}), 500
        except Exception as err:
            return jsonify({'error': f'Unexpected error occurred: {err}'}), 500
        
@app.route('/home')
def home():
    return "Welcome to the app's home page"


@app.route('/dashboard')
def dashboard_viz():
    try: 
        # get the token info
        token_info = get_token_from_session()
    except:
        print('User not logged in')
        return redirect("/login")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
    top_artists_names = [artist['name'] for artist in (top_artists['items'])]

    return jsonify({'top_artists': top_artists_names})

if __name__ == '__main__':
    app.run(debug=True)

