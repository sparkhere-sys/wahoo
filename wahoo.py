#!/usr/bin/python3

## wahoo!
## v0.4 alpha
## made with <3 by spark
## certain lines of code will be commented out with ##. thats an intentional decision, a.k.a. me trying to speedrun coding
## feel free to replace the docstrings with things that make more sense. just don't touch my comments. or anyone's comments, really. just remove TODO comments if you see that they're implemented. a clean codebase is a happy codebase :)

# quick developer's note,
# i haven't implemented this yet but im leaving this note here for future me
# an exit code of 0: command went off without a hitch, no problems here.
# an exit code of 1: CLI error. nothing to worry about (i think)
# an exit code of 2: something went wrong in the run() function, like a subprocess error
# an exit code of 3: something went wrong somewhere else in the code.
# an exit code of 11: yeah thats the segfault easter egg lol
# an exit code of anything else: god knows what happened
# an exit code of 255: i have no fucking clue why this would happen but if it does then something went catastrophically wrong

# also im never using classes. never. not until i get used to them at the very least.

version = "0.4 alpha"

# LIBRARIES AND MODULES
import sys
from pathlib import Path
import subprocess
import os
import requests # depends on python-requests

# FUNCTIONS
def internet_check():
  '''
  Pings google.com to check for internet. Returns <True> if internet is available, and <False> if not.
  '''
  
  try:
    requests.get("https://google.com", timeout=3)
    return True
  except requests.RequestException: # which usually means no internet
    return False

def prompt(msg, yolo=False, exit=False):
  '''
  CLI component. Prompts the user for confirmation before running a command.
  I really just recycled this from the run() function lmao
  I won't bother writing a docstring for this, it's 8:00 PM as I'm writing this and I have better things to code.
  '''

  # TODO: Rename exit to something that makes more sense

  print(msg)
  if not yolo:
    user_input = input("Proceed? [Y/n] ").strip().lower()
    if user_input == "n":
      print("Aborted.")
      if exit:
        return "ABORT" # idk if this will work lmfao
      else:
        sys.exit(0)
    return "CONTINUE" # ditto

  
def run(cmd, dir=None, yolo=False, exit=False):
  '''
  Runs a shell command.
  Arguments:
  - cmd (the command to be run)
  - dir (changes working directory)
  - yolo (runs without confirmation)
  - exit (on abort, it will run return if <True> and will exit if <False>.)
  Do note that `exit` is actually just routed straight to the prompt() function. Programmer laziness at its finest.
  '''
  # TODO: Rename exit to something that makes more sense

  prompt(f"wahoo: Running {cmd}", yolo, exit) # HOLY SHIT HOW DID I FORGET TO ADD THIS UUAGAUHGAUAGUAGAUGAUGAAHGAUHAGUAGAUHAGA
  try:
    subprocess.run(cmd, shell=True, check=True, cwd=dir)
  except subprocess.CalledProcessError:
    # here comes the error handling. this took a while to write but it was worth it
    # TODO: rewrite this to use match-case
    if cmd.startswith("git"):
      print("wahoo error: Git ran into an error. Is the package name correct?")
    elif cmd.startswith("makepkg"):
      print("wahoo error: Failed to build package. Is there an error in the PKGBUILD?")
    elif "pacman" in cmd and "-Rns" not in cmd:
      print("wahoo error: pacman failed to install package.")
    elif "pacman" in cmd:
      print("wahoo error: pacman failed to uninstall package. Are you sure it exists on your system?")
    else:
      print("wahoo error: Command failed.")
    sys.exit(1)

def install(pkg, source="https://aur.archlinux.org", build=True, segfault=True, yolo=False):
  '''
  Downloads, builds, and installs a package.
  Flow:
  - Runs an internet check
  - Runs git clone to download a package
  - Builds (and by default, installs) the package with makepkg
  Arguments:
  - pkg (the package to be installed)
  - source (where to clone the git repo from, by default its the AUR)
  - build (if <True>, then wahoo will run makepkg.)
  - segfault (if <True>, then the segmentation fault easter egg occurs)
  - yolo (if <True>, skips all confirmation prompts and runs the run() function with yolo=True)
  '''
  
  if pkg == "wahoo" and segfault:
    print("wahoo: Bold of you for trying to install wahoo with wahoo.")
    print("Segmentation fault (core dumped)") # originally, it ran os.kill(os.getpid(), 11) but i removed it in case some strict AUR mod decides to kill me.
    sys.exit(11) # hehe
    
  if not internet_check():
    print("wahoo error: No internet. Aborted.")
    sys.exit(1)
  
  wahooroot = Path.home() / ".wahoo" / "source"
  wahooroot.mkdir(parents=True, exist_ok=True)

  sourcedir = wahooroot / pkg

  if not sourcedir.exists():
    print("wahoo: Starting install")
    if source == "https://aur.archlinux.org":
      print(f"wahoo: Downloading {pkg} from AUR...")
    else:
      print(f"wahoo: Downloading {pkg}...")

    if yolo:
      run(f"git clone {source}/{pkg}.git", wahooroot, yolo)
    else:
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
  '''
  CLI component. checks if wahoo's install.sh is present in the source directory. if not, then it downloads it straight from source.
  '''
  
  wahooroot = Path.home() / ".wahoo" / "source" / "wahoo"
  install_sh = wahooroot / "install.sh"

  if not install_sh.exists():
    print("wahoo warn: install.sh does not exist in the wahoo directory. Downloading...")
    install("wahoo", "https://github.com/sparkhere-sys/", False, segfault=False) # since this uses install() and that chekcks for internet when its called, i don't need to add an internet check in ensure_install_sh()
    print("wahoo! Latest update fetched, and install.sh has been downloaded.")
    print("wahoo: Making install.sh executable...")
    run("chmod +x install.sh", wahooroot)

