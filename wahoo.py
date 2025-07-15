#!/usr/bin/python3
'''
wahoo's launcher and the thing that actually gets installed to /usr/bin/ by pacman
'''

from wahoo.parser import parse # as main
import wahoo.cli as cli
from wahoo.constants import *

if __name__ == "__main__":
  try:
    ## main()
    parse()
  except KeyboardInterrupt:
    cli.echo("Interrupted by Ctrl+C, see ya next time")
    ## sys.exit(130)
    # HACK: 130 is the exit code for Ctrl+C, but i dont want to use it since
    #       the "KeyboardInterrupt" exception has already been handled,
    #       so i see no need to exit the script with a non-zero exit code.
    #       naturally, this doesn't play well with scripts that use wahoo since
    #       they expect a non-zero exit code if wahoo is interrupted.
    #       no way to get around this im afraid
