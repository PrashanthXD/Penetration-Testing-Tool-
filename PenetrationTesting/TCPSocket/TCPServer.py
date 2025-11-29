import socket
import threading
import subprocess
import ssl
import os


def translate_command(command):
    """Translate Unix commands to Windows equivalents if running on Windows.
    
    Args:
        command: The command string to translate.
        
    Returns:
        The translated command string.
    """
    if os.name == 'nt':
        if command == 'ls':
            return 'dir'
        elif command == 'pwd':
            return 'cd'
    return command


def execute_command(command):
    """Execute a shell command and return the output.
    
    Args:
        command: The command string to execute.
        
    Returns:
        The output of the command as a string.
    """
    translated_command = translate_command(command)
    return subprocess.getoutput(translated_command)


def handle_client(clientsocket):
    """Handle client connections and execute commands.
    
    Args:
        clientsocket: The client socket object.
    """
    while True:
        try:
            command = clientsocket.recv(1024).decode('ascii')
            if not command or command.lower() == 'exit':
                break
            
            output = execute_command(command)
            
            clientsocket.send(output.encode('ascii'))
        except Exception as e:
            print(f"Error: {e}")
            break
    clientsocket.close()


def create_server_socket(host, port, certfile=None, keyfile=None):
    """Create and configure a server socket.
    
    Args:
        host: The host address to bind to.
        port: The port number to bind to.
        certfile: Optional path to SSL certificate file.
        keyfile: Optional path to SSL key file.
        
    Returns:
        A configured server socket.
    """
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    
    if certfile and keyfile:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        serversocket = context.wrap_socket(serversocket, server_side=True)
    
    return serversocket


def start_server(host='127.0.0.1', port=8000, certfile="server.crt", keyfile="server.key", max_connections=3):
    """Start the TCP server.
    
    Args:
        host: The host address to bind to (default: '127.0.0.1').
        port: The port number to bind to (default: 8000).
        certfile: Path to SSL certificate file.
        keyfile: Path to SSL key file.
        max_connections: Maximum number of queued connections.
    """
    serversocket = create_server_socket(host, port, certfile, keyfile)
    serversocket.listen(max_connections)
    
    while True:
        clientsocket, address = serversocket.accept()
        print("Received connection from: %s " % str(address))
        client_thread = threading.Thread(target=handle_client, args=(clientsocket,))
        client_thread.start()


if __name__ == "__main__":
    start_server()
