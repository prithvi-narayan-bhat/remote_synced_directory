##################################################################
# Project:  CSE-5306 Multi-Threaded Server synced folder
# Date:     Monday 12 September 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu)
##################################################################

import os
import threading
import xmlrpc.client
import sys
from datetime import datetime
import time

PORT                = 8000                      # Port to bind socket to
SERVER_HOST         = "0.0.0.0"                 # Server Host address
CLIENT_FILES        = "./synced_dir_client/"    # Location of files on client
NULL_FILE           = "/dev/null"

def update_dictionary(unsynced_dictionary):
    for file in os.listdir(CLIENT_FILES):
        last_modified_time = datetime.strptime(time.ctime(os.path.getmtime(os.path.join(CLIENT_FILES, file))), "%a %b %d %H:%M:%S %Y")
        unsynced_dictionary.update({str(file) : str(last_modified_time)})

def monitor_sync(server_proxy):
    synced_dictionary = {}                                                          # Empty dictionary to store timestamp and names of synced files
    while True:
        unsynced_dictionary = {}                                                    # Empty dictionary to store timestamp and names of unsynced files
        update_dictionary(unsynced_dictionary)                                      # Get the latest file changes and their timestamps from the directory

        if synced_dictionary != unsynced_dictionary:                                # Compare synced and unsynced files
            print("Syncing now")
            unsynced_file_list = []
            synced_file_list = []

            for synced_files in synced_dictionary.keys():
                synced_file_list.append(synced_files)                               #  List all available files in the shared directory

            for file_name in synced_file_list:
                with open(NULL_FILE, "rb") as null_file:
                    file_data = xmlrpc.client.Binary(null_file.read())              # Open and read files
                    server_proxy.sync(synced_files, file_data, "DELETE")            # Request a delete operation of previously synced files to upload new copies

            for unsynced_files in unsynced_dictionary.keys():
                unsynced_file_list.append(unsynced_files)                           #  List all available files in the shared directory

            for file_name in unsynced_file_list:
                destination = os.path.join(CLIENT_FILES, file_name)

                with open(destination, "rb") as file:
                    file_data = xmlrpc.client.Binary(file.read())                   # Open and read files
                    synced_dictionary.pop(file_name, None)
                    server_proxy.sync(file_name, file_data, "UPLOAD")

            synced_dictionary = unsynced_dictionary
        time.sleep(10)                                                              # Sleep for 10s before syncing

def Main():
    server_endpoint = 'http://{}:{}'.format(SERVER_HOST, PORT)                      # Set an endpoint for the client to communicate to

    server_proxy = xmlrpc.client.ServerProxy(server_endpoint)

    thread1 = threading.Thread(target = monitor_sync, args = (server_proxy, ))      # Create a thread to monitor new file creation
    thread1.start()                                                                 # Spawn a thread to monitor modifications in the shared directory

if __name__ == '__main__':
    Main()