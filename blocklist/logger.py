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

from logging.handlers import RotatingFileHandler
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG

import ui

import traceback
import logging
import sys

__all__ = ['Logger']


class Logger(logging.Logger):
    """Override logging.Logger class"""

    def __init__(self, fpath, stream, name='process'):
        logging.Logger.__init__(self, name)

        self._stream = stream

        file_handler = RotatingFileHandler(
            filename=fpath,
            mode='a',
            maxBytes=1048576,   # 1 Mio
            backupCount=1,
            encoding='utf-8'
        )

        fmt = '%(asctime)s - %(levelname)s - %(message)s'
        file_handler.setFormatter(logging.Formatter(fmt))
        file_handler.setLevel(DEBUG)

        self.addHandler(file_handler)

    def info(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'INFO'.
        """
        self._log(INFO, msg, args, **kwargs)
        if self._stream:
            ui.info(msg)

    def warning(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'WARNING'.
        """
        self._log(WARNING, msg, args, **kwargs)
        if self._stream:
            ui.err(msg, 'yellow')

    def error(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'ERROR'.
        """
        self._log(ERROR, msg, args, **kwargs)
        if self._stream:
            ui.err(msg, 'red')

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        self._log(ERROR, msg, args, exc_info=True, **kwargs)
        t, v, tb = sys.exc_info()
        traceback.print_exception(t, v, tb, None, sys.stderr)

    def critical(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'CRITICAL'.
        """
        self._log(CRITICAL, msg, args, **kwargs)
        if self._stream:
            ui.err(msg, 'red')
