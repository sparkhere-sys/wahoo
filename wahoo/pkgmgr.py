#!/usr/bin/env python3
'''
The actual package manager.

* install
* uninstall
* update
* upgrade
* search
* cleanup
'''

# LIBRARIES AND MODULES

import sys
from pathlib import Path
from shutil import rmtree

## wahoo stuff

import wahoo.cli as cli
import wahoo.utils as utils
from wahoo.constants import *
from wahoo.installer import installer

## pip packages

import requests
from rapidfuzz import fuzz

# FUNCTIONS

def install(**kwargs):
  '''
  was it a good idea to use **kwargs and NOT document the available args in the same file?
  probably not.
  did i do it anyway because vibe coding is a human right?
  heck yeah.
  '''

  install_class = installer(**kwargs)

  install_class.main()

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

  sourcedir = wahooroot / pkg

  # TODO: use pyalpm for this

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

  sourcedir = wahooroot / pkg
  if not sourcedir.exists():
    cli.echo(f"No source directory found for {pkg}.", color=wahoo_colors["wahoo_error"], prefix="wahoo warn")

  ## cli.prompt("Starting update...", yolo=yolo, dont_exit=False)
  cli.prompt(f"Updating {pkg}...", yolo=yolo, dont_exit=False)
  try:
    if sourcedir.exists():
      cli.echo("Pulling from latest source...")
      utils.run("git reset --hard HEAD", dir=sourcedir, yolo=True, silent=silent, verbose=verbose)
      utils.run("git pull", dir=sourcedir, yolo=True, dont_exit=False, silent=silent, verbose=verbose)
    
    cli.echo("Uninstalling old package...")
    uninstall(pkg, yolo=True)
    cli.echo("Reinstalling package...")
    if sourcedir.exists():
      utils.run("makepkg -si", dir=sourcedir, yolo=True, silent=silent, verbose=verbose)
    else:
      install(pkg)

    cli.echo(f"{pkg} updated successfully!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
  except Exception as e:
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
  
  utils.internet_check(print_and_exit=True)
  utils.sudo_check()

  cli.prompt("Starting upgrade...", yolo=yolo, dont_exit=False)
  cli.echo("Updating all packages...")
  cli.echo("This will not update wahoo itself, use 'wahoo -Sy wahoo' for that.")

  try:
    for pkg in wahooroot.iterdir():
      # HACK: there is not going to be a ~/.wahoo/source/wahoo directory
      #       i assume that `pkg.name != "wahoo"` is a vestigial structure from
      #       the old version of wahoo, which used the now deprecated install.sh

      if pkg.is_dir() and pkg.name != "wahoo": # don't update wahoo itself here
        ## pkgname = pkg.name # helpful alias
        # shadows pkgname from constants.py
        cli.echo(f"Updating {pkg.name}...")
        update(pkg.name, yolo=True, verbose=verbose, silent=silent)

  except Exception as e:
    cli.echo("Upgrade failed.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    if verbose:
      cli.echo(f"Details: {e}", color=None, prefix=None)

    sys.exit(1)
  
  cli.echo(f"Upgrade finished!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")

  if cli.prompt("Would you like to do a system update with pacman as well?", default=False, promptmsg="[y/N]"):
    utils.run("sudo pacman -Syu --noconfirm", yolo=True, verbose=verbose, silent=silent)

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

    if limit:
      shown = results[:limit]
    else:
      shown = results

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

def cleanup(yolo=False, verbose=True):
  ## wahooroot = Path.home() / ".wahoo" / "source"

  ## cli.echo("Cleaning up wahoo's source directory will make it impossible to update a package with wahoo.", color=wahoo_colors["wahoo_warn"], prefix="wahoo warn")
  cli.prompt("Clean up wahoo's source directory?", yolo=yolo, dont_exit=False, use_msg_as_prompt=True)

  cli.echo("Cleaning up everything...")
  try:
    ## utils.run(f"rm -rf {wahooroot}/*", yolo=yolo, verbose=verbose, silent=silent)
    rmtree(wahooroot)
    
    cli.echo("Clean up finished!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
  except Exception as e:
    cli.echo("Clean up failed.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    if verbose:
      cli.echo(f"Details: {e}", color=None, prefix=None)
