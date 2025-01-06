#!/usr/bin/python3
# Sin comprobar
import socket
# Creating the socket object. AF_INET -> ipv4, socket.SOCK_STREAM -> TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setimeout(5)

host = input("Enter IP: ")
port = str(input("Enter port: "))

def portScanner(port):
    if s.connect_ex((host, port)):
        print("The port is closed")
    else:
        print("The port is open")
portScanner(port)