#!/usr/bin/env python3
'''
wahoo's launcher and the thing that actually gets installed to /usr/bin/ by pacman
'''

import sys
from wahoo.parser import parse as main
from wahoo.cli import echo
from wahoo.constants import *

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    echo("Interrupted by Ctrl+C, see ya next time")
    sys.exit(130)