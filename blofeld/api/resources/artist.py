# -*- coding: utf-8 -*-

"""Blofeld API module."""

import logging

import simplejson as json

from .base import Resource, ResourceGetMixin


class Artist(Resource, ResourceGetMixin):

    """Artist resource class."""

    library = None

    def __init__(self):
        from blofeld.library.backends.mongo import Database
        self.library = Database()

    def _on_get(self, request, response):
        cursor = self.library.distinct('artist')
        cursor.sort()
        response.body = json.dumps([artist for artist in cursor], indent=4)
