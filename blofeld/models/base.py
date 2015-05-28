# -*- coding: utf-8 -*-

"""Base resource model stuff."""


class Resource(object):

    """Blofeld base resource model."""

    _document = None

    def __init__(self, document={}):
        """Resource initialization."""
        self._document = document

    def __getattr__(self, name):
        """Resource attribute getter."""
        return self._document.get(name)

    def __setattr__(self, name, value):
        """Resource attribute setter."""
        self._document[name] = value
