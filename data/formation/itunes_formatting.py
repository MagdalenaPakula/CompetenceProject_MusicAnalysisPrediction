import json
import pandas as pd

def format_itunes_data(input_json, output_json):
    with open(input_json, "r") as json_file:
        itunes_data = json.load(json_file)

    formatted_data = []
    for track in itunes_data:
        formatted_track = {
            "Track Name": track["Song Title"],
            "Artist Name": track["Artist"],
            "Category": track["Category"],
            "Price": track["Price"],
            "Release Date": track["Release Date"],
        }
        formatted_data.append(formatted_track)

    formatted_df = pd.DataFrame(formatted_data)

    formatted_df.to_json(output_json, orient="records", indent=4)

# Deezer
input_json_itunes = '../../data/ingestion/itunes_data.json'
output_json_deezer = 'itunes_formatted_data.json'
format_itunes_data(input_json_itunes, output_json_deezer)
