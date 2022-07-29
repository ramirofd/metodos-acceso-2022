import argparse
import json
import socket
from rich import print


class Application:
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    seller = None

    def __init__(self, host: str, port: int):
        self.sckt.connect((host, port))
        self.main_menu()

    def main_menu(self):
        while True:
            print(f"1. Cargar datos ejemplo.")
            print(f"2. Cargar producto a mano.")
            print(f"3. Listar Stock disponible.")
            print(f"0. Salir")
            opt = int(input("\nSeleccione una opcion: "))
            while opt < 0 or opt > 5:
                opt = int(input("Opcion incorrecta, ingrese [0-7]: "))
            if opt == 0:
                break
            elif opt == 1:
                self.load_example_data()
            elif opt == 2:
                self.load_product()
            elif opt == 3:
                self.list_stock()
            elif opt == 4:
                pass
            else:
                pass
        self.close_connection()

    def close_connection(self):
        self.sckt.sendall('disconnect'.encode())
        self.sckt.close()

    def send_command(self, command: str, data: dict):
        request = json.dumps({command: data})
        self.sckt.send(request.encode())
        response = self.sckt.recv(1024).decode()
        return json.loads(response)

    def load_example_data(self):
        command = "create_product"
        data = [
            {
                "name": "TOMATE",
                "price": 124.5,
                "quantity": 50.0
            },
            {
                "name": "NARANJA",
                "price": 80,
                "quantity": 25.0
            },
            {
                "name": "ZANAHORIA",
                "price": 100.,
                "quantity": 30.0
            },
            {
                "name": "RUCULA",
                "price": 180.7,
                "quantity": 10.0
            }
        ]
        for item in data:
            created = self.send_command(command, item)
            print(f"Created: {created}")
        print()

    def load_product(self):
        command = "create_product"
        print("Ingrese los datos del producto:")
        name = input("Nombre: ")
        price = float(input("Precio: "))
        quantity = float(input("Cantidad: "))
        created = self.send_command(command, {
                "name": name,
                "price": price,
                "quantity": quantity
        })
        print(f"Created: {created}")
        print()

    def list_stock(self):
        command = "product_list"
        data = {
            "names": [],
        }
        stock = self.send_command(command, data)
        for item in stock:
            print(f"{item['name']}: {item['price']}. Cantidad: {item['quantity']}")
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ejemplo de Servidor con Socket")
    parser.add_argument('-i', dest='host', type=str, default='127.0.0.1',
                        help='Direccion IP del host (default=127.0.0.1)')
    parser.add_argument('-p', dest='port', type=int, default=65432, help='Puerto (default=65432)')
    args = parser.parse_args()
    Application(args.host, args.port)
