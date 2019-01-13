# coding: utf-8
from blocklist.func import WorkInTMP
from blocklist.request import Request

import sys
import ui


@WorkInTMP()
def main(*urls):
    req = Request()

    i, total = 1, len(urls)
    for url in urls:
        req.download(
            url,
            fname=url.split('/')[-1],
            index=f'({i}/{total})',
            status=ui.statusprocess
        )
        i += 1
        sys.stdout.write('\n')


if __name__ == '__main__':
    try:
        main(
            'http://ipv4.download.thinkbroadband.com/1MB.zip',
            'http://ipv4.download.thinkbroadband.com/5MB.zip',
            'http://ipv4.download.thinkbroadband.com/10MB.zip',
        )
    except KeyboardInterrupt:
        sys.exit('KeyboardInterrupt')
