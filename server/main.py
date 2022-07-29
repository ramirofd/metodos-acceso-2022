import socket
from rich import print


class ServerOneClient:

    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host: str, port: int):
        self.sckt.bind((host, port))
        self.sckt.listen(3)
        while True:
            client_sckt, client_addr = self.sckt.accept()
            print(f"[bold]Client connected:[/bold] [green]{client_addr}[/green]")

            request = ''
            while request != 'disconnect':
                request = client_sckt.recv(1024).decode()
                print(f"[bold]*{client_addr}*Command received:[/bold] [green]{request}[/green]")

                client_sckt.send(request.encode())
            client_sckt.send("disconnect".encode())
            client_sckt.close()


if __name__ == '__main__':
    server = ServerOneClient('0.0.0.0', 65432)