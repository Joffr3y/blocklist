# Blocklist
> Command-line tool for download and write blocklists.

**Blockist** use by default [iblocklist.com](https://www.iblocklist.com/) as lists provider, but others can be added and contributions are welcome.
Its operation is simple, *Blocklist* recovers on a web page with a pattern all blocklists URI. Then it downloads and writes them to a file.

![](screenshot.png)


## Getting the source code
```
https://github.com/Joffr3y/blocklist.git
```

## Dependencies
  * Python ≥ 3.6
  * Python setuptools

## Make dependency
  * GCC compiler

## Installation
```
python setup.py install --user
```
## Datas and configurations files

  * **~/.config/blocklist/settings.ini**  : Configurations.
  * **~/.config/blocklist/sources.list**  : Sources URL.
  * **~/.config/blocklist/peers.p2p**     : Rules list by default.
  * **~/.config/blocklist/blocklist.log** : Logs.

## Usage
```
blocklist --help
usage: blocklist [-h] [-u] [-w] [-q]

Blocklist version 0.1.0

optional arguments:
  -h, --help    show this help message and exit
  -u, --update  Update the sources
  -w, --write   Write the rules
  -q, --quiet   Quiet mode
```
