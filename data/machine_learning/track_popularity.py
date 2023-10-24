import json
from sklearn.ensemble import RandomForestRegressor

# Function to load and preprocess data
def load_data(data_file):
    with open(data_file) as file:
        data = json.load(file)

    X = []
    y = []
    for data_point in data:
        track_name = data_point.get('Track Name')
        if track_name is not None:
            artist_name = data_point.get('Artist Name')
            track_popularity = data_point.get('Track Popularity', 0)  # Target variable
            duration_sec = data_point.get('Duration (sec)', 0)  # Handling missing data
            artist_popularity = data_point.get('Artist Popularity', 0)  # Additional feature

            X.append([duration_sec, artist_popularity])
            y.append(track_popularity)

    return X, y

# Load and preprocess the combined data
X, y = load_data('../../data/combination/combined_data.json')

# Creating and fitting the random forest regressor model
model = RandomForestRegressor(random_state=42)
model.fit(X, y)

# Now, you can use this model to predict track popularity for new data points
new_data_point = [
    [300, 90],  # Example: Duration = 300 seconds, Artist Popularity = 90
    # Add more new data points here if needed
]

# Predict track popularity for new data points
predicted_popularity = model.predict(new_data_point)

# Print the predicted popularity
print("Predicted Track Popularity:")
print(predicted_popularity)
