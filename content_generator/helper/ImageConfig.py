import os
import re
import shutil
import requests
import imghdr
from urllib.parse import urlparse

class ImageConfig:
    def __init__(self, folder_path):
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
                full_paths.append(os.path.join(destination_folder, filename))

                # Move the file (copy then delete)
                shutil.copy(source_path, dest_path)
                print(f"✅ Moved: {filename}")

        return full_paths

    @staticmethod
    def download_images(url,search):
        folder_path = os.getenv("IMG_PATH_INITIAL_IMG")
        os.makedirs(folder_path, exist_ok=True)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Validate content-type from headers
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"❌ Skipped (not image): {url} (Content-Type: {content_type})")
                return ""

            # Validate content using imghdr
            if not ImageConfig.is_valid_image(response.content):
                print(f"❌ Skipped (invalid image data): {url}")
                return ""

            # Sanitize filename
            filename = search+"-"+ImageConfig.sanitize_filename(url)
            file_path = os.path.join(folder_path, filename)

            # Write image to file
            with open(file_path, 'wb') as f:
                f.write(response.content)

            print(f"✅ Image saved to: {file_path}")
            return file_path

        except Exception as e:
            print(f"❌ Failed to download image from {url}: {e}")
            return ""

    @staticmethod
    def is_valid_image(content):
        image_type = imghdr.what(None, h=content)
        return image_type in ['jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']

    @staticmethod
    def sanitize_filename(url):
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # Remove unsafe characters
        filename = re.sub(r'[<>:"/\\|?*%]', '', filename)

        if not filename or filename.startswith('.'):
            filename = "image.jpg"

        return filename
