#!/usr/bin/env python3
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
    sys.exit(130)