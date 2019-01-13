# Copyright (C) 2018 Joffrey Darcq
#
# This file is part of Blocklist.
#
# Blocklist is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Blocklist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public licenses
# along with Blocklist.  If not, see <https://www.gnu.org/licenses/>.

from blocklist.config import ConfigError

from contextlib import contextmanager

import urllib.request
import re

__all__ = ['Request']


class Request(object):
    """Defines a Request class object"""

    def __init__(self, agent='Mozilla/5.0'):
        self._opener = urllib.request.build_opener()
        self._opener.addheaders = [('User-agent', agent)]

    @contextmanager
    def urlopen(self, url):
        """urlopen contextmanager with opener class attribut
        """
        try:
            req = self._opener.open(url)
            yield req
        finally:
            req.close()

    def findall(self, url, pattern):
        """Return list of elements matched in page content

        Parameters :

            url     : URL target
            pattern : Pattern to matched
        """
        with self.urlopen(url) as f:
            url_lst = re.findall(pattern, str(f.read()))

            if not url_lst:
                raise ConfigError(f'Bad pattern: "{pattern}"')

            return url_lst

    def download(self, url, fname, status, index='', length=16384):
        """Download a file and return its type, fsize

        Parameters :

            url    : URL target
            fname  : File name
            index  : Download index ex (1/10) (optional)
            status : Callback to a status function (optional)
            length : Stream size written by loop turn (default 16 Kio)
        """
        with self.urlopen(url) as fstream, \
                open(fname, 'wb') as fdown:

            fsize = int(fstream.getheader('Content-Length'))
            ftype = fstream.getheader('Content-Type')
            ftype = ftype.split('/')[-1].split('-')[-1]  # ftype = NO/NO-YES

            loaded = 0

            while 'stream':
                stream = fstream.read(length)

                if not stream:
                    break

                loaded += len(stream)
                fdown.write(stream)
                status(f'{index} {fname}', loaded, fsize)

        return ftype, fsize
