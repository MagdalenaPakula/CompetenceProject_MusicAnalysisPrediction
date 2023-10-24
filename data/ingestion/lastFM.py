import requests
import json

API_KEY = '70873b1af1d3040e6a569544aff7159e'
USER_AGENT = 'Dataquest'


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def lastfm_get(payload):
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    response = requests.get(url, headers=headers, params=payload)
    return response


def fetch_lastfm_track_data():
    payload = {
        'method': 'chart.gettoptracks',
        'limit': 100  # Specify the number of top tracks you want to retrieve
    }

    r = lastfm_get(payload)

    if r.status_code == 200:
        data = r.json()

        jprint(data)

        # Save the data in a JSON file
        with open('lastfm_data.json', 'w') as file:
            json.dump(data, file)
    else:
        print(f"Failed to fetch data. Status code: {r.status_code}")


# Usage
fetch_lastfm_track_data()
