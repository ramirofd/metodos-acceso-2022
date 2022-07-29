import json
import socket
import argparse
from rich import print

from server.interpreter import Interpreter, InvalidCommandException


class ServerOneClient:
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host: str, port: int):
        print(f"Starting server on: {host}:{port}")
        self.sckt.bind((host, port))
        self.sckt.listen()
        self.interpreter = Interpreter()
        while True:
            print(f"Esperando conexion de cliente.")
            client_sckt, client_addr = self.sckt.accept()
            print(f"[bold]Client connected:[/bold] [green]{client_addr}[/green]")

            while True:
                request = client_sckt.recv(1024).decode()
                print(f"[bold]*{client_addr}*Command received:[/bold] [green]{request}[/green]")

                if request == 'disconnect':
                    break

                command = json.loads(request)
                try:
                    result = self.interpreter.process(command=list(command)[0], data=list(command.values())[0])
                    if isinstance(result, list):
                        data = []
                        for item in result:
                            data.append(dict(zip(item.keys(), item)))

                        response = json.dumps(data)
                    else:
                        response = json.dumps(dict(zip(result.keys(), result)))
                    client_sckt.send(response.encode())
                except InvalidCommandException:
                    client_sckt.send("invalid_command".encode())

            client_sckt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ejemplo de Servidor con Socket")
    parser.add_argument('-i', dest='host', type=str, default='0.0.0.0', help='Direccion IP del host (default=0.0.0.0)')
    parser.add_argument('-p', dest='port', type=int, default=65432, help='Puerto (default=65432)')
    args = parser.parse_args()
    server = ServerOneClient(args.host, args.port)
