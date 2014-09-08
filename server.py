#! /usr/bin/env python3

__author__ = 'Chris Morgan'

import threading
import socketserver

"""
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

        # Convert it to an integer.
        value = int(data)

        # Calculate the fibonacci number.
        result = self.fib(value)

        # Encode the result in a binary string and send the result back to the client.
        self.request.sendall(str(result).encode())

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
