#!/usr/bin/python3

## wahoo!
## v0.3 beta
## made with <3 by spark
## certain lines of code will be commented out with ##. thats an intentional decision, aka me being too lazy to hold down the backspace key.
## docstrings in v0.4 :)

# LIBRARIES AND MODULES

import sys
from pathlib import Path
import subprocess
import os
import requests # new dependency

# FUNCTIONS
def internet_check():
  try:
    requests.get("https://google.com", timeout=3) # it used to ping example.com funny enough
    return True
  except requests.RequestException: # which usually means no internet
    return False
  
def run(cmd, dir=None, yolo=False, exit=False):
  print(f"wahoo: Running {cmd}")
  if not yolo:
    prompt = input("Proceed? [Y/n] ").strip().lower()
    if prompt == "n":
      print("Aborted.")
      if exit:
        return
      else:
        sys.exit(0)

  try:
    subprocess.run(cmd, shell=True, check=True, cwd=dir)
  except subprocess.CalledProcessError:
    # here comes the error handling. this took a while to write but it was worth it
    ## if cmd.split()[0] == "git":
    if cmd.startswith("git"):
      print("wahoo error: Failed to clone package. Are you sure it exists in the AUR?")
    ## elif cmd.split()[0] == "makepkg":
    elif cmd.startswith("makepkg"):
      print("wahoo error: Failed to build package. Is there an error in the PKGBUILD?")
    ## elif cmd.split()[1] == "pacman" and cmd.split()[2] != "-Rns":
    elif "pacman" in cmd and "-Rns" not in cmd:
      print("wahoo error: pacman failed to install package.")
    elif "pacman" in cmd:
      print("wahoo error: pacman failed to uninstall package. Are you sure it exists on your system?")
    else:
      print("wahoo error: Command failed.")
    sys.exit(1)

def install(pkg, source="https://aur.archlinux.org", build=True):
  if not internet_check():
    print("wahoo error: No internet. Aborting install...")
    sys.exit(1)
  wahooroot = Path.home() / ".wahoo" / "source"
  wahooroot.mkdir(parents=True, exist_ok=True)

  sourcedir = wahooroot / pkg

  if not sourcedir.exists():
    # old comment: "while there IS a confirm prompt, yolo mode is enabled when using run()" well that was a lie.

    print("wahoo: Starting install")
    if source == "https://aur.archlinux.org":
      print(f"wahoo: Downloading {pkg} from AUR...")
    else:
      print(f"wahoo: Downloading {pkg}...")
      
    run(f"git clone {source}/{pkg}.git", wahooroot, False)
    print(f"wahoo! {pkg} Downloaded.")

  else:
    print(f"wahoo warn: {pkg} source already exists at {sourcedir}.")

  if build:
    print(f"wahoo: Trying to install {pkg}...")
    prompt = input("Build package without installing? [y/N]").strip().lower()
    if prompt == "y":
      print("wahoo: Building...")
      run("makepkg -s --noconfirm", sourcedir, True) # -s is used to install missing dependencies
    else:
      print("wahoo: Building and installing...")
      run("makepkg -si --noconfirm", sourcedir, True) # -si both installs missing dependencies and the built package
    
    print(f"wahoo! {pkg} installed.")

def ensure_install_sh():
  wahooroot = Path.home() / ".wahoo" / "source" / "wahoo"
  install_sh = wahooroot / "install.sh"

  if not install_sh.exists():
    print("wahoo warn: install.sh does not exist in the wahoo directory. Downloading...")
    install("wahoo", "https://github.com/sparkhere-sys/", False) # since this uses install() and that chekcks for internet when its called, i don't need to add an internet check in ensure_install_sh()
    print("wahoo! Latest update fetched, and install.sh has been downloaded.")
    print("wahoo: Making install.sh executable...")
    run("chmod +x install.sh", wahooroot)

def uninstall(pkg, yolo=False):
  ## print(f"wahoo: Running 'sudo pacman -Rns {pkg}'...")
  sourcedir = Path.home() / ".wahoo" / "source" / pkg
  
  run(f"sudo pacman -Rns {pkg} --noconfirm", yolo=False) # the print above was commented out since run() already shows what command is being run, so its redundant to have two of them.
  print(f"wahoo! {pkg} uninstalled.")
  print("wahoo: Cleaning up source directory...")
  run(f"rm -rf {sourcedir}", yolo=False, exit=True)
  print("wahoo! Source directory cleaned.")
  

