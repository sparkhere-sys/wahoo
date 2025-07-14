#!/usr/bin/env python3
'''
CLI components.

* find_args
* echo
* prompt
* no_pkg
* help
* version
'''

# LIBRARIES AND MODULES

import sys

## wahoo stuff

from wahoo.constants import *

# CLASSES

# FIXME: everything is inside a class!
#        for usability's sake, all the functions
#        inside the cli class will be moved outside
#        of the class

class cli:
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
    fullmsg = f"{cli.echo(msg, do_return=True)}{(' ' + promptmsg_used) if use_msg_as_prompt else ('\nProceed? ' + promptmsg_used + reset + ' ')}"

    if not yolo:
      usrinput = input(fullmsg)
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
      cli.echo(fullmsg, color=None, prefix=None)
      return default
    
  @staticmethod
  def no_pkg(pkg):
    '''
    Helper function.
    No docstring needed.
    '''
    
    if pkg:
      return
    
    cli.echo("No package provided.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
    sys.exit(2)
  
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
    
    cli.echo(f"{colors['yellow']}v{version}{reset}", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
    # in plain english,
    # it does this:
    ## print(f"wahoo: v{version}")
    cli.echo("Made with <3 by Spark", prefix=None, color=None)
