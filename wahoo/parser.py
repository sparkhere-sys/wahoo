#!/usr/bin/env python3
'''
Main CLI entry point.
'''

# LIBRARIES AND MODULES

import sys

## wahoo stuff

from wahoo.cliutils import cli
import wahoo.main as main
from wahoo.pacwrap import pacwrap
from wahoo.constants import *
import wahoo.salmon as salmon

# FUNCTIONS

def find_args():
  '''
  Finds flags and positional arguments.
  '''

  ## flags = [arg for arg in sys.argv[1:] if arg.startswith("--")]
  ## positional = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

  # these oneliners also work!
  # i only commented them out for readability.

  flags = []
  positional = []

  for arg in sys.argv[1:]:
    if arg.startswith("--"):
      flags.append(arg)
    else:
      positional.append(arg)

  return flags, positional

def flagparsing(flags):
  '''
  Parses flags.
  '''
    
  parsed_flags = {
    "flag_yolo": False,
    "flag_rns": False,
    "flag_verbose": True,
    "flag_silent": False
  }
    
  for flag in flags:
    match flag:
      case ("--yolo" | "--noconfirm"):
        parsed_flags["flag_yolo"] = True
      case ("--dont-remove-depends" | "--dontremovedepends"):
        parsed_flags["flag_rns"] = True
      case "--no-error-details":
        parsed_flags["flag_verbose"] = False
      case "--silent":
        parsed_flags["flag_silent"] = True
      case "--help":
        cli.help()
        sys.exit(0)
      case "--version":
        cli.version()
        sys.exit(0)
      case _:
        cli.echo(f"Unknown flag: '{flag}'. Ignoring.", prefix="wahoo warn", color=wahoo_colors["wahoo_warn"])
    
  # yes, this means that wahoo supports running with --verbose and --silent at the same time
  # verbose technically just shows error details. i will just make it the default.
  # true silence is done by doing the classic `> /dev/null`. running wahoo with --silent won't just magically make all
  # of wahoo's messages disappear.

  return parsed_flags

def parse():
  '''
  parses the command
  '''

  # ARGUMENTS

  flags, positional = find_args()
  parsed_flags = flagparsing(flags)

  cmd = positional[0] if len(positional) >= 1 else "help"
  pkg = positional[1] if len(positional) >= 2 else None
  # TODO: add multi-package support
  #       so that something like "wahoo -S foo1 foo2" is possible

  cmd = cmd if not cmd.startswith("-") else cmd.lower() # i.e, if command is "iNsTaLL" then it will become "install"
  # this ignores "-S" and other pacman-style commands, since the capital letters are intentional there
  # fun fact: this used to be in older versions of the og wahoo, 
  #           but since the match-case would see "-s" and not "-S"
  #           my solution? remove it entirely. yeah past me was kinda 
  #           stupid

  # FLAG ALIASES

  flag_yolo = parsed_flags["flag_yolo"]
  flag_rns = parsed_flags["flag_rns"]
  flag_verb = parsed_flags["flag_verbose"]
  flag_silent = parsed_flags["flag_silent"]

  # PARSING

  match cmd:
    case ("install" | "-S"):
      cli.no_pkg(pkg)
      main.install(pkg, yolo=flag_yolo, verbose=flag_verb, silent=flag_silent)

    case ("uninstall" | "remove" | "-R" | "purge" | "autoremove" | "-Rns"): # apt syntax my beloathed
      if cmd in ["purge", "autoremove", "-Rns"]:
        flag_rns = True
        
      cli.no_pkg(pkg)
      main.uninstall(pkg, yolo=flag_yolo, rns=flag_rns, verbose=flag_verb, silent=flag_silent)

    case ("clean" | "cleanup" | "-Rc" | "-C"): # unsure what the pacman equivalent of this would be
      main.cleanup(yolo=flag_yolo, verbose=flag_verb, silent=flag_silent)

    case ("update" | "-Sy"):
      cli.no_pkg(pkg)
      if pkg == "wahoo":
        try:
          salmon.main()
          sys.exit(0)
        except:
          sys.exit(255)
      
      main.update(pkg, yolo=flag_yolo, silent=flag_silent, verbose=flag_verb)
      
    case ("upgrade" | "updateall" | "-Syu"):
      main.upgrade(yolo=flag_yolo, verbose=flag_verb, silent=flag_silent)

    case ("-Su" | "-U"):
      cli.echo("wahoo is confused", color=None, prefix=None)
      cli.echo("If you meant to update a package, use -Sy.", color=None, prefix=None)
      cli.echo("If you meant to do an upgrade, use -Syu.", color=None, prefix=None)
      sys.exit(2)
    
    case ("version" | "-V"):
      cli.version()

    case ("help" | "-H"):
      cli.help()

    case ("show" | "info" | "-Qi"):
      cli.no_pkg()
      pacwrap.info(pkg, verbose=flag_verb)
    
    case ("list" | "-Qs"):
      pacwrap.list(pkg, verbose=flag_verb)

    case _:
      cli.echo(f"Unknown command: '{cmd}'.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
      cli.help()