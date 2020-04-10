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
        self.clients_gotv = []
        self.translated_game_to_gotv = None
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
            status = client_socket.recv(1024)
            if b'play' == status[:4]:
                size_board = pickle.loads(status[5:])
                self.waiting_clients.append((client_socket, size_board))
                self.init_game()
            elif status == b'gotv':
                self.tasks.append(self.connect_to_gotv(client_socket))

    def init_game(self):
        for i in range(len(self.waiting_clients) - 1):
            # searching a pair of clients which have same sizes of board
            if self.waiting_clients[i][1] == self.waiting_clients[-1][1]:
                self.current_games.append((
                    self.waiting_clients[i][0], self.waiting_clients[-1][0]))
                self.waiting_clients.pop(i)
                self.waiting_clients.pop(-1)
                self.tasks.append(self.start_game())

    def connect_to_gotv(self, client_socket):
        if not self.translated_game_to_gotv:
            client_socket.send(b"Translation not found")
            client_socket.close()
        else:
            self.clients_gotv.append(client_socket)
            yield ("write", self.translated_game_to_gotv[0])
            self.translated_game_to_gotv[0].send(b"Get turns")
            turns = self.translated_game_to_gotv[0].recv(1024)
            yield ("write", client_socket)
            client_socket.send(turns)

    def start_game(self):
        # initialization
        side = randint(0, 1)
        player_1, player_2 = self.current_games[-1]
        player_1.send(b'Start' + str(side).encode())
        player_2.send(b'Start' + str(side ^ 1).encode())
        if not side:
            player_1, player_2 = player_2, player_1
        if not self.translated_game_to_gotv:
            self.translated_game_to_gotv = (player_1, player_2)
        self.tasks.append(self.second_player(player_1, player_2))
        # game
        while True:
            try:
                yield ('read', player_1)
                data = player_1.recv(1024)
                print(data)
                if not data:
                    player_2.send(b'exit')
                    for sock in self.clients_gotv:
                        sock.send(b'exit')
                        sock.close()
                    player_1.close()
                    break
                if data == b'exit':
                    player_1.close()
                    break
                yield ('write', player_2)
                player_2.send(data)
                print(self.clients_gotv)
                for sock in self.clients_gotv:
                    sock.send(data)
            except Exception as e:
                print(e)
        # end of game
        for i in range(len(self.current_games)):
            if self.current_games[i][0] == player_1:
                self.current_games.pop(i)
                break
        if player_1 in self.translated_game_to_gotv:
            if len(self.translated_game_to_gotv) == 0:
                self.translated_game_to_gotv = None
            else:
                self.translated_game_to_gotv = self.current_games[-1]
            for client_sock in self.clients_gotv:
                yield ('write', client_sock)
                client_sock.send(b"end_of_translation")

    def second_player(self, player_1, player_2):
        while True:
            try:
                yield ('read', player_2)
                data = player_2.recv(1024)
                if not data:
                    player_1.send(b'exit')
                    for sock in self.clients_gotv:
                        sock.send(b'exit')
                        sock.close()
                    player_2.close()
                    break
                if data == 'exit':
                    player_2.close()
                    break
                yield ('write', player_1)
                player_1.send(data)
                for sock in self.clients_gotv:
                    sock.send(data)
            except Exception as e:
                print(e)

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
