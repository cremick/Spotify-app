from auth import get_token, get_auth_header
from requests import get, post
import json

class User:
    def __init__(self, token):
        self.token = token
    
    def get_user_id(self):
        url = 'https://api.spotify.com/v1/me'
        header = {"Authorization": "Bearer " + token}

        result = get(url, headers=header)
        json_result = result.json()

        self.user_id = json_result['id']
        

def get_user_id(token):
        url = 'https://api.spotify.com/v1/me'
        headers = get_auth_header(token)

        result = get(url, headers=headers)
        json_result = result.json()

        return json_result['id']

def create_playlist(playlist_name, token):
    user_id = get_user_id(token)
    url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists'
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    data = {
        "name": playlist_name,
        "description": "Testing spotify api",
    }

    post(url, headers=headers, data=json.dumps(data))
    return

token = get_token()
u1 = User(token)