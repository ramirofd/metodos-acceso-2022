from enum import Enum, auto

from server.database import Database


class InvalidCommandException(Exception):
    pass


class Interpreter:
    def __init__(self):
        self.db = Database()

    def process(self, command: str, data):

        try:
            fn = getattr(self.db, command)
            return fn(**data)
        except AttributeError:
            raise InvalidCommandException()
