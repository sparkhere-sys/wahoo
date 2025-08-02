#!/usr/bin/env python3
'''
Constants. Unchanged stuff.

Import this with `from wahoo.constants import *`.

unlabelled:
* version (float)
* version_str (string)

ANSI colors:
* allow_colors (bool)
* colors (dict)
* styles (dict)
* wahoo_colors (dict)
* reset (string)

salmon specific:
* repo_url (string)
* sal_prefix (string)
* pkgname (string)

pkgmgr.py specific:
* wahoodir (path)
* wahooroot (path)

pyalpm:
* nothing to see here...
'''

# LIBRARIES AND MODULES

import sys
from pathlib import Path

# CONSTANTS

# if you want to add type annotations, be my guest.
# just don't expect me to rely on them.
# unlike linters, i have eyes.
# plus, python is dynamically typed. be DRY. look at the docstring.

version = 0.6 # this doesn't need to be a string i just realized
version_str = str(version)

## ANSI COLORS

_escape = "\u001b"
allow_colors = sys.stdout.isatty() # meaning if not piped to less or something

colors = {
  "white": f"{_escape}[97m" if allow_colors else "",
  "green": f"{_escape}[32m" if allow_colors else "",
  "yellow": f"{_escape}[33m" if allow_colors else "",
  "red": f"{_escape}[31m" if allow_colors else "",
  "blue": f"{_escape}[34m" if allow_colors else ""
}

styles = {
  "bold": f"{_escape}[1m" if allow_colors else "",
  "faint": f"{_escape}[2m" if allow_colors else "",
  "italic": f"{_escape}[3m" if allow_colors else "",
  "underline": f"{_escape}[4m" if allow_colors else "",
  "strike": f"{_escape}[9m" if allow_colors else ""
}

wahoo_colors = { # since i used `if allow_colors else ""` in the above dicts, there's no need for repetition
  "wahoo_message": colors["white"],
  "wahoo_success": colors["green"],
  "wahoo_warn": colors["yellow"],
  "wahoo_error": colors["red"],
  "wahoo_yn": colors["blue"]
}

reset = f"{_escape}[0m" if allow_colors else ""

## SALMON SPECIFIC

repo_url = "https://github.com/sparkhere-sys/wahoo"
sal_prefix = "salmon"
pkgname = "wahoo"

## pkgmgr.py SPECIFIC

wahoodir = Path.home() / ".wahoo"
wahooroot = wahoodir / "source"

wahooroot.mkdir(exist_ok=True, parents=True) # this is the only function call i will put in constants.py, this is only here so i don't have to shove this into parser.py or smth

# sourcedir isn't mentioned here, since that's the source directory of the package being managed

## PYALPM

# TODO: add this later