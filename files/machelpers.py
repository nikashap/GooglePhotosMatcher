import os
from PIL import Image
from datetime import datetime
import time
import piexif
import pyheif

def set_file_timestamps(file_path, new_time):
    # Set the access and modified times to the new_time
    os.utime(file_path, (new_time, new_time))

def get_exif_creation_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            return None
        
        # Get DateTimeOriginal (tag 36867) from EXIF data
        date_time_original = exif_data.get(36867)
        if date_time_original:
            # Convert string date to datetime object
            creation_time = datetime.strptime(date_time_original, "%Y:%m:%d %H:%M:%S")
            return creation_time.timestamp()
    except Exception as e:
        print(f"Error reading EXIF data for {image_path}: {e}")
        return None

def open_heic_convert_to_pillow(heic_path):
    # Read HEIC file
    heif_file = pyheif.read(heic_path)
    
    # Convert to other format (e.g., "RGB")
    image = Image.frombytes(heif_file.mode, 
                            heif_file.size, 
                            heif_file.data,
                            "raw",
                            heif_file.mode,
                            heif_file.stride)
    
    return image


def update_directory_timestamps(directory):
    for entry in os.scandir(directory):
        if entry.is_file():
            file_path = entry.path
            # Update only image files, you can add more extensions if needed
            if file_path.lower().endswith(('.jpg', '.jpeg', '.tiff', '.png')):
                creation_time = get_exif_creation_date(file_path)
                if creation_time:
                    set_file_timestamps(file_path, creation_time)
                    print(f"Updated timestamps for {file_path}")