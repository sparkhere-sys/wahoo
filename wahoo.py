#!/usr/bin/env python3
'''
wahoo's launcher and the thing that actually gets installed to /usr/bin/ by pacman
'''

import sys
from wahoo.parser import parse as main # wow that's a mouthful
from wahoo.cli import echo
from wahoo.constants import *

if __name__ == "__main__": # you know, just in case
  try:
    main()
  except KeyboardInterrupt:
    echo("Interrupted by Ctrl+C, see ya next time")
    sys.exit(130)
    # i debated on making wahoo exit with a non-zero exit code on KeyboardInterrupt
    # but since wahoo is something i want people to take even a little bit seriously,
    # i had to obey unix conventions and make wahoo exit with 130.