import socket
import ssl


def create_client_socket(host, port, use_ssl=True):
    """Create and configure a client socket.
    
    Args:
        host: The server hostname.
        port: The port number to connect to.
        use_ssl: Whether to use SSL/TLS encryption (default: True).
        
    Returns:
        A configured client socket.
    """
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if use_ssl:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        clientsocket = context.wrap_socket(clientsocket, server_hostname=host)
    
    return clientsocket


def connect_to_server(clientsocket, host, port):
    """Connect the client socket to a server.
    
    Args:
        clientsocket: The client socket object.
        host: The server address to connect to.
        port: The port number to connect to.
    """
    clientsocket.connect((host, port))


def send_command(clientsocket, command):
    """Send a command to the server.
    
    Args:
        clientsocket: The client socket object.
        command: The command string to send.
    """
    clientsocket.send(command.encode('ascii'))


def receive_response(clientsocket, buffer_size=4096):
    """Receive a response from the server.
    
    Args:
        clientsocket: The client socket object.
        buffer_size: The maximum number of bytes to receive (default: 4096).
        
    Returns:
        The decoded response string.
    """
    return clientsocket.recv(buffer_size).decode('ascii')


def run_client_interactive(host='127.0.0.1', port=8000):
    """Run the interactive client session.
    
    Args:
        host: The server hostname (default: '127.0.0.1').
        port: The port number (default: 8000).
    """
    clientsocket = create_client_socket(host, port)
    connect_to_server(clientsocket, host, port)
    
    while True:
        command = input("Enter command to execute on server: ")
        send_command(clientsocket, command)
        output = receive_response(clientsocket)
        print(output)
        if command.lower() == 'exit':
            break
    
    clientsocket.close()


if __name__ == "__main__":
    run_client_interactive()
