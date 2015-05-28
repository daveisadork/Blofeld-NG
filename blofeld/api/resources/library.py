# -*- coding: utf-8 -*-

"""Blofeld API module."""

import logging

import simplejson as json

from .base import Resource, ResourceGetMixin, ResourcePostMixin


class Library(Resource, ResourceGetMixin, ResourcePostMixin):

    """Library resource class."""

    scanner = None
    library = None

    def __init__(self):
        from blofeld.library.backends.mongo import Database
        from blofeld.library.sources.filesystem import Scanner
        self.library = Database()
        self.scanner = Scanner('/Users/dave/Music/Blofeld', self.library)

    def _on_get(self, request, response):
        cursor = self.library.find()
        response.body = json.dumps([song for song in cursor])

    def _on_post(self, request, response):
        logging.info('Starting Library scan')
        response.body = self.scanner.update()
