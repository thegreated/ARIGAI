

import os
import random

class FileHandler:

    @staticmethod
    def reset():
        print("----deleting tmp file")
        folder_path = os.getenv("NARRATION_PATH")

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

    @staticmethod
    def background_randomizer():

        folder_path = 'C:/Users/jaz2/Documents/PythonProject/resources/background_music/'
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if files:
            # Randomly select one file
            selected_file = random.choice(files)

            # Full path (optional)
            selected_file_path = os.path.join(folder_path, selected_file)

            print("---Selected file for bg_music:", selected_file_path)
            return  selected_file_path
        else:
            print("No files found in the folder.")

