import socket
import ssl

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
clientsocket = context.wrap_socket(clientsocket, server_hostname=host)

clientsocket.connect(('127.0.0.1', port))

while True:
    command = input("Enter command to execute on server: ")
    clientsocket.send(command.encode('ascii'))
    output = clientsocket.recv(4096).decode('ascii')
    print(output)
    if command.lower() == 'exit':
        break

clientsocket.close()
