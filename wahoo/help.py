#!/usr/bin/env python3
'''
TODO: add docstrings
'''

# LIBRARIES AND MODULES

## wahoo stuff

from wahoo.constants import *
import wahoo.cli as cli

# FUNCTIONS

def help(cmd=None):
  '''
  does this seriously need a docstring?
  TODO: make this more DRY
  '''

  # COLORS

  green = colors["green"]
  blue = colors["blue"]
  yellow = colors["yellow"]

  # MAIN MESSAGE

  # unstyled:
  main_msg_dev = """
[Available Commands]
install (-S):               Installs a package from the AUR.
uninstall (remove, -R):     Uninstalls a package on your system.
purge (autoremove, -Rns):   Ditto, but removes orphaned dependencies by default.
clean (cleanup, -Rc, -C):   Cleans up wahoo's source directory.
update (-Sy):               Update an AUR package.
upgrade (updateall, -Syu):  Update all installed AUR packages.
[Other Commands]
These commands wrap around their pacman equivalents.
list (-Q, -Qs)
info (show, -Qi)
[Flags]
--yolo (--noconfirm):       Skips all confirmation prompts.
--dont-remove-depends:      Doesn't remove orphaned dependencies when uninstalling a package.
--no-error-details:         Hides error info. (yeah.)
--silent:                   Silences any commands ran by wahoo.
"""
  # styled:
  main_msg = f"""
{green}[Available Commands]{reset}
{blue}install (-S){reset}:               Installs a package from the AUR.
{blue}uninstall (remove, -R){reset}:     Uninstalls a package on your system.
{blue}purge (autoremove, -Rns){reset}:   Ditto, but removes orphaned dependencies by default.
{blue}clean (cleanup, -Rc, -C){reset}:   Cleans up wahoo's source directory.
{blue}update (-Sy){reset}:               Update an AUR package.
{blue}upgrade (updateall, -Syu){reset}:  Update all installed AUR packages.
{green}[Other Commands]{reset}
{styles["italic"]}{styles["faint"]}These commands wrap around their pacman equivalents.{reset}
{blue}list (-Q, -Qs){reset}
{blue}info (show, -Qi){reset}
{green}[Flags]{reset}
{blue}--yolo {yellow}(--noconfirm){reset}:       Skips all confirmation prompts.
{blue}--dont-remove-depends{reset}:      Doesn't remove orphaned dependencies when uninstalling a package.
{blue}--no-error-details{reset}:         Hides error info. (yeah.)
{blue}--silent{reset}:                   Silences any commands ran by wahoo.
"""
  
  if not cmd:
    print(main_msg)
    sys.exit(0)
  
  match cmd:
    # TODO
    case _:
      cli.echo("This isn't implemented yet, sorry!", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
      print(main_msg)