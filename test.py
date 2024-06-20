# import time
# from subprocess import Popen, PIPE, STDOUT

# from project.server.utils.rar_or_zip import extract_and_delete_rar, extract_and_delete_zip

# command = ['python', 'train.py', 'D:\\archive\\Колледж\\курсовая 4 курс\\flask-jwt-auth-master\\datasets\\raxford32@gmail.com\\iris3\\Iris2.csv', 'D:/tmp/raxford32@gmail.com/iris3', '-e', 'iris3', '-o', 'raxford32@gmail.com', '-s', 'little']
#
# process = Popen(command, stdout=PIPE, stderr=STDOUT)
#
# stdout, stderr = process.communicate()
#
# # Print the output and errors
# print("Standard Output:")
# print(stdout.decode('latin-1'))
#
# if stderr:
#     print("Standard Error:")
#     print(stderr.decode('utf-8'))
#
# time.sleep(5*10000)


# extract_and_delete_rar("D:/images.rar", r"D:\archive\Колледж\курсовая 4 курс\flask-jwt-auth-master\datasets\images")
# extract_and_delete_zip("D:/0.zip", r"D:\archive\Колледж\курсовая 4 курс\flask-jwt-auth-master\datasets\images")

import tensorflow as tf


def read_image(file_path):
    # Read the image file
    image = tf.io.read_file(file_path)
    # Decode the image
    image = tf.image.decode_png(image, channels=3)  # Set channels to 3 for RGB
    return image


def print_pixel_values(image):
    # Convert the image to a numpy array
    image_array = image.numpy()

    # Get the dimensions of the image
    height, width, channels = image_array.shape

    # Print pixel values for each row and column
    for row in range(height):
        for col in range(width):
            pixel = image_array[row, col]
            print(f"{pixel}", end='')
        print("\n")


def main():
    file_path = r'D:\archive\Колледж\курсовая 4 курс\flask-jwt-auth-master\datasets\images\0\1.png'  # Replace with your image path
    image = read_image(file_path)
    print_pixel_values(image)


if __name__ == "__main__":
    main()
