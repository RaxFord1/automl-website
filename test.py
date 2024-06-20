# import time
# from subprocess import Popen, PIPE, STDOUT

from project.server.utils.rar_or_zip import extract_and_delete_rar, extract_and_delete_zip

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
extract_and_delete_zip("D:/0.zip", r"D:\archive\Колледж\курсовая 4 курс\flask-jwt-auth-master\datasets\images")