def uninstall(pkg, yolo=False):
  '''
  uses pacman to uninstall a package, AUR or not.
  Arguments:
  - pkg (the package to be uninstalled)
  - yolo (if <True>, will run the run() function with yolo=True)
  '''
  
  ## print(f"wahoo: Running 'sudo pacman -Rns {pkg}'...")
  if pkg == "wahoo":
    print("wahoo error: Trying to uninstall wahoo while wahoo is running isn't a good idea.")
    print("Uninstall it manually with pacman.")
    sys.exit(1)
  
  sourcedir = Path.home() / ".wahoo" / "source" / pkg
  
  run(f"sudo pacman -Rns {pkg} --noconfirm", yolo=yolo) # the print above was commented out since run() already shows what command is being run, so its redundant to have two of them.
  print(f"wahoo! {pkg} uninstalled.")
  print("wahoo: Cleaning up source directory...")
  run(f"rm -rf {sourcedir}", yolo=yolo, exit=True)
  print("wahoo! Source directory cleaned.")
  

def help():
  '''
  CLI component. does exactly what it says on the tin.
  '''

  # my least favorite part of the code YAHOO

  print("[Available commands]")
  print("install, -S:                  Installs a package from the AUR.")
  print("uninstall, remove, -R, -Rns:  Uninstalls an existing package.")
  print("help, -H, --help:             Prints this message.")
  print("update, -Sy:                  Updates an existing AUR package. You can also update wahoo by running this with wahoo as the package.")
  print("list, -Q, -Qs                 Shows all packages installed. If used with a second argument, it'll search for packages of the same name on your system.")
  print("info, show, -Qi               Shows info for a specific package.")
  print("version, --version:           Prints the version of wahoo you're running.")
  print("[Available flags]")
  print("Nothing yet.")
  print("[Usage]")
  print("wahoo <command> <pkg> <flags> (for commands like install, uninstall, etc)")

def flagparsing(flags):
  '''
  CLI component. parses flags given to wahoo and returns them as a dict.
  Arguments:
  - flags (the flags to be parsed)
  '''
  
  ## print("wahoo warn: No flag support yet.") # uhhhhh
  ## print("wahoo warn: Although flags are parsed, they will be ignored since they haven't been implemented yet. Sorry :/")

  parsed_flags = {
    "flag_yolo": False
  }

  for flag in flags:
    match flag:
      case ("--yolo" | "--noconfirm"):
        parsed_flags["flag_yolo"] = True
      case _:
        print(f"wahoo warn: Unknown flag: '{flag}'. Ignoring.")

  return parsed_flags

def update(pkg, yolo=False):
  '''
  Updates a package from the AUR.
  Flow:
  - Runs an internet check
  - Calls return if the package doesn't exist
  - Pulls latest commits with git
  - Uninstalls the old package
  - Rebuilds and installs the package
  Arguments:
  - pkg (the pkg to be updated)
  - yolo (if <True>, skips all confirmation prompts and runs the run() function with yolo=True)
  '''
  
  if not internet_check():
    print("wahoo error: No internet. Aborted.")
    sys.exit(1)
  wahooroot = Path.home() / ".wahoo" / "source" / pkg

  if not wahooroot.exists():
    print(f"wahoo error: {pkg} doesn't exist on your system. Install it with wahoo install {pkg}.") # might make it call install() here since maybe people are using wahoo with the pacman command syntax. if i do that, this will change from a 'wahoo error' to a 'wahoo warn'. v0.5 maybe.
    return

  print(f"wahoo: Starting update")
  print("wahoo: Pulling latest update from AUR...")
  try:
    run("git pull", wahooroot)
  except Exception as e:
    print(f"wahoo error: Pull failed. ({e})")
    return

  if not yolo:
    prompt = input(f"wahoo: Rebuild and install {pkg}? [Y/n]").strip().lower()
    if prompt == "n":
      print("wahoo: Skipping reinstall.")
      return

  try:
    print("wahoo: Starting rebuild...")
    print("wahoo: Removing old package...")
    uninstall(pkg, True) # runs with yolo regardless of --yolo. bad UX? maybe. but i just want to push this update
    print("wahoo: Building and installing...")
    run("makepkg -si", wahooroot, True) # ditto
    print(f"wahoo! {pkg} updated.")
  except Exception as e:
    print(f"wahoo error: Update failed. ({e})")
    sys.exit(1)

