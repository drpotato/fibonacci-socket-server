#! /usr/bin/env python3

__author__ = 'Chris Morgan'

import json
import threading
import socketserver

"""
FCP: Fibonacci Computation Protocol

Request Template:
    {
        sequence_number: <SEQUENCE_NUMBER>,
    }

Response Template:
    {
        status: <STATUS>,
        computed_value: <COMPUTED_VALUE>
    }
"""


class FibonacciHandler(socketserver.ForkingMixIn, socketserver.BaseRequestHandler):
    """
    Socket request handler to calculate the fibonacci number for a given value.
    """

    def handle(self):

        # Receive data
        data = self.request.recv(1024).decode()

        # Build a json object from the data.
        request = json.loads(data)

        try:
            # Convert it to an integer.
            value = int(request['sequence_number'])
        except ValueError:
            # The data provided wasn't an integer,
            result = {
                'status': 'failure'
            }
            self.request.sendall(json.dumps(result).encode())
            return

        if value < 0:
            # Prevent hitting recursion limit and failing for an invalid number.
            result = {
                'status': 'failure'
            }
            self.request.sendall(json.dumps(result).encode())
            return

        # Calculate the fibonacci number.
        computed_value = self.fib(value)

        result = {
            'status': 'success',
            'computed_value': computed_value
        }

        # Encode the result in a binary string and send the result back to the client.
        self.request.sendall(json.dumps(result).encode())

    @staticmethod
    def fib(n):
        """
        Computes the fibonacci number for a given index.

        :param n: fibonacci number index to be computed
        :return: the fibonacci number for a given index
        """
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return FibonacciHandler.fib(n - 1) + FibonacciHandler.fib(n - 2)

if __name__ == "__main__":

    # Bind the server to localhost on port 12345.
    # TCP is used to ensure the transmission is reliable.
    server = socketserver.TCPServer(('localhost', 12345), FibonacciHandler)

    # Start a thread to handle the requests.
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Start the server listening.
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        exit()
