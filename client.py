import sys
from socket import *


class Client:

    def __init__(self):
        self.serverHost = 'localhost'
        self.serverPort = 50009
        if len(sys.argv) > 1:
            self.serverHost = sys.argv[1]
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.access = False
        while not self.access:
            try:
                self.sockobj.connect((self.serverHost, self.serverPort))
                self.access = True
            except:
                pass


    def start_client(self):
        data = self.sockobj.recv(1024)
        if 'Start' in data.decode():
            result = True
            return result, chr(data[-1])
        else:
            result = False
            return result, None
