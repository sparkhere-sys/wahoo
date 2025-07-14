#!/usr/bin/env python3

# LIBRARIES AND MODULES

import sys
from pathlib import Path

## wahoo stuff

import wahoo.cliutils as cli
import wahoo.reusables as utils
from wahoo.constants import *

## pip packages

import requests
from rapidfuzz import fuzz

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