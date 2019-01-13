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

from contextlib import contextmanager, ContextDecorator

import os
import gzip
import tempfile
import shutil


__all__ = ['WorkInTMP', 'Func']


class WorkInTMP(ContextDecorator):
    """Defines a ContextDecorator class

    All func decoreted with it work in temporary directory
    When the process is finish the temporary directory is removed

    Usable as contextmanager and decorator.
    """

    def __enter__(self):
        self._tmpdir = tempfile.mkdtemp(prefix='blocklist_')
        os.chdir(self._tmpdir)

    def __exit__(self, *exc):
        shutil.rmtree(self._tmpdir)


class Func(object):
    """Defines a Func class for various functions"""

    @staticmethod
    @contextmanager
    def open(fname, ftype=None):
        """Open text|gzip file type
        """
        try:
            if 'gzip' in ftype:
                f = gzip.open(fname, 'rt', encoding='utf-8', errors='replace')
            else:
                f = open(fname, 'rt', encoding='utf-8', errors='replace')
            yield f
        finally:
            f.close()

    @staticmethod
    def countline(fpath):
        """Return the number of line in a file"
        """
        with open(fpath, 'r') as f:
            return sum(1 for nbline in f)

    @staticmethod
    def do_nothing(*args):
        pass
