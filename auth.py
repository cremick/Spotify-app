from dotenv import load_dotenv
import os
from requests import post, get
import base64
import json
import flask 

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_token():
    # Urls
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    # Request User Authorization
    auth_code = get(AUTH_URL, {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8888/callback',
        'scope': 'playlist-modify-public playlist-modify-private user-read-private user-read-email',
    })

    # Get code
    print(auth_code.url)
    code = input('Enter code: ')

    # Authorization headers and data
    auth_header = base64.urlsafe_b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode())

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + str(auth_header, 'utf-8')
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:8888/callback',
    }

    # Request Access Token
    result = post(url=TOKEN_URL, data=data, headers=headers)
    json_result = result.json()
    return json_result['access_token']

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}