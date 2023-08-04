from auth import get_token, get_auth_header
from requests import get, post
import json

class Account:
    # Initiates User's token and ID
    def __init__(self):
        # Set token
        self.token = get_token()

        # Get user ID
        url = 'https://api.spotify.com/v1/me'
        header = {"Authorization": "Bearer " + self.token}

        result = get(url, headers=header)
        json_result = result.json()

        self.user_id = json_result['id']

class Playlist(Account):
    def __init__(self, name):
        url = 'https://api.spotify.com/v1/users/' + self.user_id + '/playlists'
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }
        data = {
            "name": name,
            "description": "Testing spotify api",
        }

        post(url, headers=headers, data=json.dumps(data))
        self.name = name
        self.size = 0

a1 = Account()
p1 = Playlist(a1)

