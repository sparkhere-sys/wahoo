#!/usr/bin/python3
## intended to be used as a binary

# wahoo!
## v0.0.2
## made with <3 by spark

# LIBRARIES AND MODULES

import sys
from pathlib import Path
import subprocess
import os

# VARIABLES
## for source, i plan on allowing people to change the source in later versions, but for now it remains here
source = "https://aur.archlinux.org" 

# FUNCTIONS

def run(cmd, dir=None, yolo=False):
  if dir:
    os.chdir(dir)
  
  print(f"wahoo: Running {cmd}")
  if not yolo:
    prompt = input("Proceed? [Y/n] ").strip().lower()
    if prompt.lower() == "n":
      print("Aborted.")
      return

  try:
    subprocess.run(cmd, shell=True, check=True)
  except subprocess.CalledProcessError:
    # if cmd.split()[0] == "git":
    if cmd.startswith("git"):
      print("wahoo error: Failed to clone package. Are you sure it exists in the AUR?")
    # elif cmd.split()[0] == "makepkg":
    elif cmd.startswith("makepkg"):
      print("wahoo error: Failed to build package. Is there an error in the PKGBUILD?")
    # elif cmd.split()[1] == "pacman" and cmd.split()[2] != "-Rns":
    elif "pacman" in cmd and "-Rns" not in cmd:
      print("wahoo error: pacman failed to install package.")
    elif "pacman" in cmd:
      print("wahoo error: pacman failed to uninstall package. Are you sure it exists on your system?")
    else:
      print("wahoo error: Command failed.")
    sys.exit(1)

def install(pkg):
  wahooroot = Path.home() / ".wahoo" / "source"
  wahooroot.mkdir(parents=True, exist_ok=True)

  sourcedir = wahooroot / pkg

  if not sourcedir.exists():
    # while there IS a confirm prompt, yolo mode is enabled when using run()
    prompt = input(f"wahoo: Proceed with installing {pkg}? [Y/n] ")
    if prompt.lower() == "n":
      print("Aborted.")
      return

    print("wahoo: Starting install")
    print(f"wahoo: Downloading {pkg} from AUR...")
    # os.chdir(wahooroot)
    # subprocess.run(f"git clone {source}/{pkg}.git", shell=True, check=True)
    run(f"git clone {source}/{pkg}.git", wahooroot, True)
    print(f"wahoo: {pkg} Downloaded.")

  else:
    print(f"wahoo: {pkg} source already exists at {sourcedir}.")
    
  print(f"wahoo: Trying to install {pkg}...")
  prompt = input("Run 'makepkg' with '-si'? [Y/n]")
  if prompt.lower() == "n":
    run("makepkg", sourcedir, True)
  else:
    run("makepkg -si", sourcedir, True)
  ## os.chdir(sourcedir) # moves to where git cloned the repo from the aur
  ## subprocess.run("makepkg -si", shell=True, check=True) # then builds the package
  print(f"wahoo! {pkg} installed.")

def uninstall(pkg):
  print(f"wahoo: Running 'sudo pacman -Rns {pkg}'...")
  run(f"sudo pacman -Rns {pkg} --noconfirm", None, False)
  # subprocess.run(f"sudo pacman -Rns {pkg} --noconfirm", shell=True, check=True)
  print(f"wahoo! {pkg} uninstalled.")

def help():
  print("[Available commands]")
  print("I'm STILL not typing this help command.")

def flagparsing():
  print("Empty for now...")

def main():
  if len(sys.argv) < 2:
    help()
    sys.exit(1)

  cmd = sys.argv[1]
  pkg = sys.argv[2] if len(sys.argv) > 2 else None

  match cmd:
    case ("install" | "-S"):
      if not pkg:
        print("wahoo: No package or invalid package specified. Are you sure that's a real package?")
        sys.exit(1)
      install(pkg)  
    case ("remove" | "uninstall" | "-R" | "-Rns"):
      uninstall(pkg)
    case ("help" | "-H"):
      help()
      sys.exit(1)
    case ("moo"):
      print("wahoo: This is NOT archapt, brother")
    case ("version" | "--version"):
      print("wahoo - v0.0.2")
      print("made with <3 by spark :D")
    case _:
      print("wahoo: Invalid command.")
      help()
      sys.exit(1)

# MAIN

if __name__ == "__main__":
  try:
    main() # this doesn't run main if wahoo is imported as a module
  except KeyboardInterrupt:
    print("wahoo: Interrupted by Ctrl+C, see you next time")
