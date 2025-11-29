#!/usr/bin/python3
# Sin comprobar
import socket


def grab_banner(ip, port, timeout=5):
    """Grab the banner from a service running on the specified IP and port.
    
    Args:
        ip: The IP address of the target.
        port: The port number of the service.
        timeout: Socket timeout in seconds (default: 5).
        
    Returns:
        The banner string received from the service.
        
    Raises:
        socket.error: If connection fails.
        socket.timeout: If connection times out.
    """
    s = socket.socket()
    s.settimeout(timeout)
    s.connect((ip, int(port)))
    banner = str(s.recv(1024)).strip('b')
    s.close()
    return banner


def banner(ip, port):
    """Legacy function: Grab and print the banner from a service.
    
    Args:
        ip: The IP address of the target.
        port: The port number of the service.
    """
    result = grab_banner(ip, port)
    print(result)


def main():
    """Interactive main function to grab a banner."""
    ip = input("Enter IP: ")
    port = str(input("Enter port: "))
    banner(ip, port)


if __name__ == "__main__":
    main()