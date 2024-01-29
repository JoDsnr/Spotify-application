from config import ApplicationConfig
from flask import url_for, session
import urllib.parse
from datetime import datetime
import requests
from typing import Dict

def create_auth_url()->str:
    scope = 'user-top-read'

    params = {
        'client_id': ApplicationConfig.CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': url_for('callback', _external=True),
        'show_dialog': True,
    }

    auth_url = f"{ApplicationConfig.AUTH_URL}?{urllib.parse.urlencode(params)}"
    return auth_url

def get_token_from_code(code: str)->Dict[str,str]:
    request_body = {
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': url_for('callback', _external=True),
                'client_id': ApplicationConfig.CLIENT_ID,
                'client_secret': ApplicationConfig.CLIENT_SECRET
            }
        
    response = requests.post(ApplicationConfig.TOKEN_URL, data=request_body)
    token_info = response.json()
    return token_info

def get_token_from_session()->Dict[str,str]:
    if 'token_info' not in session:
        return url_for('login', _external=True)
    if datetime.now().timestamp() > session['token_info']['expires_at']:
        return refresh_token(session['token_info']['refresh_token'])
    return session['token_info']

def set_token(token_info : Dict[str,str])-> None:
    session['token_info'] = {
                  'access_token': token_info['access_token'],
                  'refresh_token': token_info['refresh_token'],
                  'expires_at': datetime.now().timestamp() + token_info['expires_in']  # Token lasts an hour
                }

def refresh_token(refresh_token: str)->Dict[str,str]:
    print('Token expired, refreshing ...')
    request_body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': ApplicationConfig.CLIENT_ID,
        'client_secret': ApplicationConfig.CLIENT_SECRET
    }
    response = requests.post(ApplicationConfig.TOKEN_URL, data=request_body)
    new_token_info = response.json()
    return new_token_info