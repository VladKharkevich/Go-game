import sys
from socket import *
import pickle
from settings import server_host, server_port


class Client:

    def __init__(self):
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
                pass

    def start_client(self, size):
        self.client_socket.send(pickle.dumps(size))
        data = self.client_socket.recv(1024)
        if 'Start' in data.decode():
            result = True
            return result, chr(data[-1])
        else:
            result = False
            return result, None
