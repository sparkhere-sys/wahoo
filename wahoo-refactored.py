#!/usr/bin/python3

# wahoo!
# rewritten!
# this will be the v0.5 of wahoo.
# certain lines of code will be commented out with two #s.
# that is an intentional decision :)
# feel free to improve the docstrings, just leave the commments alone

# BASIC GUIDE TO THE STYLING
# * cli.echo() is used instead of raw print()
# * section headers are in all caps (i.e, "# THIS IS A SECTION HEADER")
# * everything is in snake_case (yes, even the class names. screw capitalization.)
# * this version of wahoo is built modular (not in the sense of python modules) meaning that
#   it should be easier to add new features.
# * do not use emojis anywhere. in strings, in docstrings, in comments, just please don't.

# NOTE: do not try to use this script as a python module (i.e, "import wahoo")
#       this is a CLI tool, not a library.
#       if you must use it as a module, then it is recommended to just make it yourself
#       (meaning, copy the code and replace all the CLI related stuff with your own)

# EXIT CODE GUIDE
# 0 = success
# 1 = general error
# 2 = cli error
# 3 = self-update error
# 11 = segfault easter egg
# everything else: i have no idea what happened but it was so catastrophic 
#                  that it exitted with an unidentified exit code

# CONSTANTS

version = 0.5 # this doesn't need to be a string i just realized

## ANSI COLORS

allow_colors = sys.stdout.isatty() # meaning if not piped to less or something

colors = {
  "white": "\u001b[97m" if allow_colors else "",
  "green": "\u001b[32m" if allow_colors else "",
  "yellow": "\u001b[33m" if allow_colors else "",
  "red": "\u001b[31m" if allow_colors else "",
  "blue": "\u001b[34m" if allow_colors else ""
}

wahoo_colors = { # since i used `if allow_colors else ""` in the above dict, there's no need for repetition
  "wahoo_message": colors["white"],
  "wahoo_success": colors["green"],
  "wahoo_warn": colors["yellow"],
  "wahoo_error": colors["red"],
  "wahoo_yn": colors["blue"]
}

reset = "\u001b[0m" if allow_colors else ""

# LIBRARIES AND MODULES

import sys
from pathlib import Path # we love python 3
import subprocess

## PIP PACKAGES (aka, dependencies.)

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
  def echo(msg, color=wahoo_colors["wahoo_message"], prefix="wahoo", do_return=False):
    '''
    prints with color
    '''
    # with how many times i call this function with "color=None",
    # its starting to get ironic (yk, given the whole "prints with color" docstring)
    # anyway this is just a developer "lol moment"

    echoed = f"{color}{prefix + ':' if prefix else ''} {reset}{msg}"

    if not do_return:
      print(echoed)
      return # ironic isn't it?
    
    return echoed

  @staticmethod
  def prompt(msg, yolo=False, dont_exit=True, use_msg_as_prompt=False, show_abort_msg=True, default=True, promptmsg="[Y/n]"):
    '''
    prompt. what more do you want me to say?
    TODO: write proper docstrings
    '''
    if not yolo:
      usrinput = input(f"{cli.echo(msg, color=None, do_return=True)}{(' ' + promptmsg) if use_msg_as_prompt else ('\nProceed? ' + promptmsg + ' ')}")
      if usrinput.lower() == "n":
        if show_abort_msg:
          cli.echo("Aborted.", color=None, prefix=None)
        
        if dont_exit:
          return False
        else:
          sys.exit(1)

      elif not usrinput.split():
        return default
      elif usrinput.lower() == "y":
        return True
      else:
        cli.echo(f"Taking '{usrinput}' as {"yes" if default else "no"}.", "wahoo warn", None)
        return default
    else:
      return default


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
  def help():
    pass

  @staticmethod
  def version():
    cli.echo(f"{colors["yellow"]}v{version}{reset}", color=wahoo_colors["wahoo_success"], prefix="wahoo")
    cli.echo("Made with <3 by Spark", prefix=None, color=None)

  @staticmethod
  def main():
    '''
    WOHOHOHOHOHOHOHO
    TODO: add docstrings
    '''
    pass

class utils:
  @staticmethod
  def internet_check(timeout=3):
    '''
    TODO: add docstrings
    '''
    try:
      requests.get("https://archlinux.org", timeout=timeout)
    except requests.RequestException: # meaning no internet
      return False
    
    return True
  
  @staticmethod
  def run(cmd, dir=None, yolo=False, dont_exit=True, verbose=True, silent=False):
    '''
    TODO: add docstrings
    '''
    if not yolo:
      if not cli.prompt(f"Running command: {cmd}", yolo=yolo, dont_exit=dont_exit, use_msg_as_prompt=False): # use_msg_as_prompt is false for parity with the original version of wahoo
        if not dont_exit:
          sys.exit(0)
        else:
          return # doesn't need to return anything, just exits the function.
        
    try:
      subprocess.run(cmd + "> /dev/null 2>&1" if silent else '', shell=True, check=True, cwd=dir)
      return # doesn't need to return anything, just exits the function.
    
    except subprocess.CalledProcessError as e:
      # i refuse to just recycle the error handling from the old version of wahoo,
      # that was a mess.
      # TODO: make better error handling
      cli.echo(f"Command failed.", prefix="wahoo error", color=None)
      if verbose:
        cli.echo(f"Command: {cmd}", color=None, prefix=None)
        cli.echo(f"Details: {e}", color=None, prefix=None)
    
  @staticmethod
  def sudo_check():
    if os.getuid() == 0:
      cli.echo("Please do not run wahoo as root.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
      sys.exit(2)

# FUNCTIONS
def install():
  # im gonna recycle the old install() function from the old version of wahoo
  pass

# INIT

if __name__ == "__main__":
  try:
    cli.main()
  except KeyboardInterrupt:
    cli.echo("Interrupted by Ctrl+C, see ya next time")
    sys.exit(0)