def upgrade(yolo=False):
  '''
  IN PROGRESS
  I will write the docstring for this later.
  '''

  if not internet_check():
    print("wahoo error: No internet. Aborted.")
    sys.exit(1)
  
  # IMPORTANT: THIS FUNCTION DOESN'T HAVE A PROMPT! I'll add a prompt when I finish the 'prompt()' function but for now this will run by itself. I'm not responsible if you break your system with this.
  print("wahoo: Updating all packages...")
  wahooroot = Path.home() / ".wahoo" / "source"
  print("wahoo: To update wahoo itself, run 'wahoo update wahoo' or 'wahoo -Sy wahoo'.")
  
  for pkg in wahooroot.iterdir():
    if pkg.is_dir():
      pkg_name = pkg.name
      print(f"wahoo: Updating {pkg_name}...")
      update(pkg_name, yolo=True) # note: this assumes that you already went through the prompt at the start of the function, but that isn't implemented so this will run without confirmation. i know.
  
  ## run("sudo pacman -Syu --noconfirm", yolo=True) # i didn't implement this because i didn't finish the prompt() function yet, and i don't want to run this without confirmation. could break system packages if run willy nilly. maybe i'll change this to run pacman -Sy instead of -Syu. if you want to update the system, just run the pacman command directly. cmon, you're a big boy.
  # holy shit that above comment is long af, anyway
  print("wahoo! Upgrade finished.")

def self_update():
  print("wahoo: Self update requested. Updating with install.sh...")
  ensure_install_sh()
  os.chdir(Path.home() / ".wahoo/source/wahoo/")
  try:
    subprocess.run("./install.sh update", shell=True, check=True)
  except subprocess.CalledProcessError:
    print("wahoo error: install.sh failed. Is it not executable, or does it not exist?")

def search(pkg):
  '''
  Searches for a package from the AUR.
  Flow:
  - runs an internet check
  - sends a get request to the AUR
  - calls return if no packages were found
  - prints the details of each package (name, description, and votes)
  Arguments:
  - pkg (the package to be searched for)
  '''
  
  if not internet_check():
    print("wahoo error: No internet. Aborted.")
    sys.exit(1)

  url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={pkg}"
  
  try:
    response = requests.get(url, timeout=3)
    data = response.json()
    results = data.get("results", [])

    if not results:
      print(f"wahoo: No results found for {pkg}.")
      print("wahoo: If it's not an AUR package, try searching for it with pacman.")
      return

    print(f"wahoo! Found {len(results)} results for '{pkg}'.")
    for entry in results:
      name = entry.get("Name", "unknown")
      desc = entry.get("Description", "no description")
      votes = entry.get("NumVotes", 0)
      print(f" - {name} ({votes} votes): {desc}")
  except Exception as e:
    print(f"wahoo error: Failed to fetch search results. ({e})")
  
def main():
  '''
  CLI component. has a match case block which runs the functions above. if you read the code then this will be easy to understand.
  '''
  
  if os.geteuid() == 0:
    print("wahoo error: Don't run wahoo as root. Otherwise, wahoo will exit unexpectedly.")
    sys.exit(1)
  
  if len(sys.argv) < 2:
    help()
    sys.exit(1)

  cmd = sys.argv[1] if len(sys.argv) >= 2 else "help"
  pkg = sys.argv[2] if len(sys.argv) >= 3 else None
  flags = sys.argv[3:] if len(sys.argv) >= 4 else None
  cmd = cmd.lower() # i know there's going to be someone stupid enough to type wahoo iNstALL
  parsed_flags = flagparsing(flags) if flags else {}

  match cmd: # i love match case
    # this is literally the laziest code i have ever written lmfao
    # match-case is literally just nested if-else statements
    # i wonder if thats how they implemented it in the interpreter lol
    # food for thought ig

    case ("install" | "-S"):
      if not pkg:
        print("wahoo error: No package or invalid package specified.")
        sys.exit(1)
      
      install(pkg, yolo=parsed_flags.get("flag_yolo", False))  
    case ("remove" | "uninstall" | "-R" | "-Rns"):
      if not pkg:
        print("wahoo error: No package or invalid package specified.")
        sys.exit(1)
      
      uninstall(pkg, yolo=parsed_flags.get("flag_yolo", False))
    case ("help" | "-H" | "--help" | "--h"):
      help()
      sys.exit(1)
    case ("version" | "--version"):
      print(f"wahoo v{version}")
      print("made with <3 by spark")
      print("tip: run 'wahoo update wahoo' or 'wahoo -Sy wahoo' to update wahoo to the latest version.")
    case ("update" | "-Sy"):
      if not pkg:
        print("wahoo error: No package or invalid package specified.")
        return

      if pkg == "wahoo":
        self_update()
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
    case ("search" | "-Ss"):
      search(pkg)
    case ("upgrade" | "-Syu"):
      print("wahoo warn: Upgrade command is still a WIP.")
      upgrade()
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
