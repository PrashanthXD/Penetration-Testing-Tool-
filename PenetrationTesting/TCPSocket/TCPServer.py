import socket
import threading
import subprocess
import ssl
import os

def handle_client(clientsocket):
    while True:
        try:
    
            command = clientsocket.recv(1024).decode('ascii')
            if not command or command.lower() == 'exit':
                break
            
            if os.name == 'nt':
                if command == 'ls':
                    command = 'dir'
                elif command == 'pwd':
                    command = 'cd'
            
            output = subprocess.getoutput(command)
            
            clientsocket.send(output.encode('ascii'))
        except Exception as e:
            print(f"Error: {e}")
            break
    clientsocket.close()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = 8000
serversocket.bind((host, port))
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")
serversocket = context.wrap_socket(serversocket, server_side=True)
serversocket.listen(3)

while True:
    clientsocket, address = serversocket.accept()
    print("Received connection from: %s " % str(address))
    client_thread = threading.Thread(target=handle_client, args=(clientsocket,))
    client_thread.start()
