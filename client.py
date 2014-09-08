#! /usr/bin/env python3

__author__ = 'Chris Morgan'

import sys
import json
import socket


# Sets up a socket and communicates with server.
def client(value):

    request = {
        'protocol': 'SCP',
        'version': '1.0',
        'method': 'fibonacci',
        'sequence_number': value
    }

    # Create a TCP socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to server and send/receive data
        sock.connect(('localhost', 12345))
        sock.sendall(json.dumps(request).encode())
        response = sock.recv(1024).decode()
    finally:
        sock.close()
    return json.loads(response)


def logic(value):
    data = client(value)

    if data['header']['status'] == 'Success':
        print(data['data']['computed_value'])
    else:
        print(data['header']['status_code'], data['header']['status'], sep=': ')

if __name__ == '__main__':
    # Grab the value from the command line arguments
    value = ''.join(sys.argv[1:])

    if value:
        # If the there was fibonacci index in the command line arguments, run once.
        logic(value)

    else:
        # Otherwise enter a prompt to request fibonacci numbers indefinitely.
        while True:

            value = input('scp > ')

            if value == 'exit':
                exit()
            if not value:
                continue

            logic(value)
