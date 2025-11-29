#!/usr/bin/python3
import nmap


def create_scanner():
    """Create and return an nmap PortScanner instance.
    
    Returns:
        A nmap.PortScanner instance.
    """
    return nmap.PortScanner()


def get_nmap_version(scanner):
    """Get the nmap version.
    
    Args:
        scanner: The nmap.PortScanner instance.
        
    Returns:
        The nmap version tuple.
    """
    return scanner.nmap_version()


def syn_ack_scan(scanner, ip_address, port_range='1-1024'):
    """Perform a SYN ACK scan.
    
    Args:
        scanner: The nmap.PortScanner instance.
        ip_address: The IP address to scan.
        port_range: The port range to scan (default: '1-1024').
        
    Returns:
        A dictionary with scan results.
    """
    scanner.scan(ip_address, port_range, '-v -sS')
    return {
        'scaninfo': scanner.scaninfo(),
        'state': scanner[ip_address].state(),
        'protocols': scanner[ip_address].all_protocols(),
        'open_ports': list(scanner[ip_address]['tcp'].keys()) if 'tcp' in scanner[ip_address].all_protocols() else []
    }


def udp_scan(scanner, ip_address, port_range='1-1024'):
    """Perform a UDP scan.
    
    Args:
        scanner: The nmap.PortScanner instance.
        ip_address: The IP address to scan.
        port_range: The port range to scan (default: '1-1024').
        
    Returns:
        A dictionary with scan results.
    """
    scanner.scan(ip_address, port_range, '-v -sU')
    return {
        'scaninfo': scanner.scaninfo(),
        'state': scanner[ip_address].state(),
        'protocols': scanner[ip_address].all_protocols(),
        'open_ports': list(scanner[ip_address]['udp'].keys()) if 'udp' in scanner[ip_address].all_protocols() else []
    }


def comprehensive_scan(scanner, ip_address, port_range='1-1024'):
    """Perform a comprehensive scan.
    
    Args:
        scanner: The nmap.PortScanner instance.
        ip_address: The IP address to scan.
        port_range: The port range to scan (default: '1-1024').
        
    Returns:
        A dictionary with scan results.
    """
    scanner.scan(ip_address, port_range, '-v -sS -sV -A -O')
    return {
        'scaninfo': scanner.scaninfo(),
        'state': scanner[ip_address].state(),
        'protocols': scanner[ip_address].all_protocols(),
        'open_ports': list(scanner[ip_address]['tcp'].keys()) if 'tcp' in scanner[ip_address].all_protocols() else []
    }


def print_scan_results(scanner, ip_address, scan_type='tcp'):
    """Print the scan results.
    
    Args:
        scanner: The nmap.PortScanner instance.
        ip_address: The IP address that was scanned.
        scan_type: The type of scan ('tcp' or 'udp').
    """
    print("Nmap version: ", scanner.nmap_version())
    print(scanner.scaninfo())
    print("IP status:", scanner[ip_address].state())
    print(scanner[ip_address].all_protocols())
    print("Open ports: ", scanner[ip_address][scan_type].keys())


def validate_scan_option(option):
    """Validate the scan option input.
    
    Args:
        option: The option string to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    return option in ['1', '2', '3']


def main():
    """Interactive main function to run nmap scans."""
    scanner = create_scanner()
    
    ip_address = input("Enter the IP address you want to scan: ")
    type(ip_address)
    
    resp = input(""" \nEnter the type of scan
                    1) SYN ACK Scan
                    2) UDP Scan
                    3) Comprehensive scan\n """)
    
    if resp == '1':
        syn_ack_scan(scanner, ip_address)
        print_scan_results(scanner, ip_address, 'tcp')
    elif resp == '2':
        udp_scan(scanner, ip_address)
        print_scan_results(scanner, ip_address, 'udp')
    elif resp == '3':
        comprehensive_scan(scanner, ip_address)
        print_scan_results(scanner, ip_address, 'tcp')
    else:
        print("[!] Please, enter a valid type of scan option")


if __name__ == "__main__":
    main()