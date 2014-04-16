"""
Storage concerns itself with persisting data
"""

from sqlalchemy import create_engine


class Container(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Container, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self, connection, verbose=False):
        self.engine = create_engine(connection, echo=verbose)
