import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"    
# import tensorflow as tf
import base64
import io
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import requests

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

    r = requests.get("https://api.spotify.com/v1/search", params={'type': 'track', 'q': title}, headers={'Authorization': 'Basic ZDQ1ODAyNTZiNGMxNGQ4Yjk1YmQ1MWViZGRhYTQ5MzI6Y2NlMjI0YTQ2OTMwNDU2ZjgyNzQwNmJkZmQ4YjAzNTk='})

    return r.text


@app.route('/api/predict_popularity', methods=['POST'])
def echo():
    genre = request.json.get('genre')
    title = request.json.get('title')
    response = jsonify({'popularity': generate_pseudorandom_number("title"+genre+title), 'title': title, 'metrics': {
        'danceability': generate_pseudorandom_number("danceability"+genre+title),
        'energy': generate_pseudorandom_number("energy"+genre+title),
        'loudness': generate_pseudorandom_number("loudness"+genre+title),
        'speechiness': generate_pseudorandom_number("speechiness"+genre+title),
        'acousticness': generate_pseudorandom_number("acousticness"+genre+title),
        'instrumentalness': generate_pseudorandom_number("instrumentalness"+genre+title),
        'liveness': generate_pseudorandom_number("liveness"+genre+title),
        'valence': generate_pseudorandom_number("valence"+genre+title),
        'tempo': generate_pseudorandom_number("tempo"+genre+title)
    }})

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
