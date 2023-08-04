from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPE = 'playlist-modify-public playlist-modify-private user-read-private user-read-email'
SPOTIFY = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
        
def create_playlist(name, description):
    user_details = SPOTIFY.current_user()
    user_id = user_details['id']

    result = SPOTIFY.user_playlist_create(user_id, name, True, False, description)
    return result['id']

def playlist_by_decade(decade):
    playlist_name = str(decade) + 's'
    playlist_description = 'All of your songs from the ' + playlist_name + '!'

    new_playlist_id = create_playlist(playlist_name, playlist_description)

    result = SPOTIFY.current_user_playlists(50, 1)

    num_playlists = result['total'] 
    all_playlists = result['items']

    for p in range (0, num_playlists):
        playlist_id = all_playlists[p]['id']

        result = SPOTIFY.playlist_items(playlist_id)

        num_songs = result['total']
        all_songs = result['items']

        for s in range (0, num_songs):
            song_uri = all_songs[s]['track']['uri']
            release_date = all_songs[s]['track']['album']['release_date']
            song_year = int(release_date[:4])

            if song_year >= decade or song_year <= decade + 9:
                SPOTIFY.playlist_add_items(new_playlist_id, song_uri)
    return


playlist_by_decade(1970)

