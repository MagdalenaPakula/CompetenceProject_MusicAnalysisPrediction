import requests
import json

url = 'https://itunes.apple.com/us/rss/topsongs/limit=100/json'

response = requests.get(url)

data = response.json()

song_data = []

for entry in data['feed']['entry']:
    artist_name = entry['im:artist']['label']
    song_title = entry['im:name']['label']
    song_category = entry['category']['attributes']['label']
    song_price = entry['im:price']['label']

    # Check if 'im:releaseDate' is present
    if 'im:releaseDate' in entry:
        song_release_date = entry['im:releaseDate']['label']
    else:
        song_release_date = "N/A"

    song_dict = {
        "Artist": artist_name,
        "Song Title": song_title,
        "Category": song_category,
        "Price": song_price,
        "Release Date": song_release_date
    }

    song_data.append(song_dict)

# Saving the song data to a JSON file
with open("itunes_data.json", "w") as json_file:
    json.dump(song_data, json_file)

print("Song data saved to itunes_data.json")
