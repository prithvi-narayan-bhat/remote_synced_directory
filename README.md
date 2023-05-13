# Remote Synced Directory
Application to emulate a synced folder system (such as Dropbox)

## Implementation
A synced directory system is implemented using both Sockets and RPCs

## Operation
Any changes made to the synced client directory will immediately be synced with the remote server directory

## Usage
1. Run server.py and client.py simulatneously in the order
2. Make changes(addition, deletion, modifications) to files in the synced_dir_client
3. Observe changes automatically be reflected on the synced_dir_server directory
