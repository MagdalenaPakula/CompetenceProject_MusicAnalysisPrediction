import json

# List of file paths
json_files = [
    '../../data/formation/spotify_formatted_data.json',
    '../../data/formation/itunes_formatted_data.json',
    '../../data/formation/deezer_formatted_data.json',
    '../../data/formation/lastfm_formatted_data.json',
    '../../data/formation/billboard_formatted_data.json'
]

# Create an empty list to store the data from all files
combined_data = []

# Iterate through each file
for file_path in json_files:
    with open(file_path) as file:
        data = json.load(file)
        combined_data.extend(data)  # Extend the list with data from the current file

# Save the combined data to a new JSON file
output_file = 'combined_data.json'
with open(output_file, 'w') as file:
    json.dump(combined_data, file)
