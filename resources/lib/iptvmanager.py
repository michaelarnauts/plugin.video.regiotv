# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Implementation of IPTVManager class"""

from __future__ import absolute_import, division, unicode_literals
from data import CHANNELS


class IPTVManager(object):
    """Interface to IPTV Manager"""

    def __init__(self, port):
        """Initialize IPTV Manager object"""
        self.port = port

    def via_socket(func):
        """Send the output of the wrapped function to socket"""

        def send(self):
            """Decorator to send over a socket"""
            import json
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', self.port))
            try:
                sock.send(json.dumps(func()))
            finally:
                sock.close()

        return send

    @via_socket
    def send_channels():
        """Return JSON-M3U formatted information to IPTV Manager"""
        streams = []
        for channel in CHANNELS:
            if not channel.get('live_stream'):
                continue
            streams.append(dict(
                id=channel.get('website'),
                name='{name} ({label})'.format(**channel),
                logo=channel.get('logo'),
                preset=channel.get('preset'),
                stream=channel.get('live_stream'),
            ))
        return dict(version=1, streams=streams)
