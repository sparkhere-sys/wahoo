#!/usr/bin/env python3
'''
wahoo's not a pacman wrapper per se,
it's just here because i believe in good UX.

essentially, just helper functions.
'''

# LIBRARIES AND MODULES

import sys

## wahoo stuff

import wahoo.utils as utils

# FUNCTIONS

# TODO: add docstrings here

def list(pkg, verbose=False): # no point in adding --silent support
  if not pkg:
    utils.run("pacman -Q", yolo=True, verbose=verbose)
    sys.exit(0)
    
  utils.run(f"pacman -Qs {pkg}", yolo=True, verbose=verbose)

def info(pkg, verbose=False):
  utils.run(f"pacman -Qi {pkg}", yolo=True, verbose=verbose)