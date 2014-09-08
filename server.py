#! /usr/bin/env python3

__author__ = 'Chris Morgan'

import json
import threading
import socketserver

"""
SCP: Sequence Computation Protocol


Notes:
    After having a look at the HTTP specification, I considered changing the protocol message structure to something
    more closely resembling the HTTP messaging structure. However, the convenience of json when developing in python is
    too desirable for such a small project. I will however, make the system a little more flexible/extensible.
    If I were to move it to a HTTP inspired format it would look like this:
    Request Template:
        <METHOD> <SEQUENCE_NUMBER> SCP/<VERSION>

    Response Template:
    SCP/<VERSION> <STATUS_CODE> <STATUS_MESSAGE>

Request Template:
    {
        protocol: SCP,
        version: <VERSION>
        method: <METHOD>,
        sequence_number: <SEQUENCE_NUMBER>,
    }

Response Template:
    {
        status: <STATUS>,
        code: <STATUS_CODE>,
        computed_value: <COMPUTED_VALUE>
    }

Status Codes:
    200: Success.
    401: Invalid data type.
    402: Out of sequence range.
    501: Not yet implemented.
"""


class FibonacciHandler(socketserver.ForkingMixIn, socketserver.BaseRequestHandler):
    """
    Socket request handler to calculate the fibonacci number for a given value.
    """

    _status_codes = {
        200: 'Success',
        401: 'Invalid data type',
        402: 'Out of sequence range',
        501: 'Not yet implemented'
    }

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
            self.failure(401)
            return

        if request['version'] == '1.0':

            if request['method'] == 'fibonacci':

                if value < 0:
                    # Prevent hitting recursion limit and failing for an invalid number.
                    self.failure(402)
                    return

                # Calculate the fibonacci number.
                computed_value = self.fib(value)

                self.success(200, computed_value)

            else:
                self.failure(501)
        else:
            self.failure(501)

    def success(self, status_code, computed_value):
        result = {
            'status': self._status_codes[status_code],
            'status_code': status_code,
            'computed_value': computed_value
        }
        # Encode the result in a binary string and send the result back to the client.
        self.request.sendall(json.dumps(result).encode())

    def failure(self, status_code):
        result = {
            'status': self._status_codes[status_code],
            'status_code': status_code
        }
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
