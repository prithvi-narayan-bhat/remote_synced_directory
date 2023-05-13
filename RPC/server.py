##################################################################
# Project:  CSE-5306 Multi-Threaded Server synced folder
# Date:     Monday 12 September 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu)
##################################################################

import os
import threading
from xmlrpc.server import SimpleXMLRPCServer

PORT                = 8000                      # Port to bind socket to
SERVER_HOST         = "0.0.0.0"                 # Server Host address
SERVER_FILES        = "./synced_dir_server/"    # Location of files on server

def file_upload(file_name, file_data):                                      # Method to handle file upload to server
    destination = os.path.join(SERVER_FILES, file_name)                     # Set the upload destination
    with open(destination, "wb") as file:                                   # Create a new file with the same name as received from client
        file.write(file_data.data)                                          # Write data into it
    return True

def file_delete(file_name):                                                 # Function to delete files
    if not os.path.exists(os.path.join(SERVER_FILES, file_name)):           # Determine if the provided file actually exists
        return False
    else:
        os.remove(os.path.join(SERVER_FILES, file_name))                    # Invoke system call to remove file
    return True

def directory_sync(file_name, file_data, file_operation):                   # RPC method to sync a client directory to the server
    print("Syncing now")
    if file_operation == "UPLOAD":                                          # Call appropriate function based on client request
        file_upload(file_name, file_data)
    elif file_operation == "DELETE":
        file_delete(file_name)
    return True

def Main():
    server = SimpleXMLRPCServer((SERVER_HOST, PORT))                        # Create a server instance
    print("Server online\nListening on port [" + str(PORT) + "]")
    server.register_function(directory_sync, 'sync')                        # Register RPCs broadcast by server
    try:
        server.serve_forever()                                              # Keep server running indefinitely
    except KeyboardInterrupt:
        print("Killing Server")

if __name__ == '__main__':
    Main()