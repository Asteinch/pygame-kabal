from PIL import Image
import os

folder_path = "h96"  # Specify the path to your folder

# Create a new folder to store the upscaled images
output_folder = os.path.join(folder_path, "upscaled")
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(folder_path):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Open the image file
        file_path = os.path.join(folder_path, filename)
        image = Image.open(file_path)

        # Calculate the new dimensions
        new_width = int(image.width * 1.5)
        new_height = int(image.height * 1.5)

        # Resize the image using the nearest neighbor method
        upscaled_image = image.resize((new_width, new_height), resample=Image.NEAREST)

        # Save the upscaled image with the same filename in the output folder
        output_path = os.path.join(output_folder, filename)
        upscaled_image.save(output_path)

        # Close the image file
        image.close()