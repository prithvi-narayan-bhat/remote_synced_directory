##################################################################
# Project:  CSE-5306 Multi-Threaded Server
# Date:     Saturday 10 September 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu)
##################################################################

import socket
import os
import time
import threading
from datetime import datetime

PORT                = 8000                      # Port to bind socket to
DELIMITER           = "<DELIMITER>"             # to decode path and filenames
BUFFER_SIZE         = 5120                      # 5MB buffer size
CLIENT_HOST         = "0.0.0.0"
SYNCED_CLIENT_DIR   = "./synced_dir_client/"

def monitor_sync(socket_instance, last_sync_time):
    print("Sync thread now")
    while True:
        last_modified_time = datetime.strptime(time.ctime(os.path.getmtime(SYNCED_CLIENT_DIR)), "%a %b %d %H:%M:%S %Y")

        if(last_modified_time != last_sync_time):
            print("Syncing now")

            for file_name in os.listdir(SYNCED_CLIENT_DIR):                         # Iterate through all files for sync
                socket_instance.send(f"{file_name}".encode())                       # Inform server of new file being synced
                file = open(os.path.join(SYNCED_CLIENT_DIR, file_name), 'rb')       # Open file and stream it to a server as a string o binary data
                data = file.read(BUFFER_SIZE)

                while data:
                    socket_instance.sendall(data)                                   # Send file as stream of binary data
                    data = file.read(BUFFER_SIZE)                                   # Continue reading next character until NULL is encountered

                    if not data:
                        break

                file.close()                                                        # Close file descriptor
                print("File: " + str(file_name) + " synced")

            last_sync_time = last_modified_time                                     # Update present time as the last sync time
        else:
            print("Synced already")

        time.sleep(10)                                                              # Sleep for 10s before syncing


def Main():
    socket_instance = socket.socket()                                                       # Get instance of socket
    socket_instance.connect((CLIENT_HOST, PORT))                                            # Bind hostname and port number to socket
    print(f"Server[{socket_instance}] connected")                                           # Provide feedback to user

    last_sync_time = datetime.strptime(time.ctime(time.time()), "%a %b %d %H:%M:%S %Y")     # Initialise epoch time for last sync
    thread1 = threading.Thread(target = monitor_sync, args = (socket_instance, last_sync_time, ))
    thread1.start()                                                                         # Spawn a thread to monitor modification in 


if __name__ == '__main__':
    Main()