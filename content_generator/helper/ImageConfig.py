
import os
import glob
import shutil
from datetime import datetime
import re

class ImageConfig:

    def __init__(self,folder_path):
        self.folder_path = folder_path + "initial_image_data/"
        self.folder_path_parent = folder_path

    def check_images_exist(self):
        print("Getting the saved images for the article.")
        png_files = glob.glob(os.path.join(self.folder_path, "*.png"))
        jpg_files = glob.glob(os.path.join(self.folder_path, "*.jpg"))
        webp_files = glob.glob(os.path.join(self.folder_path, "*.webp"))

        image_files = png_files + jpg_files + webp_files

        if image_files:
            date_str = datetime.now().strftime("%Y_%m_%d_%H_%M")
            destination_path = self.folder_path_parent + date_str + "/"
            os.makedirs(destination_path)
            return self.move_images(self.folder_path, destination_path)



        else:
            print("❌ No .png or .jpg files found in the folder. initial_image_data please check")
            return []


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
