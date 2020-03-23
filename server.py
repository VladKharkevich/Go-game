from socket import *
from select import select
from random import randint
from collections import deque
import pickle
from settings import server_port


class Server:

    def __init__(self):
        self.to_read = {}
        self.to_write = {}
        self.tasks = deque()
        self.waiting_clients = []
        self.current_games = []
        self.host = ''
        self.port = server_port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.tasks.append(self.get_client())
        self.run()

    def get_client(self):
        while True:
            yield ('read', self.server_socket)
            client_socket, address = self.server_socket.accept()
            print('Server connected by', address)
            size_board = pickle.loads(client_socket.recv(1024))
            self.waiting_clients.append((client_socket, size_board))
            self.init_game()

    def init_game(self):
        for i in range(len(self.waiting_clients) - 1):
            # searching a pair of clients which have same sizes of board
            if self.waiting_clients[i][1] == self.waiting_clients[-1][1]:
                self.current_games.append((
                    self.waiting_clients[i][0], self.waiting_clients[-1][0]))
                self.waiting_clients.pop(i)
                self.waiting_clients.pop(-1)
                self.tasks.append(self.start_game())

    def start_game(self):
        # initialization
        side = randint(0, 1)
        player_1, player_2 = self.current_games[-1]
        player_1.send(b'Start' + str(side).encode())
        player_2.send(b'Start' + str(side ^ 1).encode())
        if not side:
            player_1, player_2 = player_2, player_1
        self.tasks.append(self.second_player(player_1, player_2))
        # game
        while True:
            try:
                yield ('read', player_1)
                data = player_1.recv(1024)
                if not data:
                    player_2.send(b'exit')
                    player_1.close()
                    break
                if data == b'exit':
                    player_1.close()
                    break
                yield ('write', player_2)
                player_2.send(data)
            except:
                break
        # end of game
        for i in range(len(self.current_games)):
            if self.current_games[i][0] == player_1:
                self.current_games.pop(i)
                break

    def second_player(self, player_1, player_2):
        while True:
            try:
                yield ('read', player_2)
                data = player_2.recv(1024)
                if not data:
                    player_1.send(b'exit')
                    player_2.close()
                    break
                if data == 'exit':
                    player_2.close()
                    break
                yield ('write', player_1)
                player_1.send(data)
            except:
                break

    def run(self):
        while any([self.tasks, self.to_read, self.to_write]):
            while not self.tasks:
                ready_to_read, ready_to_write, _ = select(
                    self.to_read, self.to_write, [])
                for sock in ready_to_read:
                    self.tasks.append(self.to_read.pop(sock))
                for sock in ready_to_write:
                    self.tasks.append(self.to_write.pop(sock))
            try:
                task = self.tasks.popleft()
                reason, sock = next(task)
                if reason == 'read':
                    self.to_read[sock] = task
                if reason == 'write':
                    self.to_write[sock] = task
            except StopIteration:
                print('Done')


if __name__ == '__main__':
    s = Server()
