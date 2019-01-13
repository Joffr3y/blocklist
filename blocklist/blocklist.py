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

from blocklist.func import WorkInTMP, Func
from blocklist.request import Request
from blocklist.logger import Logger
from blocklist.config import Config

import ui

__all__ = ['Blocklist']


class Blocklist(Request, Config, Logger):
    """Defines the Main class of Blocklist module"""

    def __init__(self, stream):
        Config.__init__(self)
        Request.__init__(self)
        Logger.__init__(self, self.get_logfile(), stream)

        self.debug('Use configuration: "' + self.get_setting() + '"')

        if stream:
            self._status = ui.statusprocess
            self._endl = print
        else:
            self._status = Func.do_nothing
            self._endl = Func.do_nothing

        self._fsrc = self.get_srcfile()
        self._nurl = 0  # N URL find in sources.list

        self.debug('Use the source : "' + self._fsrc + '"')

    @WorkInTMP()
    def update_src(self):
        """Parse site(s) page and write blocklist url in url file
        """
        self.info('Update source(s)…')

        with open(self._fsrc, 'w', encoding='utf-8') as f:

            for section in self.sections()[1:]:  # Except Default section
                url = self[section]['URL']
                pat = self[section]['Pattern']

                msg = ' section ' + section
                self.debug(msg)

                for uri in self.findall(url, pat):
                    f.write(uri + '\n')
                    self._nurl += 1

                self._status(msg, 0, 0, False)
                self._endl()

        self.info(f'{self._nurl} URL found')

    @WorkInTMP()
    def write_rules(self):
        """Download lists and write them in "ListPath"
        """
        self.info('Download and write rules…')
        listpath = self['Default']['ListPath']
        self.debug(f'Use Listpath: "{listpath}"')

        with open(listpath, 'w', encoding='utf-8') as flist, \
                open(self._fsrc, 'r', encoding='utf-8') as furl:

            if not self._nurl:
                self._nurl = Func.countline(self._fsrc)

            nfile, nrule = 1, 0

            for url in furl:
                fname = url.split('/')[2]   # Get Second + Grand Level Domain
                index = '(' + ui.index(nfile, self._nurl) + ')'

                ftype, fsize = self.download(
                    url, fname, self._status, ' ' + index
                )

                msg = f' {index} {fname}...'
                self._status(msg, fsize, fsize)

                with Func.open(fname, ftype) as f:
                    for line in f:
                        if line and line[0] not in ('#', '\n'):
                            flist.write(line)
                            nrule += 1

                nfile += 1
                msg += ' written'

                self.debug(msg)
                self._status(msg, fsize, fsize)
                self._endl()

        self.info(f'{nrule} rules written with {nfile - 1}/{self._nurl} files')
