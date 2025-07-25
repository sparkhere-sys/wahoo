#!/usr/bin/env python3
'''
Constants. Unchanged stuff.

Import this with `from wahoo.constants import *`.

unlabelled:
* version (float)

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
'''

# LIBRARIES AND MODULES

import sys

# CONSTANTS

version = 0.6 # this doesn't need to be a string i just realized

## ANSI COLORS

allow_colors = sys.stdout.isatty() # meaning if not piped to less or something

colors = {
  "white": "\u001b[97m" if allow_colors else "",
  "green": "\u001b[32m" if allow_colors else "",
  "yellow": "\u001b[33m" if allow_colors else "",
  "red": "\u001b[31m" if allow_colors else "",
  "blue": "\u001b[34m" if allow_colors else ""
}

styles = {
  "bold": "\u001b[1m" if allow_colors else "",
  "faint": "\u001b[2m" if allow_colors else "",
  "italic": "\u001b[3m" if allow_colors else "",
  "underline": "\u001b[4m" if allow_colors else "",
  "strike": "\u001b[9m"
}

wahoo_colors = { # since i used `if allow_colors else ""` in the above dict, there's no need for repetition
  "wahoo_message": colors["white"],
  "wahoo_success": colors["green"],
  "wahoo_warn": colors["yellow"],
  "wahoo_error": colors["red"],
  "wahoo_yn": colors["blue"]
}

reset = "\u001b[0m" if allow_colors else ""

## SALMON SPECIFIC

repo_url = "https://github.com/sparkhere-sys/wahoo"
sal_prefix = "salmon"
pkgname = "wahoo"
