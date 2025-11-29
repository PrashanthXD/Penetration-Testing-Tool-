#!/usr/bin/python3
# Sin comprobar
import socket


def create_scanner_socket(timeout=5):
    """Create a socket configured for port scanning.
    
    Args:
        timeout: Socket timeout in seconds (default: 5).
        
    Returns:
        A configured socket object.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    return s


def scan_port(host, port, timeout=5):
    """Scan a single port on the specified host.
    
    Args:
        host: The IP address or hostname to scan.
        port: The port number to scan (can be string or int).
        timeout: Socket timeout in seconds (default: 5).
        
    Returns:
        True if the port is open, False if closed.
    """
    s = create_scanner_socket(timeout)
    try:
        result = s.connect_ex((host, int(port)))
        s.close()
        return result == 0
    except (socket.error, socket.timeout):
        s.close()
        return False


def portScanner(port, host=None, s=None):
    """Legacy function: Check if a port is open and print result.
    
    Args:
        port: The port number to scan.
        host: The host to scan (optional, uses global if not provided).
        s: The socket to use (optional, creates new if not provided).
    """
    if host is None:
        raise ValueError("Host must be provided")
    
    is_open = scan_port(host, port)
    if is_open:
        print("The port is open")
    else:
        print("The port is closed")
    return is_open


def main():
    """Interactive main function to scan a port."""
    host = input("Enter IP: ")
    port = str(input("Enter port: "))
    portScanner(port, host)


if __name__ == "__main__":
    main()