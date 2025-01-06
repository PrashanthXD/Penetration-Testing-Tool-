#!/usr/bin/python3

import socket
import threading
import subprocess
import ssl
import os

def handle_client(clientsocket):
    while True:
        try:
            # Receive command from client
            command = clientsocket.recv(1024).decode('ascii')
            if not command or command.lower() == 'exit':
                break
            
            # Execute the command based on the operating system
            if os.name == 'nt':  # Windows
                if command == 'ls':
                    command = 'dir'
                elif command == 'pwd':
                    command = 'cd'
            
            # Execute the command
            output = subprocess.getoutput(command)
            
            # Send the command output back to the client
            clientsocket.send(output.encode('ascii'))
        except Exception as e:
            print(f"Error: {e}")
            break
    clientsocket.close()

# Creating the socket object. AF_INET -> ipv4, socket.SOCK_STREAM -> TCP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the address to be reused
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Use '0.0.0.0' to bind to all available interfaces
host = '127.0.0.1'
port = 8000

# To bind host and port to server
serversocket.bind((host, port))

# Create SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Wrap the socket with SSL
serversocket = context.wrap_socket(serversocket, server_side=True)

# Set up TCP listener and how many connections/request 
serversocket.listen(3)

while True:
    # Starting connection
    clientsocket, address = serversocket.accept()
    
    # Server text output
    print("Received connection from: %s " % str(address))
    
    # Handle the client in a new thread
    client_thread = threading.Thread(target=handle_client, args=(clientsocket,))
    client_thread.start()