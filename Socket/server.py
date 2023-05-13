##################################################################
# Project:  CSE-5306 Multi-Threaded Server
# Date:     Friday 9 September 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu)
##################################################################

import socket
import os

PORT                = 8000                      # Port to bind socket to
DELIMITER           = "<DELIMITER>"             # to decode path and filenames
BUFFER_SIZE         = 5120                      # 5MB buffer size
SERVER_HOST         = "0.0.0.0"                 # Server Host address
SYNCED_SERVER_DIR   = "./synced_dir_server/"    # Location of files on server

def server_sync(client_instance, file_name):
    print("Syncing " + str(file_name) + " now")
    file = open((os.path.join(SYNCED_SERVER_DIR, str(file_name))), "wb")     # Open an existing file the same name or create a new one

    while True:
        data = client_instance.recv(BUFFER_SIZE)

        if not data:
            break
        else:
            file.write(data)                                            # Store the received data into a file at the default location

        print("File: " + str(file_name) + " synced to server")
        file.close()


def Main():
    socket_instance = socket.socket()                                   # Get instance of socket
    socket_instance.bind((SERVER_HOST, PORT))                           # Bind hostname and PORT number to socket

    print(f"Listening for connection request on PORT {PORT}")

    socket_instance.listen(5)                                           # Number of requests that can be made

    while True:
        client_instance, address = socket_instance.accept()             # Accept an incoming Client request
        print(f"Client[{client_instance}] connected")                   # Provide feedback to user

        file_name = client_instance.recv(BUFFER_SIZE).decode()          # Receive file from client
        if not file_name:                                               # No data received
            break
        else:
            server_sync(client_instance, file_name)

if __name__ == '__main__':
    Main()