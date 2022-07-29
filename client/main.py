import socket
from rich import print


class Client:
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host: str, port: int):
        self.sckt.connect((host, port))
        response = ''
        while response != 'disconnect':
            command = input("Ingrese comando: ")
            self.sckt.sendall(command.encode())
            response = self.sckt.recv(1024).decode()
            print(response)
        self.sckt.close()


if __name__ == '__main__':
    client = Client('127.0.0.1', 65432)