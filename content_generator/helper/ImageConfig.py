
import os
import glob
import shutil
from datetime import datetime
import re
import requests

class ImageConfig:

    def __init__(self,folder_path):
        self.folder_path = folder_path + "initial_image_data/"
        self.folder_path_parent = folder_path


    def move_images(self, source_folder, destination_folder):
        # Ensure destination folder exists
        os.makedirs(destination_folder, exist_ok=True)
        full_paths = []
        # Allowed image extensions
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')

        for filename in os.listdir(source_folder):
            if filename.lower().endswith(image_extensions):
                source_path = os.path.join(source_folder, filename)
                dest_path = os.path.join(destination_folder, filename)
                full_paths.append(destination_folder + filename)

                # Move the file (copy then delete)
                shutil.copy(source_path, dest_path)
                print(f"✅ Moved: {filename}")


        return full_paths

    @staticmethod
    def download_images(url) :
        folder_path = os.getenv("IMG_PATH_INITIAL_IMG")
        # Make sure the folder exists
        os.makedirs(folder_path, exist_ok=True)
        # Extract filename from URL
        filename = os.path.basename(url)
        # Full path to save the image
        file_path = os.path.join(folder_path, filename)

        # Download and save the image
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)

            print(f"Image saved to: {file_path}")
            return file_path
        else:
            print("Failed to download image:", response.status_code)
            return ""



