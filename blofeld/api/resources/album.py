# -*- coding: utf-8 -*-

"""Blofeld API module."""

import logging

import simplejson as json

from .base import Resource, ResourceGetMixin


class Album(Resource, ResourceGetMixin):

    """Library resource class."""

    library = None

    def __init__(self):
        from blofeld.library.backends.mongo import Database
        self.library = Database()

    def _on_get(self, request, response, artist=None):
        response.set_headers([('Access-Control-Allow-Origin', '*')])
        query = {}
        if artist and artist not in ('album', 'All Artists'):
            query['artist'] = artist
        cursor = self.library._database.albums.find(query)
        albums = []
        for album in cursor:
            album.pop('_id')
            albums.append(album)
        response.body = json.dumps(albums, indent=4)
