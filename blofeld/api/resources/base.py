# -*- coding: utf-8 -*-

"""Blofeld base API resource module."""

import logging


class Resource(object):

    """Base API Resource class."""


class ResourceGetMixin(object):

    """API Resource GET mixin."""

    def on_get(self, *args, **kwargs):
        """HTTP GET handler. Calls the subclass's _on_get method."""
        logging.debug('%s.on_get(%s, %s)' % (type(self).__name__, args, kwargs))
        self._on_get(*args, **kwargs)

    def _on_get(self, *args, **kwargs):
        """HTTP GET handler. Intended to be overridden by subclasses."""


class ResourcePostMixin(object):

    """API Resource POST mixin."""

    def on_post(self, *args, **kwargs):
        """HTTP POST handler. Calls the subclass's _on_post method."""
        logging.debug('%s.on_get(%s, %s)' % (type(self).__name__, args, kwargs))
        self._on_post(*args, **kwargs)

    def _on_post(self, *args, **kwargs):
        """HTTP POST handler. Intended to be overridden by subclasses."""
