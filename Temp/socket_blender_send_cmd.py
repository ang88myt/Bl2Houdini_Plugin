import bpy
import socket

# Specify the host and port for the communication
host = '127.0.0.1'  # IP address of the machine running Houdini
port = 5005        # Port number to use for communication

# Establish a socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Send the command to reload the USD file
command = "reload_usd_file"
client_socket.send(command.encode())

# Close the socket connection
client_socket.close()