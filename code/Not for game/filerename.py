import os

folder_path = "h96"  # Specify the path to your folder

for filename in os.listdir(folder_path):
    if filename.endswith(".gif"):
        # Rename the file by replacing the ".gif" extension with ".png"
        new_filename = os.path.splitext(filename)[0] + ".png"
        file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        os.rename(file_path, new_file_path)