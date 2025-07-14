#!/usr/bin/python3

# wahoo! (but more gooder)
# this will be the v0.5 release of wahoo.

# certain lines of code will be commented out with two #s,
# that is an intentional decision, aka me trying to speedrun coding :)
# you can remove those comments if you like, they are just padding at the end of the day

# STYLE GUIDE
# * cli.echo() is used instead of raw print()
# * section headers are in all caps (i.e, "# THIS IS A SECTION HEADER")
# * everything is in snake_case (yes, even the class names. screw capitalization.)
# * this version of wahoo is built modular (not in the sense of python modules) meaning that
#   it should be easier to add new features.
# * do not use emojis anywhere. in strings, in docstrings, in comments, just please don't.
# * feel free to improve the docstrings, just leave the comments alone

# NOTE: do not try to use this script as a python module (i.e, "import wahoo")
#       this is a CLI tool, not a library.
#       if you must use it as a module, then it is recommended to just make it yourself
#       (meaning, copy the code and replace all the CLI related stuff with your own)
#       also this won't work on anything that isn't arch-based. its an AUR helper after all.

# EXIT CODE GUIDE
# 0 = success
# 1 = general error
# 2 = cli error
# 3 = self-update error
# 4 = no internet
# 11 = segfault easter egg
# everything else: i have no idea what happened but it was so catastrophic 
#                  that it exitted with an unidentified exit code

# LIBRARIES AND MODULES

import sys
from pathlib import Path
import subprocess
from os import getuid

## PIP PACKAGES (aka, dependencies.)

import requests
from rapidfuzz import fuzz

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

# CLASSES

