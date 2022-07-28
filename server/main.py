# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from database import Database

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    db = Database()
    # db.sales.create("ALFREDO", [
    #     {
    #         "id": 4,
    #         "quantity": 1.66,
    #         "price": 63.00
    #     },
    #     {
    #         "id": 6,
    #         "quantity": 0.45,
    #         "price": 5.00
    #     }
    # ])
    db.sales.seller_sales("RAMIRO")
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
