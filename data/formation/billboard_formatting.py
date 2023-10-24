import json
import pandas as pd
import pyarrow.parquet as pq


def format_billboard_data(input_json, output_json):
    with open(input_json, "r") as json_file:
        billboard_data = json.load(json_file)

    formatted_data = []
    for track in billboard_data["data"]:
        formatted_track = {
            "Track Name": track["name"],
            "Artist Name": track["artist"],
            "Image": track["image"],
            "Rank": track["rank"],
            "Last Week Rank": track["last_week_rank"],
            "Peak Rank": track["peak_rank"],
            "Weeks on Chart": track["weeks_on_chart"]
        }
        formatted_data.append(formatted_track)

    formatted_df = pd.DataFrame(formatted_data)

    formatted_df.to_json(output_json, orient="records", indent=4)



# Billboard
input_json = '../../data/ingestion/billboard_data.json'
output_json = 'billboard_formatted_data.json'
format_billboard_data(input_json, output_json)