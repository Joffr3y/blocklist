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
"""\
[Default]
ListPath = @datadir@/peers.p2p

[iblocklist.com]
URL     = http://www.iblocklist.com/list
Pattern = http:[a-z0-9\/?=&;.]+archiveformat=gz
"""

from configparser import ConfigParser

import blocklist
import os

__all__ = ['Config', 'ConfigError']


class ConfigError(Exception):
    pass


class Config(ConfigParser):

    def __init__(self):
        """Init the config parser and default configuration"""

        ConfigParser.__init__(self)
        modname = blocklist.__name__

        self._datadir = os.path.join(os.environ['HOME'], '.config',  modname)
        self._logfile = os.path.join(self._datadir, modname + '.log')
        self._setting = os.path.join(self._datadir, 'settings.ini')
        self._srcfile = os.path.join(self._datadir, 'sources.list')

        self._init_config()
        self.read(self._setting)

    def _init_config(self):
        """Init a default configuration if it doesn't exist
        """
        try:
            os.mkdir(self._datadir, mode=0o755)
        except FileExistsError:
            pass

        try:
            with open(self._setting, 'x', encoding='utf-8') as config:
                config.write(__doc__.replace('@datadir@', self._datadir))
        except FileExistsError:
            pass

    def get_datadir(self):
        """Return str _datadir classe attribut
        """
        return self._datadir

    def get_logfile(self):
        """Return str _logfile classe attribut
        """
        return self._logfile

    def get_setting(self):
        """Return str _setting classe attribut
        """
        return self._setting

    def get_srcfile(self):
        """Return str _srcfile classe attribut
        """
        return self._srcfile
