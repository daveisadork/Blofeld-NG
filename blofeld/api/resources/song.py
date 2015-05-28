# -*- coding: utf-8 -*-

"""Blofeld API module."""

import logging

import simplejson as json

from .base import Resource, ResourceGetMixin


class Song(Resource, ResourceGetMixin):

    """Library resource class."""

    library = None

    def __init__(self):
        from blofeld.library.backends.mongo import Database
        self.library = Database()

    def _on_get(self, request, response, artist=None, album=None):
        query = {}
        if artist and artist != 'All Artists':
            query['artist'] = artist
        if album and album != 'All Albums':
            query['album'] = album
        cursor = self.library.find(query, sort=[
            ('albumartist', 1),
            ('album', 1),
            ('discnumber', 1),
            ('tracknumber', 1)
        ])
        songs = []
        for song in cursor:
            del song['_id']
            songs.append(song)
        response.body = json.dumps(songs, indent=4)

