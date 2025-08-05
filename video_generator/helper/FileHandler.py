

import os
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