
from config import ApplicationConfig
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
from flask.json import jsonify
from flask_cors import CORS 
from flask_session import Session
from flask_bcrypt import Bcrypt



# initialize Flask app
app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app)
#server_session = Session(app)

# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'

# route to handle the login
@app.route('/')
def login():
    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    
    # redirect the user to the authorization URL
    return redirect(auth_url)

# route to handle the redirect URI after authorization

@app.route('/redirect')
def redirect_page():
    # clear the session
    session.clear()
    # get the authorization code from the request parameters
    code = request.args.get('code')
    # exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info

    # redirect the user to the dashboard_viz route
    return redirect(url_for('dashboard_viz',_external=True))

# route to dashboard data 

@app.route('/dashboard')
def dashboard_viz():
    try: 
        # get the token info from the session
        token_info = get_token()

    except:
        # if the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/")
    
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
    top_artists_names = [artist['name'] for artist in (top_artists['items'])]

    return jsonify({'top_artists': top_artists_names})


# function to get the token info from the session
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        # if the token info is not found, redirect the user to the login route
        return redirect(url_for('login', _external=False))
    
    # check if the token is expired and refresh it if necessary
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    scope = 'user-top-read'

    return SpotifyOAuth(
        client_id=ApplicationConfig.CLIENT_ID,
        client_secret=ApplicationConfig.CLIENT_SECRET,
        redirect_uri=ApplicationConfig.REDIRECT_URI,
        scope=scope,
        show_dialog=True 
    )

app.run(debug=True)

