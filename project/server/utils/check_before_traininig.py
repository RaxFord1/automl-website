import logging
import os
import tensorflow as tf


def check_image_sizes(folder) -> (int, int):
    logging.log(logging.ERROR, f"folder = {folder}")
    image_sizes = set()

    # Walk through the folder
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                image = tf.io.read_file(file_path)
                image = tf.image.decode_image(image, channels=3)
                shape = tuple(image.shape[:2])
                image_sizes.add(shape)

                if len(image_sizes) > 1:
                    logging.log(logging.ERROR, f"Image sizes mismatch found in {file_path}. Sizes found: {image_sizes}")
                    return None

    if len(image_sizes) == 1:
        single_size = image_sizes.pop()
        logging.log(logging.INFO, f"All images are of the same size: {single_size}")

        return single_size
    else:
        logging.log(logging.ERROR, f"Different image sizes found: {image_sizes}")
        return None
