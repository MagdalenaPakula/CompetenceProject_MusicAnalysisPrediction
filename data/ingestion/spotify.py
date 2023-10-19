import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time


def fetch_spotify_data():
    # CLIENT AUTHORISATION - FOR THIS APP
    client_id = 'f941f7e0468348718970f83aaf3939f3'
    client_secret = 'dc19280dabdd4fc2807760db18ff2402'

    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # PLAYLIST LINK TO URI FOR EXTRACTING
    # Playlist "Top 100 track World"
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=787568002113444e"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_items(playlist_URI)["items"]]

    track_data = []

    for track in sp.playlist_items(playlist_URI)["items"]:
        # URI
        track_uri = track["track"]["uri"]

        # Track name
        track_name = track["track"]["name"]

        # Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)

        # Name, popularity, genre
        artist_name = artist_info["name"]
        artist_pop = artist_info["popularity"]
        artist_genres = artist_info["genres"]

        # Album
        album = track["track"]["album"]["name"]

        # Popularity of the track
        track_pop = track["track"]["popularity"]

        # Audio features of the track
        audio_features = sp.audio_features(track_uri)[0]

        # Duration of the track
        duration_ms = track["track"]["duration_ms"]
        duration_sec = duration_ms / 1000

        # Release date of the track
        release_date = track["track"]["album"]["release_date"]

        # Dictionary with the data
        track_dict = {
            "Track Name": track_name,
            "Artist Name": artist_name,
            "Artist Popularity": artist_pop,
            "Artist Genres": artist_genres,
            "Album": album,
            "Track Popularity": track_pop,
            "Release Date": release_date,
            "Duration (sec)": duration_sec,
            "Audio Features": audio_features
        }

        # Adding data to the list
        track_data.append(track_dict)

        # Pausing execution for a second to avoid rate limiting
        time.sleep(1)

    # Saving the track data to a JSON file
    with open("spotify_data.json", "w") as json_file:
        json.dump(track_data, json_file)

    print("Track data saved to spotify_track_data.json")


fetch_spotify_data()
