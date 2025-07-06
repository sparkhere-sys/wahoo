#!/usr/bin/python3

# wahoo!
# rewritten!
# this will be the v0.5 of wahoo.
# certain lines of code will be commented out with two #s.
# that is an intentional decision :)
# feel free to improve the docstrings, just leave the commments alone

version = 0.5 # this doesn't need to be a string i just realized
colors = {
  "white": "\u001b[97m",
  "green": "\u001b[32m",
  "yellow": "\u001b[33m",
  "red": "\u001b[31m",
  "blue": "\u001b[34m"
}

# LIBRARIES AND MODULES

import sys
from pathlib import Path
## from subprocess import run
import subprocess

## PIP

import requests
from rapidfuzz import fuzz

# CLASSES

# NOTE: idk why this is here since i could just move findflags() to outside this class?
#       ig its here for organization (which was much needed, especially for something like wahoo)


class argparser:
  @staticmethod
  def findflags():
    flags = [arg for arg in sys.argv[1:] if arg.startswith("--")]
    return flags

class cli:
  @staticmethod
  def echo(msg, prefix="wahoo", color, return=False)
    '''
    prints with color
    '''

    reset = "\u001b[0m"
    echoed = f"{color}{prefix + ":" if prefix else None} {reset}{msg}"

    if not return:
      print(echoed)
      return # ironic isn't it?
    
    return echoed

  @staticmethod
  def prompt(msg, yolo=False, dont_exit=True, use_msg_as_prompt=False, show_abort_msg=True, default=True, prompt="[Y/n]")
    '''
    prompt. what more do you want me to say?
    TODO: write proper docstrings
    '''
    if not yolo:
      usrinput = input(f"{cli.echo(msg, color=None, return=True)} {" " + prompt if use_msg_as_prompt else f"\nProceed? {prompt} "})
      if usrinput.lower() == "n":
        return False
      elif not usrinput.split():
        return default
      elif usrinput.lower == "y":
        return True
      else:
        cli.echo(f"Taking '{usrinput}' as {"yes" if default else "no"}.", "wahoo warn", None)
        return default
    else:
      return default

  @staticmethod
  def help():
    # TODO: add help
    pass

  @staticmethod
  def flagparsing(flags):
    parsed_flags = {
      "flag_yolo": False,
      "flag_rns": False
    }
    
    for flag in flags:
      match flag:
        case ("--yolo" | "--noconfirm"):
          parsed_flags["flag_yolo"] = True
        case ("--dont-remove-depends" | "--dontremovedepends"):
          parsed_flags["flag_rns"] = True
        case _:
          cli.echo(f"Unknown flag: '{flag}'. Ignoring.", "wahoo warn", None)
    
    return parsed_flags

  @staticmethod
  def main():
    '''
    WOHOHOHOHOHOHOHO
    TODO: add docstrings
    '''
    pass

