from socket import *
from select import select
from random import randint


class Server:

    def __init__(self):
        self.to_monitor = []

        self.myHost = ''
        self.myPort = 50009
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.myHost, self.myPort))
        self.server_socket.listen(5)
        self.to_monitor.append(self.server_socket)
        self.event_loop()

    def start_server(self, server_socket):
        if len(self.to_monitor) < 3:
            client_socket, address = server_socket.accept()
            print('Server connected by', address)
            self.to_monitor.append(client_socket)

    def event_loop(self):
        game = False
        while not game:
            ready_to_read, _, _ = select(self.to_monitor, [], [])
            for sock in ready_to_read:
                if sock is self.server_socket:
                    self.start_server(sock)
                else:
                    sock.send(b'')
            side = randint(0, 1)
            for sock in self.to_monitor:
                if sock is not self.server_socket:
                    if len(self.to_monitor) == 3:
                        if side:
                            if 'player_1' in locals():
                                player_2 = sock
                            else:
                                player_1 = sock
                        else:
                            if 'player_2' in locals():
                                player_1 = sock
                            else:
                                player_2 = sock
                        sock.send(b'Start' + str(side).encode())
                        side ^= 1
                        game = True
        queue = [player_1, player_2]
        while True:
            data = queue[0].recv(1024)
            queue[1].send(data)
            temp = queue.pop(0)
            queue.append(temp)


if __name__ == '__main__':
    s = Server()
