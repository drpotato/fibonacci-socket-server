#! /usr/bin/env python3

__author__ = 'Chris Morgan'

import sys
import socket

# Grab the value from the command line arguments
value = " ".join(sys.argv[1:])

# Create a TCP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect(('localhost', 12345))

    # Send the data through the socket.
    sock.sendall(value.encode())

    # Receive data from the server and shut down
    received = sock.recv(1024).decode()

    # Display revieved information.
    print(received)


finally:
    sock.close()