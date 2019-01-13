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

from blocklist.blocklist import Blocklist

import blocklist

import sys
import os
import argparse

__all__ = ['main']


def main():
    """Run Blocklist in command-line"""

    try:
        sys.argv[1]
    except IndexError:
        print('usage: [-h|--help]', file=sys.stderr)
        sys.exit('Error: no argument')

    try:
        parser = argparse.ArgumentParser(
            prog=blocklist.__name__,
            description=f'Blocklist version {blocklist.__version__}'
        )
        parser.add_argument(
            '-u', '--update', action='store_true',
            help='Update the sources'
        )
        parser.add_argument(
            '-w', '--write', action='store_true',
            help='Write the rules'
        )
        parser.add_argument(
            '-q', '--quiet', action='store_false',
            help='Quiet mode'
        )
        args = parser.parse_args()

        blk = Blocklist(stream=args.quiet)

        if args.update:
            blk.update_src()
        if args.write:
            blk.write_rules()

    except PermissionError as exc:
        if os.access(blk.get_logfile(), os.W_OK):
            blk.critical(exc)
        else:
            print(exc, file=sys.stderr)
        sys.exit(77)

    except KeyboardInterrupt:
        blk.warning('KeyboardInterrupt')
        sys.exit(130)

    except Exception as exc:
        blk.exception(exc)
        sys.exit(1)

    sys.exit(0)
