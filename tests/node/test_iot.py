import os
import sys
import time
import random
import socket
import json
from datetime import datetime

class TestIOT:
    def __init__(self):
        self.socket = self.create_socket()

    def create_socket(self):
        # Create a socket
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return socket

    def connect_socket(self, host, port):
        # Connect to a socket
        self.socket.connect((host, port))

    def send_data(self, data):
        # Send data over the socket
        self.socket.send(json.dumps(data).encode())

    def receive_data(self):
        # Receive data over the socket
        data = self.socket.recv(1024)
        return json.loads(data.decode())

    def test_iot(self):
        # Test the IOT functions
        host = "localhost"
        port = 8080
        self.connect_socket(host, port)
        data = {"temperature": random.uniform(20, 30), "humidity": random.uniform(40, 60), "timestamp": datetime.now().isoformat()}
        self.send_data(data)
        response = self.receive_data()
        print("Received response:", response)

if __name__ == "__main__":
    test_iot = TestIOT()
    test_iot.test_iot()
