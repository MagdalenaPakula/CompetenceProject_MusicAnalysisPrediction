import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the combined data
with open('../../data/combination/combined_data.json') as file:
    combined_data = json.load(file)

# Extract track features
features = []
track_names = []
for data_point in combined_data:
    track_name = data_point.get('Track Name')
    if track_name is not None and 'Audio Features' in data_point:
        audio_features = data_point['Audio Features']
        features.append([
            audio_features['danceability'],
            audio_features['energy'],
            audio_features['loudness'],
            audio_features['speechiness'],
            audio_features['acousticness'],
            audio_features['instrumentalness'],
            audio_features['liveness'],
            audio_features['valence'],
            audio_features['tempo']
        ])
        track_names.append(track_name)

# Convert features to numpy array
features = np.array(features)

# Calculate cosine similarity between tracks
cosine_similarities = cosine_similarity(features, features)


def get_similar_tracks(track_name, top_n=5):
    # Find the index of the track
    track_index = track_names.index(track_name)

    # Get the cosine similarities for the track
    track_similarities = cosine_similarities[track_index]

    # Get the indices of the top similar tracks
    similar_track_indices = np.argsort(track_similarities)[-top_n - 1:-1][::-1]

    # Get the names of the similar tracks
    similar_tracks = [track_names[i] for i in similar_track_indices]

    return similar_tracks


# Example usage
similar_tracks = get_similar_tracks('MONACO', top_n=5)
print(f"Tracks similar to MONACO:")
for track in similar_tracks:
    print(track)
