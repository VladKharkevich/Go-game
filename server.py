from socket import *
from select import select
from random import randint
import threading
import pickle


class Server:

    def __init__(self):
        self.to_monitor = []
        self.size_board = [None]
        self.current_games = []
        self.myHost = ''
        self.myPort = 50009
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.myHost, self.myPort))
        self.server_socket.listen(5)
        self.to_monitor.append(self.server_socket)
        self.run()

    def get_client(self):
        client_socket, address = self.server_socket.accept()
        print('Server connected by', address)
        self.to_monitor.append(client_socket)
        size_board = client_socket.recv(1024)
        size_board = pickle.loads(size_board)
        self.size_board.append(size_board)

    def event_loop(self):
        while True:
            ready_to_read, _, _ = select(self.to_monitor, [], [])
            for sock in ready_to_read:
                if sock is self.server_socket:
                    self.get_client()

    def check_sizes(self):
        while True:
            for i in range(1, len(self.size_board) - 1):
                if self.size_board[i] == self.size_board[-1]:
                    self.make_game(i)
                    break

    def make_game(self, pos):
        self.current_games.append((self.to_monitor[pos], self.to_monitor[-1]))
        self.to_monitor.pop(pos)
        self.to_monitor.pop(-1)
        self.size_board.pop(pos)
        self.to_monitor.pop(-1)
        thr_game = threading.Thread(target=self.start_game)
        thr_game.start()

    def start_game(self):
        side = randint(0, 1)
        player_1, player_2 = self.current_games[-1]
        player_1.send(b'Start' + str(side).encode())
        player_2.send(b'Start' + str(side^1).encode())
        if not side:
            player_1, player_2 = player_2, player_1
        queue = [player_1, player_2]
        while True:
            try:
                data = queue[0].recv(1024)
                if not data:
                    queue[0].close()
                    queue[1].close()
                    break
                queue[1].send(data)
                temp = queue.pop(0)
                queue.append(temp)
            except:
                break

    def run(self):
        thr_connecter = threading.Thread(target=self.event_loop)
        thr_checker = threading.Thread(target=self.check_sizes)
        thr_connecter.start()
        thr_checker.start()


if __name__ == '__main__':
    s = Server()

'''
        Необходимо добавить возможность множественного подключения, 
    при подключении спросить размер доски. Если где-то размеры совпадают, 
    то создать для них отдельный поток игры, после удалить из списка 
    для мониторинга и продолжать дальше ждать.

    Первый поток: ожидание пользователей и add self.to_monitor.
    Второй поток: ждет, когда когда-то совпадут размеры. Если совпадают, то 
    удалить из self.to_monitor и создать для них отдельный поток с игрой. 

'''