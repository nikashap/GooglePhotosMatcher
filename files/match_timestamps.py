import argparse
import json
import os
import time

def set_file_timestamps(file_path, new_time):
    # Set the access and modified times to the new_time
    os.utime(file_path, (new_time, new_time))

def get_photo_taken_time(json_file_path):
    # Open and load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        # Extract photoTakenTime timestamp
        photo_taken_timestamp = int(data['photoTakenTime']['timestamp'])
        return photo_taken_timestamp

def update_media_timestamps(media_file_path, json_file_path):
    # Extract photo taken time from JSON
    photo_taken_time = get_photo_taken_time(json_file_path)

    # Convert Unix timestamp to time format suitable for os.utime
    photo_taken_time = time.mktime(time.gmtime(photo_taken_time))

    # Update file timestamps
    set_file_timestamps(media_file_path, photo_taken_time)

def match_media_with_json(media_file_path):
    """Uses the `timestamp` attribute from the corresponding json file.
    If the json file doesn't exist, make note of the unsuccess."""

    # Check if the .mp4 file is associated with an HEIC file
    if media_file_path.lower().endswith('.mp4'):
        path_HEIC = os.path.splitext(media_file_path)[0] + '.HEIC.json'
        path_JPG = os.path.splitext(media_file_path)[0] + '.JPG.json'
        path_JPEG = os.path.splitext(media_file_path)[0] + '.JPEG.json'
        if os.path.exists(path_HEIC):
            json_file_path = path_HEIC
        elif os.path.exists(path_JPG):
            json_file_path = path_JPG
        elif os.path.exists(path_JPEG):
            json_file_path = path_JPEG
        else:
            json_file_path = media_file_path + ".json"
    else:
        json_file_path = media_file_path + ".json"

    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        # print(f"JSON file does not exist for {media_file_path}")
        return False

    try:
        update_media_timestamps(media_file_path, json_file_path)
        update_media_timestamps(json_file_path, json_file_path) #Update json file path timestamp too
        return True
    except Exception as e:
        # Log or print the error message
        # print(f"Failed to update timestamps for {media_file_path}: {e}")
        return False


def main(parent_directory_path):
    media_extensions = ('.jpg', '.jpeg', '.png', '.heic', '.mp4', '.mov')
    failed_paths = []
    # Walk through all subdirectories in the parent directory
    for subdir, _, files in os.walk(parent_directory_path):
        for file in files:
            if file.lower().endswith(media_extensions):
                media_file_path = os.path.join(subdir, file)
                # Attempt to match and update each media file with its JSON
                if not match_media_with_json(media_file_path):
                    failed_paths.append(media_file_path)
    print("Failed Paths:")
    for path in failed_paths:
        print(path)
    
if __name__ == '__main__':
    # Initialize parser
    parser = argparse.ArgumentParser(description="Update media timestamps using corresponding JSON files.")
    # Adding required argument for parent directory path
    parser.add_argument("parent_directory_path", help="Specify the parent directory path containing all media and JSON files")
    # Parse arguments
    args = parser.parse_args()
    # Call main function with the provided directory path
    main(args.parent_directory_path)