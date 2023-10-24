import json
from sklearn.ensemble import RandomForestClassifier

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
            genre = data_point.get('Genre', 'Unknown')  # Assuming 'Genre' is in the data

            X.append([duration_sec, track_popularity])  # Using track popularity as a feature
            y.append(genre)  # Predicting genre instead of artist popularity

    return X, y

# Load and preprocess the combined data
X, y = load_data('../../data/combination/combined_data.json')

# Creating and fitting the random forest classifier model (as genre is a categorical variable)
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Now, you can use this model to predict genre for new data points
new_data_point = [
    [300, 90],  # Example: Duration = 300 seconds, Track Popularity = 80
    # Add more new data points here if needed
]

# Predict genre for new data points
predicted_genre = model.predict(new_data_point)

# Print the predicted genre
print("Predicted Genre:")
print(predicted_genre)
