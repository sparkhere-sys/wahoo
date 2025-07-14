#!/usr/bin/env python3
'''
wahoo's self-updating utility :)

yes, salmon is named after the fish
no, wahoo isn't named after the fish.

this is very barebones...
if you'd like to expand it then feel free!
'''

# LIBRARIES AND MODULES

import tempfile
import sys
from pathlib import Path

## wahoo stuff

from wahoo.constants import *
import wahoo.cliutils as cli
import wahoo.reusables as utils

# CLASSES

# do i add success messages in these steps?
# im honestly not sure.
# i'd like to know what the people think about this
# so maybe open up an issue if you're reading this!

class steps:
  @staticmethod
  def uninstall_wahoo():
    cli.echo("Removing old wahoo installation...", prefix=sal_prefix)
    utils.run(f"sudo pacman -R {pkgname}") # notice that it doesn't run with -Rns

  @staticmethod
  def clone_wahoo(temp_dir):
    cli.echo("Cloning wahoo...", prefix=sal_prefix)
    utils.run(f"git clone {repo_url}", dir=temp_dir)
  
  @staticmethod
  def reinstall_wahoo(temp_dir):
    cli.echo("Reinstalling wahoo...", prefix=sal_prefix)
    utils.run("makepkg -si", dir=temp_dir)

# FUNCTIONS

def update():
  cli.echo("Starting update...", prefix=sal_prefix)

  with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)

    steps.uninstall_wahoo()
    steps.clone_wahoo(tmp_path)
    steps.reinstall_wahoo(tmp_path)
  
  cli.echo("Update completed!", prefix=sal_prefix)

def main():
  try:
    update()
  except Exception as e:
    cli.echo("Something went wrong.", color=wahoo_colors["wahoo_error"], prefix=f"{sal_prefix} error")
    cli.echo("You may have a broken wahoo install.", color=None, prefix=None)
    sys.exit(3)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    cli.echo("what have you done.", color=None, prefix=None)
    sys.exit(255) # you deserve it at this point