#!/usr/bin/env python3
'''
wahoo's not a pacman wrapper per se,
it's just here because i believe in good UX.

essentially, just helper functions.
'''

# LIBRARIES AND MODULES

import sys

## wahoo stuff

from wahoo.reusables import utils

# CLASSES

# FIXME: everything is inside a class!
#        for usability's sake, all the functions
#        inside the pacwrap class will be moved outside
#        of the class

# TODO: add docstrings here

class pacwrap:
  @staticmethod
  def list(pkg, verbose=False): # no point in adding --silent support
    if not pkg:
      utils.run("pacman -Q", yolo=True, verbose=verbose)
      sys.exit(0)
    
    utils.run(f"pacman -Qs {pkg}", yolo=True, verbose=verbose)

  @staticmethod
  def info(pkg, verbose=False):
    utils.run(f"pacman -Qi {pkg}", yolo=True, verbose=verbose)