class cli:
  '''
  CLI components.

  * find_args
  * echo
  * prompt
  * no_pkg
  * flagparsing
  * help
  * version
  * main
  '''
  
  @staticmethod
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
  
  @staticmethod
  def echo(msg, color=wahoo_colors["wahoo_message"], prefix="wahoo", do_return=False):
    '''
    prints with color (helper function)

    Args:
    * msg (string) - the message to be printed
    * color (string?) - what ANSI escape color should be used on the prefix - default: "wahoo_message" from the wahoo_colors dict
    * prefix (string) - what prefix should be used before the message - default: "wahoo"
    * do_return (bool) - if false, print the message. if true, return it. - default: False
    '''
    # with how many times i call this function with "color=None",
    # its starting to get ironic (yk, given the whole "prints with color" concept)
    # anyway this is just a developer "lol moment"

    echoed = f"{color}{prefix + ':' if prefix and prefix != 'wahoo!' else ''} {reset}{msg}"

    if not do_return:
      print(echoed)
      return # ironic isn't it?
    
    return echoed

  @staticmethod
  def prompt(msg, yolo=False, dont_exit=True, use_msg_as_prompt=False, show_abort_msg=True, default=True, promptmsg="[Y/n]"):
    '''
    prompt helper function

    Flow:
    TODO: add flow

    Args:
    * msg (string) - the prompt message
    * yolo (bool) - yolo mode (skips the prompt) - default: False
    * dont_exit (bool) - if false, will exit if the user chooses to abort (n) - default: True
    * use_msg_as_prompt (bool) - if true, will append the variable promptmsg_used to the message. else, promptmsg_used will be in a new line. - default: False
    * default (bool) - if the user just presses enter without giving an answer, then it will return itself. True is Y, False is N - default: True (y)
    * show_abort_msg (bool) - self explanatory. - default: True
    * promptmsg (string) - the [Y/n] bracket. can be anything! - default: "[Y/n]"
    '''

    promptmsg_used = wahoo_colors["wahoo_yn"] + promptmsg

    if not yolo:
      usrinput = input(f"{cli.echo(msg, color=None, do_return=True)}{(' ' + promptmsg_used) if use_msg_as_prompt else ('\nProceed? ' + promptmsg_used + ' ')}")
      if usrinput.lower().split()[0] == "n": # allows for answers like nn, no, nope, nah, etc
        if show_abort_msg:
          cli.echo("Aborted.", color=None, prefix=None)
        
        if dont_exit:
          return False
        else:
          sys.exit(1)

      elif not usrinput.split():
        return default
      elif usrinput.lower().split()[0] == "y": # allows for answers like yy, yes, yeah, yea, yep, etc
        return True
      else:
        cli.echo(f"Taking '{usrinput}' as {'yes' if default else 'no'}.", "wahoo warn", None)
        return default
    else:
      # TODO: add a cli.echo() that shows what the message was (along with the [Y/n] prompt)
      return default
    
  @staticmethod
  def no_pkg(pkg):
    '''
    Helper function.
    No docstring needed, used in `cli.main()`
    '''
    
    if pkg:
      return
    
    cli.echo("No package provided.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    sys.exit(2)

  @staticmethod
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
  
  @staticmethod
  def help():
    '''
    does this seriously need a docstring?
    '''
    
    # this is the only function where it would be easier to use print() instead of cli.echo()
    # so use print()
    print("no help for u")
    print("help is in next version of the refactor")

  @staticmethod
  def version():
    '''
    does this seriously need a docstring?
    '''
    
    cli.echo(f"{colors["yellow"]}v{version}{reset}", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
    # in plain english,
    # it does this:
    ## print(f"wahoo: v{version}")
    cli.echo("Made with <3 by Spark", prefix=None, color=None)

  @staticmethod
  def main():
    '''
    parses the command
    '''

    # ARGUMENTS

    flags, positional = cli.find_args()
    parsed_flags = cli.flagparsing(flags)

    cmd = positional[0] if len(positional) >= 1 else "help"
    pkg = positional[1] if len(positional) >= 2 else None
    # TODO: add multi-package support
    #       so that something like "wahoo -S foo1 foo2" is possible

    cmd = cmd if not cmd.startswith("-") else cmd.lower() # i.e, if command is "iNsTaLL" then it will become "install"
    # this ignores "-S" and other pacman-style commands, since the capital letters are intentional there

    # fun fact: this used to be in older versions of the og wahoo,
    #           since the match-case would see "-s" and not "-S"
    #           my solution? remove it entirely. yeah past me was kinda stupid

    # FLAG ALIASES

    flag_yolo = parsed_flags["flag_yolo"]
    flag_rns = parsed_flags["flag_rns"]
    flag_verb = parsed_flags["flag_verbose"]
    flag_silent = parsed_flags["flag_silent"]

    # PARSING

    match cmd:
      case ("install" | "-S"):
        cli.no_pkg(pkg)
        install(pkg, yolo=flag_yolo, verbose=flag_verb, silent=flag_silent)

      case ("uninstall" | "remove" | "-R" | "purge" | "autoremove" | "-Rns"): # apt syntax my beloathed
        if cmd in ["purge", "autoremove", "-Rns"]:
          flag_rns = True
        
        cli.no_pkg(pkg)
        uninstall(pkg, yolo=flag_yolo, rns=flag_rns, verbose=flag_verb, silent=flag_silent)

      case ("clean" | "cleanup" | "-Rc" | "-C"): # unsure what the pacman equivalent of this would be
        cleanup(yolo=flag_yolo, verbose=flag_verb, silent=flag_silent)

      case ("update" | "-Sy"):
        update(pkg, yolo=flag_yolo, silent=flag_silent, verbose=flag_verb)
      
      case ("upgrade" | "updateall" | "-Syu"):
        upgrade(yolo=flag_yolo, verbose=flag_verb, silent=flag_silent)

      case ("-Su" | "-U"):
        cli.echo("wahoo is confused", color=None, prefix=None)
        cli.echo("If you meant to update a package, use -Sy.", color=None, prefix=None)
        cli.echo("If you meant to do an upgrade, use -Syu.", color=None, prefix=None)
        sys.exit(2)
    
      case ("version" | "-V"):
        cli.version()

      case ("help" | "-H"):
        cli.help()

      case _:
        cli.echo(f"Unknown command: '{cmd}'.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
        cli.help()

class utils:
  '''
  Reusable helper functions organized into one place.

  * internet_check
  * run
  * sudo_check
  * (unused and empty) ensure_install_sh
  '''

  @staticmethod
  def internet_check(timeout=3, print_and_exit=False):
    '''
    TODO: add docstrings
    '''
    try:
      requests.get("https://archlinux.org", timeout=timeout)
    except requests.RequestException: # meaning no internet
      if print_and_exit:
        cli.echo("No internet, aborting.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
        sys.exit(4)
      
      return False
    
    return True
  
  @staticmethod
  def run(cmd, dir=None, yolo=False, dont_exit=True, verbose=True, silent=False):
    '''
    runs a shell command

    Flow:
    * prompts to run the command
    * runs the command
    * should something go wrong and verbose=True, show error details along with the command being ran

    Args:
    * cmd (string) - the command to be run
    * dir (string) - where to run the command (passed to subprocess.run()'s cwd paramater) - default: None (i.e, current working directory)
    * yolo (bool) - yolo mode - default: False
    * dont_exit (bool) - don't exit if the user 
    '''

    if not yolo:
      if not cli.prompt(f"Running command: {cmd}", yolo=yolo, dont_exit=False): # use_msg_as_prompt is false (using defaults since it wasn't added to the function call) for parity with the original version of wahoo
        if not dont_exit:
          sys.exit(0)
        else:
          return # doesn't need to return anything, just exits the function.
    else:
      if not silent:
        cli.echo(f"Running command: {cmd}", color=None, prefix=None)
    try:
      subprocess.run(cmd + (" > /dev/null 2>&1" if silent else ""), shell=True, check=True, cwd=dir)
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
  def sudo_check(): # wahoo is flexible now, some commands support running as root, some don't.
    '''
    check if wahoo is being run as root
    '''

    if getuid() == 0:
      cli.echo("Please do not run this command as root.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
      sys.exit(2)
  
  @staticmethod
  def ensure_install_sh():
    '''
    vestigial? structure from the old version of wahoo
    i say vestigial with a ? because i am not sure how to implement
    the self-updating feature without outsourcing it to a separate script
    and tbh using bash for that install script is just kinda dumb
    it would be easier to just use python for everything

    PROPOSED SOLUTION:
    1. install.sh stays and can still be used to update wahoo, however it will not be used by wahoo itself. (neither the old version nor this one)
    2. two scripts are added to PATH when wahoo is installed:
      - wahoo (this one)
      - salmon (the self-updater, wahoo requires this for self-updating and if it is removed then you'll be stuck with the version of wahoo you already have, which could potentially be buggy)
    '''

    pass

class pacwrap:
  '''
  wahoo's not a pacman wrapper per se,
  it's just here because i believe in good UX.

  essentially, just helper functions.
  '''

  @staticmethod
  def list(pkg, verbose=False): # no point in adding --silent support
    if not pkg:
      utils.run("pacman -Q", yolo=True, verbose=verbose)
      sys.exit(0)
    
    utils.run(f"pacman -Qs {pkg}", yolo=True, verbose=verbose)

  @staticmethod
  def info(pkg, verbose=False):
    utils.run(f"pacman -Qi {pkg}", yolo=True, verbose=verbose)

# FUNCTIONS

def install(pkg, source="https://aur.archlinux.org", yolo=False, build=True, segfault=True, silent=False, verbose=False):
  '''
  installs a package from the AUR

  Flow:
  * segfault easter egg (if enabled)
  * sudo check
  * internet check
  * prompts to start the cloning
  * prompts to build and install (or build without installing) the package (if build=True)
  * fin

  Args:
  * pkg (string) - the package to be installed
  * source (string) - where to clone the package from - default: "https://aur.archlinux.org"
  * yolo (bool) - yolo mode - default: False
  * build (bool) - enable building - default: True
  * segfault (bool) - segfault easter egg >:) - default: True
  * silent (bool) - silences git and makepkg - default: False
  * verbose (bool) - prints error info should something go wrong - default: False
  '''

  if segfault and pkg == "wahoo":
    # muahahahahahaha
    cli.echo("Bold of you to try to install wahoo with wahoo.", color=None, prefix=None)
    cli.echo("Segmentation fault (core dumped)", color=None, prefix=None)
    sys.exit(11) # SIGSEGV
  
  utils.sudo_check()
  utils.internet_check(print_and_exit=True)

  wahooroot = Path.home() / ".wahoo" / "source"
  wahooroot.mkdir(parents=True, exist_ok=True)
  sourcedir = wahooroot / pkg

  try:
    cli.prompt("Starting install...", yolo=yolo, dont_exit=False)
    cli.echo(f"Installing {pkg}" + f" from {source}" if source != "https://aur.archlinux.org" else "...")
    if not sourcedir.exists():
      if verbose:
        cli.echo(f"Cloning {pkg} git repo ({source}/{pkg}.git) to {sourcedir}")

      utils.run(f"git clone {source}/{pkg}.git", dir=wahooroot, yolo=yolo, dont_exit=False, silent=silent)
    else:
      cli.echo(f"Source directory for {pkg} already exists, skipping clone.", color=wahoo_colors["wahoo_warn"], prefix="wahoo warn")

    # TODO: add dependency resolution for packages that aren't available in the pacman repos
    # context: i tested out the old version again, tried to install osu-lazer-tachyon-bin (for funsies)
    #          then when the build started, makepkg freaked out about not being able to find
    #          `osu-mime`. turns out osu-mime is an AUR package which couldn't be installed with pacman.

    if build:
      if yolo:
        # assume the user wants to build and install the package (-si)
        cli.echo("Building and installing package...")
        utils.run("makepkg -si --noconfirm", dir=sourcedir, yolo=yolo, dont_exit=True, silent=silent, verbose=verbose)
        cli.echo(f"Successfully installed {pkg}!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
        return
      
      if cli.prompt(f"Build {pkg} without installing?", use_msg_as_prompt=True, default=False, promptmsg="[y/N]", show_abort_msg=False):
        cli.echo("Building package...")
        utils.run("makepkg -s", dir=sourcedir, silent=silent, verbose=verbose)
        cli.echo(f"{pkg} built successfully!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
        sys.exit(0)
        
      cli.echo("Building and installing package...")
      utils.run("makepkg -si", dir=sourcedir, silent=silent, verbose=verbose)
  except Exception as e:
    cli.echo(f"Installation failed.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    if verbose:
      cli.echo(f"Details: {e}", color=None, prefix=None)
    
    sys.exit(1)

def uninstall(pkg, yolo=False, silent=False, verbose=False, rns=False):
  '''
  Uninstalls a package with pacman.
  This means that if a package was installed with any other AUR helper, it can also be uninstalled.

  Flow:
  * prompt to start the uninstall
  * gives a little heads up if you ran with rns=false
  * prompt to start the clean up
  * fin

  Args:
  * pkg (string) - the package to be uninstalled
  * yolo (bool) - yolo mode - default: False
  * silent (bool) - silences pacman and rm - default: False
  * verbose (bool) - prints error info should something go wrong - default: False
  * rns (bool) - removes orphaned dependencies - default: False
  '''

  # no need for a sudo check here, pacman will require sudo anyway
  # also no need for an internet check, since pacman isn't installing anything

  sourcedir = Path.home() / ".wahoo" / "source" / pkg

  cli.prompt(f"Uninstall {pkg}?", yolo=yolo, dont_exit=False, use_msg_as_prompt=True)
  utils.run(f"sudo pacman {'-Rns' if rns else '-R'} {'--noconfirm' if yolo else ''} {pkg}", silent=silent, verbose=verbose)
  cli.echo(f"{pkg} uninstalled successfully!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
  if not rns and not yolo and not silent: # woah thats a lot of conditions
    cli.echo("Heads up, you may have some orphaned dependencies left over.", prefix="wahoo warn", color=wahoo_colors["wahoo_warn"])
    cli.echo("You can remove them with `sudo pacman -Rns $(pacman -Qdtq)`.", prefix=None, color=None)
  
  cli.prompt("Starting cleanup...", yolo=yolo, dont_exit=False)
  utils.run(f"rm -rf {sourcedir}", yolo=yolo, verbose=verbose, silent=silent)
  cli.echo("Cleanup finished!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")

def update(pkg, yolo=False, silent=False, verbose=False):
  '''
  Updates a package installed with wahoo.
  NOTE: wahoo can't update any packages installed with other AUR helpers, such as yay or paru.

  Flow:
  * internet check
  * sudo check
  * checks if the package's source directory exists
  * prompt to start the update
  * fin

  Args:
  * pkg (string) - the package to be updated
  * yolo (bool) - yolo mode - default: False
  * silent (bool) - silences the update process (and pacman) - default: False
  * verbose (bool) - prints error info should something go wrong - default: False
  '''

  utils.internet_check(print_and_exit=True)
  utils.sudo_check()

  sourcedir = Path.home() / ".wahoo" / "source" / pkg
  if not sourcedir.exists():
    cli.echo(f"No source directory found for {pkg}.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    cli.echo("If it was installed with pacman, try updating it with pacman instead.", color=None, prefix=None)
    cli.echo("Otherwise, it may have been cleaned up. Try uninstalling it with pacman, then reinstalling it with wahoo.", color=None, prefix=None)
    cli.echo("This will reinstall the latest version of the package from the AUR.", color=None, prefix=None)

  cli.prompt("Starting update...", yolo=yolo, dont_exit=False)
  cli.echo(f"Updating {pkg}...")
  try:
    utils.run("git reset --hard HEAD", dir=sourcedir, yolo=yolo, dont_exit=False, silent=silent, verbose=verbose)
    utils.run("git pull", dir=sourcedir, yolo=yolo, dont_exit=False, silent=silent, verbose=verbose)
    cli.echo(f"{pkg} updated successfully!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
  except subprocess.CalledProcessError as e:
    cli.echo(f"Update failed.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    if verbose:
      cli.echo(f"Details: {e}", color=None, prefix=None)
    
    sys.exit(1)

def upgrade(yolo=False, verbose=False, silent=False):
  '''
  Updates all packages installed with wahoo.
  NOTE: wahoo can't update any packages installed with other AUR helpers, such as yay or paru.

  Flow:
  * internet check
  * sudo check
  * prompt to start the upgrade
  * prompt to update the system with pacman -Syu
  * fin

  Args:
  * yolo (bool) - yolo mode - default: False
  * verbose (bool) - prints error info should something go wrong - default: False
  * silent (bool) - silences the update process (and pacman) - default: False
  '''

  wahooroot = Path.home() / ".wahoo" / "source"
  
  utils.internet_check(print_and_exit=True)
  utils.sudo_check()

  cli.prompt("Starting upgrade...", yolo=yolo, dont_exit=False)
  cli.echo("Updating all packages...")
  cli.echo("This will not update wahoo itself. (self-updating for wahoo refactored has not been implemented yet)")
  # TODO: add self-updating

  try:
    for pkg in wahooroot.iterdir():
      if pkg.is_dir() and pkg.name != "wahoo": # don't update wahoo itself here
        pkgname = pkg.name # helpful alias
        cli.echo(f"Updating {pkgname}...")
        update(pkgname, yolo=True, verbose=verbose, silent=silent)

  except Exception as e:
    cli.echo("Upgrade failed.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    if verbose:
      cli.echo(f"Details: {e}", color=None, prefix=None)

    sys.exit(1)
  
  if cli.prompt("Would you like to do a system update with pacman as well?", default=False, promptmsg="[y/N]"):
    utils.run("sudo pacman -Syu --noconfirm", yolo=True, verbose=verbose, silent=silent)
  
  cli.echo(f"Upgrade finished!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")

def search(query, limit=20, use_fuzz=True, timeout=3, exit_on_fail=False, verbose=False):
  '''
  Searches for a package from the AUR.

  Flow:
  * internet check
  * sends a get request to the AUR RPC API (wow thats a mouthful)
  * raises an HTTPError for bad responses (4xx and 5xx)
  * converts the response to JSON
  * gets the results from the JSON and exits or returns (depending on exit_on_fail) if no results were found
  * sorts the results with rapidfuzz (if use_fuzz=True)
  * caps the results to limit
  * prints the results
  * fin

  Args:
  * query (string) - what to search for
  * limit (int) - maximum no. results should be shown - default: 20
  * use_fuzz (bool) - toggle to use rapidfuzz's string matching - default: True
  * timeout (int) - timeout for the get request to the AUR - default: 3
  * exit_on_fail (bool) - toggle to exit if no results are found - default: False
  * verbose (bool) - prints error info should something go wrong - default: False
  '''

  utils.internet_check(print_and_exit=True)

  url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={query}"

  # NOTE: pagination will not be implemented (for now)
  #       expect it to either not *ever* be implemented or implemented in a future version

  try:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])
    if not results:
      cli.echo(f"No results found for '{query}'.", color=wahoo_colors["wahoo_warn"], prefix="wahoo warn") # i should probably make this a wahoo error instead, but since its non-fatal im not sure what to do here
      cli.echo(f"Try searching for {query} with pacman instead.", color=None, prefix=None)
      if exit_on_fail:
        sys.exit(1)
      else:
        return
    
    if use_fuzz:
      results.sort(key=lambda entry: fuzz.WRatio(query, entry.get("Name", "unknown")), reverse=True)

    shown = results[:limit]

    if len(results) > limit:
      cli.echo(f"Found {colors['blue']}{len(results)}{reset} results for '{query}', showing the first {limit} results.", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
    elif len(results) == 1:
      cli.echo(f"Found {colors['blue']}1{reset} result for '{query}'.", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
    else:
      cli.echo(f"Found {colors['blue']}{len(results)}{reset} results for '{query}'.", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
    
    for entry in shown:
      name = entry.get("Name", "unknown")
      desc = entry.get("Description", "no description")
      votes = entry.get("NumVotes", "???")
      cli.echo(f" - {colors['green']}{name} {reset}({colors['yellow']}{votes} {reset} votes): {desc}", color=None, prefix=None) # "color=None" how ironic
      # in plain english,
      # it does this:
      ## cli.echo(f" - {name} ({votes} votes): {desc}", color=None, prefix=None)
      # which would give you this output:
      ##  - foo (100 votes): this is where she writes a description

  except Exception as e:
    cli.echo("Search failed.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    if verbose:
      cli.echo(f"Details: {e}", color=None, prefix=None)

    sys.exit(1)

def cleanup(yolo=False, verbose=True, silent=True):
  wahooroot = Path.home() / ".wahoo" / "source"

  cli.echo("Cleaning up wahoo's source directory will make it impossible to update a package with wahoo.", color=wahoo_colors["wahoo_warn"], prefix="wahoo warn")
  cli.prompt("Are you sure?", dont_exit=False, use_msg_as_prompt=True)

  cli.echo("Cleaning up everything...")
  try:
    utils.run(f"rm -rf {wahooroot}/*", yolo=yolo, verbose=verbose, silent=silent)
    # would it be better to use rmdir instead of rm -rf?
    # eh... im not sure.
    # it should delete everything INSIDE the source dir, not nuke it completely.
    cli.echo("Clean up finished!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
  except Exception as e:
    cli.echo("Clean up failed.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    if verbose:
      cli.echo(f"Details: {e}", color=None, prefix=None)

# INIT

if __name__ == "__main__":
  try:
    cli.echo("You are using an outdated and soon to be deprecated version of wahoo.")
    cli.prompt("Are you sure you want to continue?", dont_exit=False, use_msg_as_prompt=True, default=False, promptmsg="[y/N]")
    cli.main()
  except KeyboardInterrupt:
    cli.echo("Interrupted by Ctrl+C, see ya next time")
    ## sys.exit(130)
    # HACK: 130 is the exit code for Ctrl+C, but i dont want to use it since
    #       the "KeyboardInterrupt" exception has already been handled,
    #       so i see no need to exit the script with a non-zero exit code.
    #       naturally, this doesn't play well with scripts that use wahoo since
    #       they expect a non-zero exit code if wahoo is interrupted.
    #       no way to get around this im afraid

# OH MY GOD THE REWRITE OF WAHOO IS LONGER THAN THE ORIGINAL
# WHAT HAVE I GOTTEN MYSELF INTO