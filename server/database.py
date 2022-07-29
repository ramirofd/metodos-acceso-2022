import sqlite3
from datetime import datetime


class Database:

    def __init__(self):
        self.db = sqlite3.connect('stock.db')
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS stock(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            f'name TEXT, price REAL, quantity REAL)')

    def create_product(self, name: str, price: float, quantity: float):
        if self.search_product(name) is None:
            self.cursor.execute(f'INSERT INTO stock(name, price, quantity) VALUES(?, ?, ?)',
                                (name, price, quantity))
            self.db.commit()
        return self.search_product(name)

    def search_product(self, name: str):
        self.cursor.execute(f'SELECT * FROM stock WHERE name=:name', {"name": name})
        return self.cursor.fetchone()

    def product_list(self, names: list):
        if len(names) == 0:
            self.cursor.execute(f"SELECT * FROM stock")
        else:
            self.cursor.execute(f"SELECT * FROM stock WHERE name IN ({','.join(['?'] * len(names))})", names)
        return self.cursor.fetchall()


