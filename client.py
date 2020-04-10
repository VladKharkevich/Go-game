import sys
from socket import *
import pickle
from settings import server_host, server_port


class Client:

    def __init__(self, mode="play"):
        self.server_host = server_host
        self.server_port = server_port
        if len(sys.argv) > 1:
            self.server_host = sys.argv[1]
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.access = False
        while not self.access:
            try:
                self.client_socket.connect(
                    (self.server_host, self.server_port))
                self.access = True
            except:
                if mode == "gotv":
                    break

    def start_client(self, size):
        self.client_socket.send(b"play " + pickle.dumps(size))
        data = self.client_socket.recv(1024)
        if 'Start' in data.decode():
            result = True
            return result, chr(data[-1])
        else:
            result = False
            return result, None

    def connect_to_go_TV(self):
        self.client_socket.send(b"gotv")
        data = self.client_socket.recv(1024)
        if data == b"Translation not found":
            return "Translation not found"
        else:
            return pickle.loads(data)
