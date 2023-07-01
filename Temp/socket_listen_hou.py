import hou
import socket

# Specify the host and port for the communication
host = '127.0.0.1'  # IP address of the machine running Houdini
port = 5005        # Port number to use for communication

# Create a socket and listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print("Waiting for connection...")

# Accept the connection from Blender
client_socket, address = server_socket.accept()
print("Connected to:", address)

# Receive the command from Blender
command = client_socket.recv(1024).decode()
print("Received command:", command)

# Reload the USD file
if command == "reload_usd_file":
    # Replace "/obj/usdimport1" with the actual path to your imported USD node
    usd_node = hou.node("/obj/geo1/usdimport1")
    if usd_node is not None:
        usd_node.parm("reload").pressButton()
        print("USD file reloaded.")

# Close the socket connection
client_socket.close()
server_socket.close()
