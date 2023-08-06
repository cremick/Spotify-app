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
    # empty list to store all songs
    songs = []
    
    # get playlist data
    pl_data = SPOTIFY.current_user_playlists()
    num_playlists = pl_data['total']
    playlists = pl_data['items']

    # iterate thru playlists
    for p in range(num_playlists):
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
        for s in range(num_songs):
            # add song if not already added
            if songs.count(pl_songs[s]['track']['uri']) == 0:
                songs.append(pl_songs[s]['track']['uri'])

    # get saved songs
    saved_data = SPOTIFY.current_user_saved_tracks()
    num_saved = saved_data['total']
    saves = saved_data['items']

    # iterate thru saved songs
    offset = 0
    for s in range(num_saved):
        # if limit is reached, get more songs
        if s % 20 == 0 and s > 0:
            offset = offset + 20
            saved_data = SPOTIFY.current_user_saved_tracks(offset=offset)
            saves = saved_data['items']

        # add song if not already added
        index = s % 20
        if songs.count(saves[index]['track']['uri']) == 0:
            songs.append(saves[index]['track']['uri'])

    return songs  

def playlist_by_decade(decade):
    songs = get_all_songs()

    # create new decade playlist
    playlist_name = str(decade) + 's'
    new_playlist_id = create_playlist(playlist_name)

    # iterate thru songs
    num_songs = len(songs)
    for s in range(num_songs):
        # get song info
        song = SPOTIFY.track(songs[s])
        release_date = song['album']['release_date']
        year = int(release_date[:4])

        # add song if it is the correct decade
        if year >= decade and year <= decade + 9:
            SPOTIFY.playlist_add_items(new_playlist_id, {songs[s]})