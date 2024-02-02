import os
from flask import current_app
from models import db, SpotifyHistory
import json

# Function to add Spotify history from JSON files to the database
def add_spotify_history_from_json():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    json_folder_path = os.path.join(script_directory, "..", "Spotify Account Data")

    # Initialize Flask app context
    app = current_app._get_current_object()
    with app.app_context():
        # Iterate through each JSON file in the folder
        for file_name in os.listdir(json_folder_path):
            if file_name.startswith("StreamingHistory_music"):
                file_path = os.path.join(json_folder_path, file_name)

                # Open the JSON file and load the data
                with open(file_path, "r", encoding="utf-8") as json_file:
                    spotify_history_data = json.load(json_file)

                # Iterate through each entry in the JSON data and add it to the database
                for entry in spotify_history_data:
                    new_entry = SpotifyHistory(
                        endTime=entry.get("endTime"),
                        artistName=entry.get("artistName"),
                        trackName=entry.get("trackName"),
                        msPlayed=entry.get("msPlayed")
                    )
                    db.session.add(new_entry)
            # Commit the changes to the database
            db.session.commit()
