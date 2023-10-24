import json
import pandas as pd
import pyarrow.parquet as pq


def format_lastfm_data(input_json, output_json):
    # Read the JSON file
    with open(input_json) as json_file:
        lastfm_track_data = json.load(json_file)

    formatted_data = []
    for track in lastfm_track_data['tracks']['track']:
        formatted_track = {
            'Track Name': track['name'],
            'Artist Name': track['artist']['name'],
            'Image': track['image'][3]['#text'],  # Choose the 'extralarge' image size
            'Duration': int(track['duration']),
            'Playcount': int(track['playcount']),
            'Listeners': int(track['listeners']),
            'url': track['url']
        }
        formatted_data.append(formatted_track)

    formatted_df = pd.DataFrame(formatted_data)

    formatted_df.to_json(output_json, orient='records')

    formatted_data = pd.read_json(output_json)
    print("Formatted lastfm_track_data:")
    print(formatted_data)


# lastFM
input_json = '../../data/ingestion/lastfm_data.json'
output_json = 'lastfm_formatted_data.json'
format_lastfm_data(input_json, output_json)