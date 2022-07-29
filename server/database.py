import sqlite3
from datetime import datetime


class Interface:

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.cursor = db.cursor()


class Stock(Interface):

    def __init__(self, db: sqlite3.Connection):
        super(Stock, self).__init__(db)
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS stock(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            f'name TEXT, price REAL, quantity REAL)')

    def create_product(self, name: str, price: float, quantity: float):
        if self.search_product(name) is None:
            self.cursor.execute(f'INSERT INTO stock(name, price, quantity) VALUES(?, ?, ?)', (name, price, quantity))
            self.db.commit()
            return self.search_product(name)

    def search_product(self, name: str):
        self.cursor.execute(f'SELECT * FROM stock WHERE name=:name', {"name":name})
        return self.cursor.fetchone()

    def product_list(self, names: list):
        self.cursor.execute(f"SELECT * FROM stock WHERE name IN ({','.join(['?']*len(names))})", names)
        return self.cursor.fetchall()

    def update_price(self, name:str, price: float):
        self.cursor.execute(f'UPDATE stock SET price=:price WHERE name=:name', {"name":name, "price":price})
        self.db.commit()
        return self.search_product(name)

    def update_quantity(self, name:str, quantity: float):
        self.cursor.execute(f'UPDATE stock SET quantity=:quantity WHERE name=:name', {"name":name, "quantity":quantity})
        self.db.commit()
        return self.search_product(name)


class Sales(Interface):

    def __init__(self, db: sqlite3.Connection):
        super(Sales, self).__init__(db)
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS sale(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            f'seller TEXT, date timestamp)')
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS sale_stock(sale_id INTEGER, stock_id INTEGER, quantity REAL, '
                            f'price REAL)')

    def create_sale(self, seller: str, products: list):
        self.cursor.execute(f'INSERT INTO sale(seller, date) VALUES(?, ?)', (seller, datetime.now()))
        sale_id = self.cursor.lastrowid
        for product in products:
            product['sale_id'] = sale_id
            self.cursor.execute(f"INSERT INTO sale_stock(stock_id, quantity, price, sale_id) "
                                f"VALUES(?, ?, ?, ?)", tuple(product.values()))
        self.db.commit()

    def seller_sales(self, seller: str):
        self.cursor.execute(f"SELECT sales.date, sale_stock.quantity, sale_stock.price FROM (SELECT id, date FROM sale WHERE seller=(?))"
                            f" as sales INNER JOIN sale_stock ON sales.id = sale_stock.sale_id", (seller, ))
        return self.cursor.fetchall()


class Database:

    def __init__(self):
        db = sqlite3.connect('stock.db')
        db.row_factory = sqlite3.Row
        self.stock = Stock(db)
        self.sales = Sales(db)


