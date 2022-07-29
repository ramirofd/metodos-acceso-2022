from enum import Enum, auto

from server.database import Database


class Command(Enum):
    DISCONNECT = 'disconnect'
    CREATE_PRODUCT = 'create_product'
    SEARCH_PRODUCT = 'search_product'
    PRODUCT_LIST = 'product_list'
    UPDATE_PRICE = 'update_price'
    UPDATE_QUANTITY = 'update_quantity'
    CREATE_SALE = 'create_sale'
    SELLER_SALES = 'seller_sales'


    def __str__(self):
        return str(self.value)


class Interpreter:
    def __init__(self):
        self.db = Database()

    def process(self, command: str, data):
        pass
