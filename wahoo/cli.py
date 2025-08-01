#!/usr/bin/env python3
'''
CLI components.

* echo
* prompt
* no_pkg
'''

# LIBRARIES AND MODULES

import sys

## wahoo stuff

from wahoo.constants import *

# FUNCTIONS

# TODO: possibly add a style() function?
#       if so it will probably extend echo()'s functionality by a bit

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

  if prefix is None:
    used_prefix = ""
  elif prefix == "wahoo!":
    used_prefix = f"{prefix} "
  else:
    used_prefix = f"{prefix}: "
  
  ## echoed = f"{color}{prefix + ':' if prefix and prefix != 'wahoo!' else ''} {reset}{msg}"
  ## echoed = color + used_prefix + reset + msg
  echoed = f"{color if color else ''}{used_prefix}{reset}{msg}"

  if not do_return:
    print(echoed)
    return # ironic isn't it?
    
  return echoed

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
  fullmsg = f"{echo(msg, do_return=True)}{(' ' + promptmsg_used) if use_msg_as_prompt else ('\nProceed? ' + promptmsg_used + reset + ' ')}"

  if not yolo:
    usrinput = input(fullmsg).lower().strip()
    if not usrinput:
      return default

    splitted = usrinput.split()[0] # fat finger prevention >:D
    if splitted == "n": # allows for answers like nn, no, nope, nah, etc
      if show_abort_msg:
        echo("Aborted.", color=None, prefix=None)
        
      if dont_exit:
        return False
      else:
        sys.exit(1)
        
    elif splitted == "y": # allows for answers like yy, yes, yeah, yea, yep, etc
      return True
    else:
      echo(f"Taking '{usrinput}' as {'yes' if default else 'no'}.", "wahoo warn", None)
      return default
  else:
    echo(fullmsg, color=None, prefix=None)
    return default

# TODO: move no_pkg() to parser.py since its only called there
    
def no_pkg(pkg):
  '''
  Helper function.
  No docstring needed.
  '''
    
  if pkg:
    return
    
  echo("No package provided.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
  sys.exit(2)

# TODO: move version_msg() to parser.py since its only called there

def version_msg():
  '''
  does this seriously need a docstring?
  '''
    
  echo(f"{colors['yellow']}v{version}{reset}", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
  # in plain english,
  # it does this:
  ## print(f"wahoo! v{version}")
  echo("Made with <3 by Spark", prefix=None, color=None)
