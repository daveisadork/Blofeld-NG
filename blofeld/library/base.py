# -*- coding: utf-8 -*-

"""Blofeld database abstraction module."""


class Database(object):

    """Base abstraction class for databases."""

    def __init__(self, server=None, database=None):
        """Base database initialization."""
        super(Database, self).__init__()
        if server is None:
            self.connect()
        if server:
            self.connect(server)
        if database is None:
            self.get_or_create()
        if database:
            self.get_or_create(database)

    def _connect(self, *args, **kwargs):
        """Method for connecting to a server.

        This method is intended to be overridden by the backend's subclass.
        """

    def connect(self, *args, **kwargs):
        """Wrapper method for connecting to a server."""
        self._connect(*args, **kwargs)

    def _get_or_create(self, name, **kwargs):
        """Method for getting or creating a database.

        This method is intended to be overridden by the backend's subclass.
        """

    def get_or_create(self, name='blofeld', **kwargs):
        """Get or create a database."""
        self._get_or_create(name)
