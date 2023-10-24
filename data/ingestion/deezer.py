import requests
import json

playlist_id = "3155776842"
api_url = f"https://api.deezer.com/playlist/{playlist_id}/tracks"

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    tracks = data.get('data', [])

    with open('deezer_data.json', 'w') as json_file:
        json.dump(tracks, json_file)

    print("Playlist tracks saved to deezer_data.json")
else:
    print(f"Error fetching data from Deezer API. Status code: {response.status_code}")
