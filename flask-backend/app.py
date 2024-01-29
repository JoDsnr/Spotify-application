from config import ApplicationConfig
import spotipy
from spotipy.exceptions import SpotifyException
from flask import Flask, request, url_for, session, redirect, Response
from flask.json import jsonify
from flask_cors import CORS 
from flask_bcrypt import Bcrypt
from models import db, User
from scripts.authentification import create_auth_url, get_token_from_code, get_token_from_session, set_token
import requests


# initialize Flask app
app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
<<<<<<< HEAD
CORS(app, supports_credentials=True)
#server_session = Session(app)
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
    # return redirect(auth_url)




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



=======
CORS(app)

@app.route('/')
def hello():
    return redirect(url_for('login', _external=True))

@app.route('/login')
def login():
    auth_url = create_auth_url()
    return redirect(auth_url)

>>>>>>> f9670b91c89aadfd2cdb7bf4f9c3761bee5f4230
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
<<<<<<< HEAD
            # return redirect(url_for('dashboard_viz', _external=True))
            return redirect('http://localhost:3000/dashboard')
=======
            return redirect(url_for('dashboard_viz', _external=True))
>>>>>>> f9670b91c89aadfd2cdb7bf4f9c3761bee5f4230
        
        except requests.exceptions.HTTPError as http_err:
            return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
        except SpotifyException as spot_err:
            return jsonify({'error': f'Spotify API error occurred: {spot_err}'}), 500
        except Exception as err:
            return jsonify({'error': f'Unexpected error occurred: {err}'}), 500
<<<<<<< HEAD

# route to dashboard data 
=======
        
@app.route('/home')
def home():
    return "Welcome to the app's home page"

>>>>>>> f9670b91c89aadfd2cdb7bf4f9c3761bee5f4230

@app.route('/dashboard')
def dashboard_viz():
    try: 
<<<<<<< HEAD
        # get the token info from the session
        token_info = get_token_from_session()

=======
        # get the token info
        token_info = get_token_from_session()
>>>>>>> f9670b91c89aadfd2cdb7bf4f9c3761bee5f4230
    except:
        print('User not logged in')
        return redirect("/login")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
    top_artists_names = [artist['name'] for artist in (top_artists['items'])]

    return jsonify({'top_artists': top_artists_names})

<<<<<<< HEAD


@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


app.run(debug=True)
=======
if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> f9670b91c89aadfd2cdb7bf4f9c3761bee5f4230

