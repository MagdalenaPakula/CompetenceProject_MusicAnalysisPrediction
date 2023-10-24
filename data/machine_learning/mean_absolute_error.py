import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

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

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating and fitting the random forest regressor model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Making predictions on the testing data
y_pred = model.predict(X_test)

# Calculating mean absolute error
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# TO DO:
# Predict Track Popularity
# Predict Artist Popularity
# Genre-Based Predictions
# Release Date Analysis
# Audio Feature Analysis
# Clustering or Segmentation
# Recommendation System

