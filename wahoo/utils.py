#!/usr/bin/env python3
'''
Reusable helper functions organized into one place.

* internet_check
* run
* sudo_check
'''

# LIBRARIES AND MODULES

import sys
import subprocess
from os import getuid

## wahoo stuff

from wahoo.constants import *
import wahoo.cli as cli

## pip packages

import requests

# FUNCTIONS


def internet_check(timeout=3, print_and_exit=False, request_to="https://archlinux.org"):
  '''
  Checks for internet by sending a GET request to a website.

  Args:
  * timeout (int) - passed to requests.get() - default: 3
  * print_and_exit (bool) - prints a no internet message and exits with code 4 if true - default: False
  * request_to (string?) - the server to send the GET request to - default: https://archlinux.org
  '''

  try:
    requests.get(request_to, timeout=timeout)
  except requests.RequestException: # meaning no internet
    if print_and_exit:
      cli.echo("No internet, aborting.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
      sys.exit(4)
      
    return False
    
  return True

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
  * dont_exit (bool) - don't exit if the user aborts - default: True
  * verbose (bool) - prints error info should something go wrong - default: True
  * 
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
    # TODO: add a log file

    # yes, this runs with shell=True.
    # no, i don't care.
    # we're arch users, what do you expect?

    silent_stdout = subprocess.DEVNULL if silent else None
    ## silent_stderr = silent_stdout

    subprocess.run(cmd, shell=True, check=True, cwd=dir, stdout=silent_stdout) ## stderr=silent_stderr
    return # doesn't need to return anything, just exits the function.
    
  except subprocess.CalledProcessError as e:
    # i refuse to just recycle the error handling from the old version of wahoo,
    # that was a mess.
    # TODO: make better error handling
    cli.echo(f"Command failed.", prefix="wahoo error", color=None)
    if verbose:
      cli.echo(f"Command: {cmd}", color=None, prefix=None)
      cli.echo(f"Details: {e}", color=None, prefix=None)
  
def sudo_check(): # wahoo is flexible now, some commands support running as root, some don't.
  '''
  check if wahoo is being run as root
  '''

  if getuid() == 0:
    cli.echo("Please do not run this command as root.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    sys.exit(2)