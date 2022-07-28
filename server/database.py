import sqlite3


class Interface:

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.cursor = db.cursor()


class Stock(Interface):

    def __init__(self, db: sqlite3.Connection):
        super(Stock, self).__init__(db)
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS stock(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            f'name TEXT, price REAL, quantity REAL)')

    def create(self, name: str, price: float, quantity: float):
        if self.search_product(name) is None:
            self.cursor.execute(f'INSERT INTO stock(name, price, quantity) VALUES(?, ?, ?)', (name, price, quantity))
            self.db.commit()

    def search_product(self, name: str):
        self.cursor.execute(f'SELECT * FROM stock WHERE name=:name', {"name":name})
        return self.cursor.fetchone()

    def update_price(self, name:str, price: float):
        self.cursor.execute(f'UPDATE stock SET price=:price WHERE name=:name', {"name":name, "price":price})
        self.db.commit()

    def update_quantity(self, name:str, quantity: float):
        self.cursor.execute(f'UPDATE stock SET quantity=:quantity WHERE name=:name', {"name":name, "quantity":quantity})
        self.db.commit()


class Database:

    def __init__(self):
        db = sqlite3.connect('database.sqlite')

        self.stock = Stock(db)


