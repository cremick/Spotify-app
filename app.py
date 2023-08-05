from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPE = 'playlist-modify-public playlist-modify-private user-read-private user-read-email'
SPOTIFY = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
        
def create_playlist(name):
    user_details = SPOTIFY.current_user()
    user_id = user_details['id']

    result = SPOTIFY.user_playlist_create(user_id, name, True, False)
    return result['id']

def get_all_songs():
    play_result = SPOTIFY.current_user_playlists()
    
    num_playlists = play_result['total']
    all_playlists = play_result['items']

    songs = []
    for p in range(num_playlists):
        playlist_id = all_playlists[p]['id']
        song_result = SPOTIFY.playlist_items(playlist_id)

        num_songs = song_result['total']
        all_songs = song_result['items']

        for s in range(num_songs):
            if songs.count(all_songs[s]['track']['uri']) == 0:
                songs.append(all_songs[s]['track']['uri'])


    return songs       

def playlist_by_decade(decade):
    # get playlist data
    pl_data = SPOTIFY.current_user_playlists()
    num_playlists = pl_data['total']
    playlists = pl_data['items']

    # create new decade playlist
    playlist_name = str(decade) + 's'
    new_playlist_id = create_playlist(playlist_name)

    # empty list to store all songs
    songs = []

    # iterate thru playlists
    for p in range (num_playlists):
        # get playlist id
        playlist_id = playlists[p]['id']

        # get song data
        song_data = SPOTIFY.playlist_items(playlist_id)
        num_songs = song_data['total']
        # temporary fix for limit issue
        if num_songs >= 100:
            num_songs = 100
        pl_songs = song_data['items']

        # iterate thru songs
        for s in range (num_songs):
            # song info
            song_uri = pl_songs[s]['track']['uri']
            release_date = pl_songs[s]['track']['album']['release_date']
            year = int(release_date[:4])

            # check for repeats and proper date
            if (year >= decade and year <= decade + 9) and songs.count(song_uri) == 0:
                # add to list
                songs.append(song_uri)

    # add songs to playlist
    if len(songs) > 100:
        for i in range(0, len(songs), 100):
            chunk = songs[i:i + 100]
            SPOTIFY.playlist_add_items(new_playlist_id, chunk)
    else:
        SPOTIFY.playlist_add_items(new_playlist_id, songs)

playlist_by_decade(1990)
playlist_by_decade(1970)
playlist_by_decade(1960)
playlist_by_decade(1950)