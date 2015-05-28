# -*- coding: utf-8 -*-

"""Blofeld MongoDB backend."""

from pymongo import MongoClient
from blofeld.library import base


class Database(base.Database):

    """MongoDB database class."""

    _client = None
    _database = None
    _collection = None

    def __init__(self, *args, **kwargs):
        """MongoDB database class initialization."""
        super(Database, self).__init__(*args, **kwargs)

    def _connect(self, *args, **kwargs):
        """Connect to a MongoDB instance."""
        self._client = MongoClient(*args, **kwargs)

    def _get_or_create(self, name, collection='songs'):
        """Get or create a database with the given name."""
        self._database = self._client[name]
        self._collection = self._database[collection]

    def __getattr__(self, name):
        return getattr(self._collection, name)
