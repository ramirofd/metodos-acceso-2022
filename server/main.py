import socket
from rich import print

from server.interpreter import Command


class ServerOneClient:

    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host: str, port: int):
        self.sckt.bind((host, port))
        self.sckt.listen(3)
        while True:
            client_sckt, client_addr = self.sckt.accept()
            print(f"[bold]Client connected:[/bold] [green]{client_addr}[/green]")

            request = client_sckt.recv(1024).decode()
            while request != Command.DISCONNECT.value:
                print(f"[bold]*{client_addr}*Command received:[/bold] [green]{request}[/green]")
                # ToDo: Process command with Interpreter
                client_sckt.send(request.encode())
                request = client_sckt.recv(1024).decode()

            client_sckt.sendall(request.encode())
            client_sckt.close()


if __name__ == '__main__':
    server = ServerOneClient('0.0.0.0', 65432)