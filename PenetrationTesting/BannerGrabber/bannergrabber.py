#!/usr/bin/python3
# Sin comprobar
import socket

def banner(ip, port):
    s = socket.socket()
    s.connect((ip, int (port)))
    s.setimeout(5)
    print(str(s.recv(1024)).strip('b'))
def main():
    ip = input("Enter IP: ")
    port = str(input("Enter port: "))
    banner(ip,port)
main()