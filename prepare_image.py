import os
from PIL import Image

# Base directory containing the folders
base_dir = 'D:\\Programming\\train'

# List of subdirectories to process
subdirs = [os.path.join(base_dir, str(i)) for i in range(5)]

# Desired size
size = (255, 255)


def resize_images_in_directory(directory, size):
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Add other image formats if needed
            file_path = os.path.join(directory, filename)
            with Image.open(file_path) as img:
                img = img.resize(size, Image.ANTIALIAS)
                img.save(file_path)
            print(f"Resized {file_path}")


for subdir in subdirs:
    resize_images_in_directory(subdir, size)
    print(f"Processed directory: {subdir}")

print("All images resized.")
