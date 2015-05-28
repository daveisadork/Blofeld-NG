# -*- coding: utf-8 -*-

"""Blofeld API module."""

import logging

import falcon

from .resources.library import Library
from .resources.song import Song
from .resources.artist import Artist
from .resources.album import Album
from .resources.cover import Cover


def main():
    """WSGI entry point."""
    logging.debug('Bootstrapping API')
    app = falcon.API()
    library = Library()
    album = Album()
    song = Song()
    artist = Artist()
    cover = Cover()
    app.add_route('/api/albums', album)
    app.add_route('/api/artists', artist)
    app.add_route('/api/library', library)
    app.add_route('/api/songs', song)
    app.add_route('/api/album/{album}', song)
    app.add_route('/api/artist/albums', album)
    app.add_route('/api/artist/{artist}', song)
    app.add_route('/api/artist/{artist}/albums', album)
    app.add_route('/api/songs/{artist}/{album}', song)
    app.add_route('/api/artist/{artist}/album/{album}/songs', song)
    app.add_route('/api/cover/{album}', cover)
    return app


app = main()
