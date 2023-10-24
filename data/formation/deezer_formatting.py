import json
import pandas as pd

def format_deezer_data(input_json, output_json):
    with open(input_json, "r") as json_file:
        deezer_data = json.load(json_file)

    formatted_data = []
    for track in deezer_data:
        formatted_track = {
            "Track Name": track["title"],
            "Artist Name": track["artist"]["name"],
            "Rank": track["rank"],
            "Duration": track["duration"],
            "Explicit Content Lyrics": track["explicit_content_lyrics"],
            "Explicit Content Cover": track["explicit_content_cover"],
            "Time Add": track["time_add"],
            "Artist ID": track["artist"]["id"],
            "Artist Type": track["artist"]["type"],
            "Album ID": track["album"]["id"],
            "Album Type": track["album"]["type"],
            "Type": track["type"]
        }
        formatted_data.append(formatted_track)

    formatted_df = pd.DataFrame(formatted_data)

    formatted_df.to_json(output_json, orient="records", indent=4)

# Deezer
input_json_deezer = '../../data/ingestion/deezer_data.json'
output_json_deezer = 'deezer_formatted_data.json'
format_deezer_data(input_json_deezer, output_json_deezer)
