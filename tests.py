__author__ = 'Chris Morgan'

import json
import time
import socket
import random
import unittest
import threading
import socketserver
from server import SCPHandler


class TestSCPServer(unittest.TestCase):

    def setUp(self):
        self.ip = 'localhost'
        self.port = random.randint(10000, 20000)
        self.server = socketserver.TCPServer((self.ip, self.port), SCPHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()


    def tearDown(self):
        self.server.shutdown()

    def client(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        try:
            sock.sendall(json.dumps(data).encode())
            response = sock.recv(1024).decode()
        finally:
            sock.close()
        return response

    def test_successful_calculation(self):
        scp_request = {
            'protocol': 'SCP',
            'version': '1.0',
            'method': 'fibonacci',
            'sequence_number': 10
        }

        received = self.client(scp_request)

        data = json.loads(received)

        self.assertEqual(data['header']['status'], 'Success')
        self.assertEqual(data['header']['status_code'], 200)
        self.assertEqual(data['data']['computed_value'], 55)


    def test_number_out_of_range(self):
        scp_request = {
            'protocol': 'SCP',
            'version': '1.0',
            'method': 'fibonacci',
            'sequence_number': -1
        }

        received = self.client(scp_request)

        data = json.loads(received)

        self.assertEqual(data['header']['status'], 'Out of sequence range')
        self.assertEqual(data['header']['status_code'], 402)

    def test_invalid_data_type(self):
        scp_request = {
            'protocol': 'SCP',
            'version': '1.0',
            'method': 'fibonacci',
            'sequence_number': 'test'
        }

        received = self.client(scp_request)

        data = json.loads(received)

        self.assertEqual(data['header']['status'], 'Invalid data type')
        self.assertEqual(data['header']['status_code'], 401)

    def test_invalid_method(self):
        scp_request = {
            'protocol': 'SCP',
            'version': '1.0',
            'method': 'padovan',
            'sequence_number': 10
        }

        received = self.client(scp_request)

        data = json.loads(received)

        self.assertEqual(data['header']['status'], 'Not yet implemented')
        self.assertEqual(data['header']['status_code'], 501)

    def test_invalid_version(self):
        scp_request = {
            'protocol': 'SCP',
            'version': '2.0',
            'method': 'fibonacci',
            'sequence_number': 10
        }

        received = self.client(scp_request)

        data = json.loads(received)

        self.assertEqual(data['header']['status'], 'Not yet implemented')
        self.assertEqual(data['header']['status_code'], 501)



if __name__ == '__main__':
    unittest.main()
