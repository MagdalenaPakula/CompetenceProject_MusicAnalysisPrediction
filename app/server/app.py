import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"    
# import tensorflow as tf
import base64
import io
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


app = Flask(__name__, static_folder='frontend')
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


# TODO: Implement when we have model
# @app.before_first_request
# def get_model():
#     global model
#     model = tf.keras.models.load_model('./model/digits_recognition')

def generate_pseudorandom_number(input_string):
    hash_value = hash(input_string)
    mapped_value = hash_value % 101
    
    return mapped_value


@app.route('/api/search', methods=['POST'])
def search():
    title = request.json.get('title')
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='d4580256b4c14d8b95bd51ebddaa4932', client_secret='cce224a46930456f827406bdfd8b0359'))
    results = spotify.search(q=title, type='track', limit=5)

    response = jsonify({
        'tracks': list(map(lambda t : {
                'title': t["name"],
                'artists': ", ".join(list(map(lambda a : str(a["name"]), t["artists"]))),
                'id': t["id"],
                'img': t["album"]["images"][0]["url"],
                'preview': t['preview_url']
            }, 
            results["tracks"]["items"]))
        })

    return response


@app.route('/api/predict_popularity', methods=['POST'])
def echo():
    track_id = request.json.get('id')
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='d4580256b4c14d8b95bd51ebddaa4932', client_secret='cce224a46930456f827406bdfd8b0359'))
    track_response = spotify.track(track_id)
    title = track_response["name"]
    popularity = track_response["popularity"]
    result = spotify.audio_features([track_id])[0]

    response = jsonify({
        'popularity': popularity,
        'title': title,
        'metrics': {
            'danceability': result["danceability"],
            'energy': result["energy"],
            'loudness': result["loudness"],
            'speechiness': result["speechiness"],
            'acousticness': result["acousticness"],
            'instrumentalness': result["instrumentalness"],
            'liveness': result["liveness"],
            'valence': result["valence"],
            'tempo': result["tempo"]
        }
    })

    # if (genre and title):
    #     response = jsonify({'prediction': str(np.argmax(prediction[0])), 'probability': str(np.max(prediction[0]))})
    
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