def help():
  # i wish i didn't have to update this with every commit
  print("[Available commands]")
  print("install, -S:                  Installs a package from the AUR.")
  print("uninstall, remove, -R, -Rns:  Uninstalls an existing package.")
  print("help, -H:                     Prints this message.")
  print("update, -Sy:                  Updates an existing AUR package. You can also update wahoo with this.")
  print("list, -Q, -Qs                 Shows all packages installed. If used with a second argument, it'll search for packages of the same name on your system.")
  print("info, show, -Qi               Shows info for a specific package.")
  print("[Available flags]")
  print("Nothing yet.")
  print("[Usage]")
  print("wahoo -S foo")
  print("wahoo install foo")
  print("wahoo update wahoo")
  print("wahoo -Sy foo")
  print("wahoo uninstall foo")

def flagparsing(flags):
  print("wahoo warn: No flag support yet.") # uhhhhh
  return

def update(pkg):
  if not internet_check():
    print("wahoo error: No internet. Aborting...")
    sys.exit(1)
  wahooroot = Path.home() / ".wahoo" / "source" / pkg

  if not wahooroot.exists():
    print(f"wahoo error: {pkg} doesn't exist on your system. Install it with wahoo install {pkg}.") # might make it call install() here since maybe people are using wahoo with the pacman command syntax. if i do that, this will change from a 'wahoo error' to a 'wahoo warn'.
    return

  print(f"wahoo: Starting update")
  print("wahoo: Pulling latest update from AUR...")
  try:
    run("git pull", wahooroot)
  except:
    return

  prompt = input(f"wahoo: Rebuild and install {pkg}? [Y/n]").strip().lower()
  if prompt == "n":
    print("wahoo: Skipping reinstall.")
    return

  try:
    print("wahoo: Starting rebuild...")
    print("wahoo: Removing old package...")
    uninstall(pkg, True) # runs with yolo
    print("wahoo: Building and installing...")
    run("makepkg -si", wahooroot, True)
    print(f"wahoo! {pkg} updated.")
  except:
    return

def search():
  print("Nothing here yet...") # coming soon! ...in valve time.

def main():
  if len(sys.argv) < 2:
    help()
    sys.exit(1)

  cmd = sys.argv[1]
  pkg = sys.argv[2] if len(sys.argv) > 2 else None
  flags = sys.argv[3:] if len(sys.argv) > 3 else None
  cmd = cmd.lower() # i know there's going to be someone stupid enough to type wahoo iNstALL
  if flags:
    flagparsing(flags)

  match cmd: # i love match case
    case ("install" | "-S"):
      if not pkg:
        print("wahoo error: No package or invalid package specified.")
        sys.exit(1)
      
      if pkg == "wahoo": # why would you try to download wahoo with wahoo?
        print("wahoo: Bold of you to try to install wahoo with wahoo.")
        os.kill(os.getpid(), 11) # this legit gives you a segmentation fault error
      
      install(pkg)  
    case ("remove" | "uninstall" | "-R" | "-Rns"):
      uninstall(pkg)
    case ("help" | "-H" | "--help" | "--h"):
      help()
      sys.exit(1)
    case ("version" | "--version"):
      print("wahoo - v0.3 beta")
      print("made with <3 by spark :D")
    case ("update" | "-Sy"):
      if not pkg:
        print("wahoo error: No package or invalid package specified.")
        return

      if pkg == "wahoo":
        print("wahoo: Self update requested. Updating with install.sh...")
        ensure_install_sh()
        os.chdir(Path.home() / ".wahoo/source/wahoo/")
        try:
          subprocess.run("./install.sh update", shell=True, check=True)
        except subprocess.CalledProcessError:
          print("wahoo error: install.sh failed. Is it not executable, or does it not exist?")
      else:
        update(pkg)
    case ("list" | "-Q" | "-Qs"):
      if pkg:
        run(f"sudo pacman -Qs {pkg}", yolo=True)
        return

      run("sudo pacman -Q", yolo=True)
    case ("show" | "-Qi"):
      if not pkg:
        print("wahoo error: No package or invalid package specified.")
        return

      run(f"sudo pacman -Qi {pkg}", yolo=True)
    case _:
      print("wahoo: Invalid command.")
      help()
      sys.exit(1)

# MAIN

if __name__ == "__main__":
  try:
    main() # this doesn't run main if wahoo is imported as a module
  except KeyboardInterrupt:
    print("wahoo: Interrupted by Ctrl+C, see you next time") # lol
