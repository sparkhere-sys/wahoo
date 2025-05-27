#!/usr/bin/python3
## intended to be used as a binary

# wahoo!
## v0.0.1
## made with <3 by spark

# LIBRARIES AND MODULES

import sys
from pathlib import Path
import subprocess
import os

# VARIABLES
## none of these are constants, i just have a habit of defining variables globally even though they're only used locally lol
## as for source, i plan on allowing people to change the source in later versions
prompt = "null"
sourcedir = "null"
source = "https://aur.archlinux.org/" 

# FUNCTIONS

def run(cmd):
  print(f"wahoo: Running {cmd}")
  # if cmd !=
  prompt = input("Proceed? [Y/n] ").strip().lower()
  if prompt.lower() == "n":
    print("Aborted.")
    return

  try:
    subprocess.run(cmd, shell=True, check=True)
  except subprocess.CalledProcessError:
    print("wahoo: Command failed.")

def install(pkg):
  wahooroot = Path.home() / ".wahoo" / "source"
  wahooroot.mkdir(parents=True, exist_ok=True)

  sourcedir = wahooroot / pkg

  if not sourcedir.exists():
    # the lines below are commented out since you already have a y/n prompt in run()
    ## confirm = input(f"wahoo: Proceed with installing {pkg}? [Y/n] ")
    ## if confirm.lower() == "n":
    ##  print("Aborted.")
    ##  return

    print("wahoo: Starting install")
    print(f"wahoo: Downloading {pkg} from AUR...")
    os.chdir(wahooroot) # cd to ~/.wahoo/source/
    subprocess.run(f"git clone {source}/{pkg}.git", shell=True, check=True) # verbose because it doesn't run in the background. is it possible?

  else:
    print(f"wahoo: {pkg} source already exists at {sourcedir}.")

  print(f"wahoo: {pkg} Downloaded.")
  print(f"wahoo: Trying to install {pkg}...")
  os.chdir(sourcedir) # moves to where git cloned the repo from the aur
  subprocess.run("makepkg -si", shell=True, check=True) # then builds the package
  print(f"wahoo! {pkg} installled.")

def uninstall(pkg):
  print(f"wahoo: Running 'sudo pacman -Rns {pkg} --noconfirm'...")
  subprocess.run(f"sudo pacman -Rns {pkg} --noconfirm", shell=True, check=True)
  print(f"wahoo! {pkg} uninstalled.")

def help():
  print("help coming in v0.0.2, im too lazy to type it, sorry.")
def main():
  if len(sys.argv) < 3:
    help()
    sys.exit(1)

  cmd = sys.argv[1]
  pkg = sys.argv[2]

  match cmd:
    case ("install" | "-S"):
      install(pkg)
    case ("remove" | "uninstall" | "-R" | "-Rns"):
      uninstall(pkg)
    case _:
      print("wahoo: Invalid command.")
      help()
      sys.exit(1)

# the last part (i have no clue how to name this)

if __name__ == "__main__":
  main() # this doesn't run main if wahoo is imported as a module
