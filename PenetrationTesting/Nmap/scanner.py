#!/usr/bin/python3
import nmap
scanner = nmap.PortScanner()

ip_address = input("Enter the IP address you want to scan: ")
type(ip_address)

resp = input(""" \nEnter the type of scan
                1) SYN ACK Scan
                2) UDP Scan
                3) Comprehensive scan\n """)

if resp == '1':
    print("Nmap version: ", scanner.nmap_version())
    scanner.scan(ip_address, '1-1024', '-v -sS')
    print(scanner.scaninfo())
    print("IP status:", scanner[ip_address].state())
    print(scanner[ip_address].all_protocols())
    print("Open ports: ", scanner[ip_address]['tcp'].keys())
elif resp == '2':
    print("Nmap version: ", scanner.nmap_version())
    scanner.scan(ip_address, '1-1024', '-v -sU')
    print(scanner.scaninfo())
    print("IP status:", scanner[ip_address].state())
    print(scanner[ip_address].all_protocols())
    print("Open ports: ", scanner[ip_address]['udp'].keys())
elif resp == '3':
    print("Nmap version: ", scanner.nmap_version())
    scanner.scan(ip_address, '1-1024', '-v -sS -sV -A -O')
    print(scanner.scaninfo())
    print("IP status:", scanner[ip_address].state())
    print(scanner[ip_address].all_protocols())
    print("Open ports: ", scanner[ip_address]['tcp'].keys())
else:
    print("[!] Plesea, enter a valid type of scan option")