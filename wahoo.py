#!/usr/bin/python3

## wahoo!
## v0.5 alpha
## made with <3 by spark
## certain lines of code will be commented out with ##. thats an intentional decision, a.k.a. me trying to speedrun coding
## feel free to replace the docstrings with things that make more sense. just don't touch my comments. or anyone's comments, really.
## just remove satisfied TODO comments. a clean codebase is a happy codebase :)

version = "0.4" # NOTE: i didn't update this because the config loading hasn't been fully implemented yet.
colors = {
  "white": "\u001b[97m",
  "green": "\u001b[32m",
  "yellow": "\u001b[33m",
  "red": "\u001b[31m",
  "blue": "\u001b[34m"
}

# LIBRARIES AND MODULES

import sys
from pathlib import Path
import subprocess
from os import getuid
import tomllib # requires python 3.11+

## pip packages
import requests
from rapidfuzz import fuzz

# CLASSES

class config: # unused currently. will be used later i promise
  # NOTE: this doesn't use the ANSI colors

  def __init__(self):
    self.config_path = self.find_config_file()
    self.config_data = None

  def load_config(self):
    if not self.config_path:
      return

    try:
      with open(self.config_path, "rb") as f:
        return tomllib.load(f)

    except Exception as e:
      print(f"wahoo error: Failed to load config from {self.config_path}. ({e})")

  def parse_config(self):
    self.config_data = self.load_config()
    data = self.config_data

    print("not implemented :/")
    print("here's all the data in your config though:")
    print(data)

  def find_config_file(self, force=None):
    wahoo_config = Path.home() / ".wahoo" / "config.toml"
    linux_config = Path.home() / ".config" / "wahoo" / "config.toml"
    
    # priority: ~/.wahoo/config.toml -> ~/.config/wahoo/config.toml -> ~/.wahoo/default.toml
    # will throw an error if none of them are found.
    if not force:
      if wahoo_config.exists():
        return wahoo_config
      elif linux_config.exists():
        return linux_config
      else:
        return None
    else:
      return force

# ANSI COLORS

# one little thought that i had is that i should add colors for the [Y/n] things you see often
# not now though. programmer laziness at its finest (insert smug face here)

## allow_coloring = True
allow_coloring = sys.stdout.isatty()
reset = "\033[0m"
wahoo_message = colors["white"] if allow_coloring else reset
wahoo_error = colors["red"] if allow_coloring else reset
wahoo_warn = colors["yellow"] if allow_coloring else reset
wahoo_success = colors["green"] if allow_coloring else reset # green

# FUNCTIONS

def internet_check():
  '''
  Pings archlinux.org to check for internet. Returns <True> if internet is available, and <False> if not.
  '''
  
  try:
    requests.get("https://archlinux.org", timeout=3)
    return True
  except requests.RequestException: # which usually means no internet
    return False

def prompt(msg, yolo=False, exit_on_abort=False, use_msg_as_prompt=False, show_abort_msg=True):
  '''
  CLI component. (also used outside of the CLI for safety reasons)
  Prompts the user for confirmation. Returns <False> if the user aborts, and <True> if the user confirms.
  I really just recycled this from the run() function lmao
  Arguments:
  - msg (the message to be printed)
  - yolo (if <True>, skips the prompt and immediately returns <True>)
  - exit_on_abort (if <True>, returns <False> if the user aborts, and if <False>, exits the script with code 0)
  '''
  # once again, exit_on_abort is a misnomer.
  # i should probably rename it to dont_exit or smth like that?
  # later.

  if not yolo:
    if not use_msg_as_prompt:
      print(msg)
      user_input = input("Proceed? [Y/n] ").strip().lower()
    else:
      user_input = input(msg).strip().lower()

    if user_input == "n":
      if show_abort_msg:
        print("Aborted.")
      if exit_on_abort:
        return False
      else:
        sys.exit(0)
  else:
    print(msg)

  return True

  
def run(cmd, dir=None, yolo=False, exit_on_abort=False, verbose=True, silent=False):
  '''
  Runs a shell command.
  Arguments:
  - cmd (the command to be run)
  - dir (changes working directory)
  - yolo (runs without confirmation)
  - exit_on_abort (on abort, it will run return if <True> and will exit if <False>.)
  Do note that `exit_on_abort` is actually just routed straight to the prompt() function. Programmer laziness at its finest.
  '''
  # see the prompt() function on my thoughts on exit_on_abort's ridiculous name

  if not silent and not prompt(f"{wahoo_message}wahoo: {reset}Running {cmd}", yolo, exit_on_abort):
    if exit_on_abort:
      sys.exit(0)
    else:
      return
    
  try:
    subprocess.run(cmd, shell=True, check=True, cwd=dir)
  except subprocess.CalledProcessError as e:
    # here comes the error handling. this took a while to write but it was worth it
    error = cmd.split()[0] if cmd else "???"

    match error:
      case "git":
        print(f"{wahoo_error}wahoo error: {reset}Git ran into an error. ({wahoo_error}{e}{reset})")
      case "makepkg":
        print(f"{wahoo_error}wahoo error: {reset}Failed to build package. ({wahoo_error}{e}{reset})")
      case "pacman":
        print(f"{wahoo_error}wahoo error: {reset}pacman ran into an error. ({wahoo_error}{e}{reset})")
      case _:
        print("??????????????")
        print("Congratulations, you managed to break wahoo's error handling. A winner is you!") # the easter eggs never end
        print("Did you try turning it on and back off again?")
          
        if verbose:
          print(f"details: {wahoo_error}{e}{reset}")

    sys.exit(2)

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
    print(f"{wahoo_message}wahoo: {reset}Bold of you for trying to install wahoo with wahoo.")
    print("Segmentation fault (core dumped)") # originally, it ran os.kill(os.getpid(), 11) but i removed it in case some strict AUR mod decides to kill me.
    sys.exit(11) # hehe
    
  if not internet_check():
    print(f"{wahoo_error}wahoo error: {reset}No internet. Aborted.")
    sys.exit(1)
  
  wahooroot = Path.home() / ".wahoo" / "source"
  wahooroot.mkdir(parents=True, exist_ok=True)

  sourcedir = wahooroot / pkg

  try:
    if not sourcedir.exists():
      print(f"{wahoo_message}wahoo: {reset}Starting install")
      if source == "https://aur.archlinux.org":
        print(f"{wahoo_message}wahoo: {reset}Downloading {pkg} from AUR...")
      else:
        print(f"{wahoo_message}wahoo: {reset}Downloading {pkg}...")

      if yolo:
        run(f"git clone {source}/{pkg}.git", wahooroot, yolo)
      else:
        run(f"git clone {source}/{pkg}.git", wahooroot, False)
      print(f"{wahoo_success}wahoo! {reset}{pkg} Downloaded.")

    else:
      print(f"{wahoo_warn}wahoo warn: {reset}{pkg} source already exists at {sourcedir}.")

    if build:
      print(f"{wahoo_message}wahoo: {reset}Installing {pkg}...")

      if yolo:
        run("makepkg -si --noconfirm", sourcedir, yolo=True)
        sys.exit(0) # too lazy to do an else branch, here's a hard exit for now. no, i will not make it a return call.

      build_only = prompt(f"{wahoo_message}wahoo: {reset}Build package without installing? [y/N] ", yolo, True, True, False) # i really should rename exit_on_abort

      if build_only:
        print(f"{wahoo_message}wahoo: {reset}Building...")
        run("makepkg -s --noconfirm", sourcedir, True) # -s is used to install missing dependencies
        print(f"{wahoo_success}wahoo! {reset}{pkg} built successfully.")
      else:
        print(f"{wahoo_message}wahoo: {reset}Building and installing...")
        run("makepkg -si --noconfirm", sourcedir, True) # -si both installs missing dependencies and the built package
        print(f"{wahoo_success}wahoo! {reset}{pkg} installed.")
  except Exception as e:
    print(f"{wahoo_error}wahoo error: {reset}Install failed. ({wahoo_error}{e}{reset})")

def ensure_install_sh():
  '''
  CLI component. checks if wahoo's install.sh is present in the source directory. if not, then it downloads it straight from source.
  '''
  # TODO: rewrite this
  
  wahooroot = Path.home() / ".wahoo" / "source" / "wahoo"
  install_sh = wahooroot / "install.sh"

  if not install_sh.exists():
    print(f"{wahoo_warn}wahoo warn: {reset}install.sh does not exist in the wahoo directory.")
    install("wahoo", "https://github.com/sparkhere-sys", False, segfault=False) # since this uses install() and that checks for internet when its called, i don't need to add an internet check in ensure_install_sh()
    print(f"{wahoo_success}wahoo! {reset}Latest update fetched, and install.sh has been downloaded.")
    print(f"{wahoo_message}wahoo: {reset}Making install.sh executable...")
    run("chmod +x install.sh > /dev/null", wahooroot)
  else:
    # most likely, the install.sh file is not executable after already updating wahoo with it
    run("chmod +x install.sh > /dev/null", wahooroot, silent=True) # so this just runs silently

def uninstall(pkg, yolo=False, Rns=True):
  '''
  uses pacman to uninstall a package, AUR or not.
  Arguments:
  - pkg (the package to be uninstalled)
  - yolo (if <True>, will run the run() function with yolo=True)
  '''

  if pkg == "wahoo":
    print(f"{wahoo_error}wahoo error: {reset}Trying to uninstall wahoo while wahoo is running isn't a good idea.")
    print("Uninstall it manually with pacman.")
    sys.exit(1)
  
  sourcedir = Path.home() / ".wahoo" / "source" / pkg
  
  if Rns:
    run(f"sudo pacman -Rns {pkg} --noconfirm", yolo=yolo)
  else:
    run(f"sudo pacman -R {pkg} --noconfirm", yolo=yolo)
  print(f"{wahoo_success}wahoo! {reset}{pkg} uninstalled.")

  if sourcedir.exists():
    print(f"{wahoo_message}wahoo: {reset}Cleaning up source directory...")
    run(f"rm -rf {sourcedir}", yolo=yolo, exit_on_abort=True)
  else:
    print(f"{wahoo_message}wahoo: {reset}No source directory found for {pkg}, skipping cleanup.")

  print(f"{wahoo_success}wahoo! {reset}Source directory cleaned.")

def help(cmd=None):
  '''
  CLI component. does exactly what it says on the tin.
  '''

  # my least favorite part of the code YAHOO
  # TODO: add colors to the help message
  main_help = """
[Available commands]
install, -S:                                    Installs a package from the AUR.
uninstall, remove, autoremove, -R, -Rns:        Uninstalls an existing package.
update, -Sy:                                    Updates an existing AUR package. You can also update wahoo by running this with wahoo as the package.
upgrade, -Syu:                                  Updates all packages installed with wahoo. Does not update packages installed with other AUR helpers.
list, -Q, -Qs:                                  Shows all packages installed. If you specify a package, it'll search for packages of the same name that are installed on your system.
info, show, -Qi:                                Shows info for a specific package.
search, -Ss:                                    Searches for a package in the AUR.
help:                                           You're reading it.
version:                                        Shows you the version of wahoo you're running.
[Available flags]
--yolo, --noconfirm:                            Skips all confirmation prompts. Use with caution.
--dont-remove-depends:                          (short: autoremove, -Rns) Doesn't remove orphaned dependencies. You never know when you might need that one library.              
[Example usage]
wahoo install <pkg>
wahoo -Sy <pkg>
wahoo remove <pkg>
wahoo -Syu --yolo
wahoo -Ss <pkg>
    """
  
  if not cmd:
    print(main_help)
    # you're welcome, future me
  else:
    match cmd:
      # long ass match-case block
      case ("install" | "-S"):
        print(f"""
[Usage]
wahoo {cmd} <pkg> <flags>

Installs a package from the AUR.
        """)

      case ("uninstall" | "remove" | "-R"):
        print(f"""
[Usage]
wahoo {cmd} <pkg> <flags>

Uninstalls a package from your system. Note that this just runs "pacman -R" so this command will work with ALL packages, AUR or not.
        """)

      case ("update" | "-Sy"):
        print(f"""
[Usage]
wahoo {cmd} <pkg> <flags>

Updates a package from the AUR. If you run "wahoo {cmd} wahoo", it will update wahoo itself.
        """)

      case ("upgrade" | "-Syu"):
        print(f"""
[Usage]
wahoo {cmd} <flags>

Updates all packages installed with wahoo. Does not update packages installed with other AUR helpers.
This command can also upgrade pacman packages, but it is up to you to decide if you want to do that.
Does not update wahoo itself. Use "wahoo update wahoo" for that.
        """)

      case ("list" | "-Q" | "-Qs"):
        print(f"""
[Usage]
wahoo {cmd} (optional: <pkg>)

Lists all packages. This just runs "pacman -Q", so it will work with all packages, AUR or not.
If you specify a package, it will search for packages of the same name that are installed on your system.
        """)

      case ("info" | "show" | "-Qi"):
        print(f"""
[Usage]
 wahoo {cmd} <pkg>

Shows information about a specific package. This just runs "pacman -Qi", so it will work with all packages, AUR or not.
        """)

      case ("search" | "-Ss"):
        print(f"""
[Usage]
wahoo {cmd} <pkg>

Searches for a package from the AUR.
        """)

      case ("--yolo" | "--noconfirm"):
        print("""
Skips any confirmation prompts in a command. If the command doesn't have any confirmation prompts, then save yourself the effort of typing this and don't use it.
Use with caution.
        """)

      case "version":
        print("Shows you the version of wahoo you're running.")

      case "help":
        print("help-ception")

      case "moo":
        print("Have you mooed today?") # you thought the segfault easter egg was the only one? pathetic.

      case _:
        print(main_help)

def flagparsing(flags):
  '''
  CLI component. parses flags given to wahoo and returns them as a dict.
  Arguments:
  - flags (the flags to be parsed)
  '''
  
  ## print("wahoo warn: No flag support yet.") # uhhhhh
  ## print("wahoo warn: Although flags are parsed, they will be ignored since they haven't been implemented yet. Sorry :/")

  parsed_flags = {
    "flag_yolo": False,
    "flag_remove_depends": False
  }

  for flag in flags:
    match flag:
      case ("--yolo" | "--noconfirm"):
        parsed_flags["flag_yolo"] = True
      case ("--dont-remove-depends" | "--dontremovedepends"):
        parsed_flags["flag_remove_depends"] = True
      case _:
        print(f"{wahoo_warn}wahoo warn: {reset}Unknown flag: '{flag}'. Ignoring.")

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
    print(f"{wahoo_error}wahoo error: {reset}No internet. Aborted.")
    sys.exit(1)
  
  wahooroot = Path.home() / ".wahoo" / "source" / pkg

  if not wahooroot.exists():
    print(f"{wahoo_error}wahoo error: {reset}{pkg} doesn't exist on your system. Install it with wahoo install {pkg}.") # might make it call install() here since maybe people are using wahoo with the pacman command syntax. if i do that, this will change from a 'wahoo error' to a 'wahoo warn'. v0.5 maybe.
    # note: this above line isn't foolproof since the user can just rename the directory to something else. i WOULD put a file named smth like .wahoo but that would be a waste of time and effort.
    return

  print(f"{wahoo_message}wahoo: {reset}Starting update.")
  print(f"{wahoo_message}wahoo: {reset}Pulling latest update from AUR...")
  try:
    run("git pull", wahooroot)
  except Exception as e:
    print(f"{wahoo_error}wahoo error: {reset}Pull failed. {wahoo_error}({e}){reset}") # this looks like {} soup
    return

  if not yolo:
    prompt = input(f"{wahoo_message}wahoo: {reset}Rebuild and install {pkg}? [Y/n]").strip().lower()
    if prompt == "n":
      print("wahoo: Skipping reinstall.")
      return

  try:
    print(f"wahoo: Starting rebuild...")
    print(f"wahoo: Removing old package...")
    uninstall(pkg, True) # runs with yolo regardless of --yolo. bad UX? maybe. but i just want to push this update
    print(f"wahoo: Building and installing...")
    run("makepkg -si", wahooroot, True) # ditto
    print(f"wahoo! {reset}{pkg} updated.")
  except Exception as e:
    print(f"{wahoo_error}wahoo error: {reset}Update failed. {wahoo_error}({e}){reset}")
    sys.exit(1)

def upgrade(yolo=False):
  '''
  Upgrades all packages *installed with wahoo.* wahoo has no access to any packages installed with other AUR helpers, like yay or paru, so it won't do anything to those.
  Flow:
  - Runs an internet check
  - Prompts the user for confirmation (unless --yolo is used)
  - Goes through each package in ~/.wahoo/source and updates them (ignores wahoo itself)
  - (prompted) Runs an update to pacman packages with 'pacman -Sy' (requires sudo however. not sure how to get around that yet)
  '''

  # remind me never to write long comments again.
  if not internet_check():
    print(f"{wahoo_error}wahoo error: {reset}No internet. Aborted.")
    sys.exit(1)
  
  # 12/6/2025: added the prompt
  if prompt(f"{wahoo_message}wahoo: {reset}Start upgrade? [Y/n] ", yolo, exit_on_abort=False):
    print(f"{wahoo_message}wahoo: {reset}Updating all packages...")
    wahooroot = Path.home() / ".wahoo" / "source"
    print(f"{wahoo_message}wahoo: {reset}To update wahoo itself, run {wahoo_warn}'wahoo update wahoo'{reset} or {wahoo_warn}'wahoo -Sy wahoo'{reset}.") # using {wahoo_warn} as highlighting, no warn here :)
  
    for pkg in wahooroot.iterdir():
      if pkg.is_dir() and pkg.name != "wahoo": # don't update wahoo itself here.
        pkg_name = pkg.name
        print(f"{wahoo_message}wahoo: {reset}Updating {pkg_name}...")
        update(pkg_name, yolo=True) # note: this assumes that you already went through the prompt at the start of the function

    prompt(f"{wahoo_message}wahoo: {reset}Would you like to do a system update as well? (with pacman -Sy) [Y/n]", yolo, True) # if the user says no, then it will exit the program, which is why i didn't put this in an if block. lazy code i know.
    run("sudo pacman -Syu --noconfirm", yolo=True) # 12/6/2025 # since there's a prompt already for this, the prompt is ignored here. i also made it run with --noconfirm since if you said yes to the prompt then you probably know what you're doing.
    print(f"{wahoo_success}wahoo! {reset}Upgrade finished.")

def self_update():
  '''
  TODO: add docstring
  '''

  # TODO: update self updating feature
  
  print(f"{wahoo_message}wahoo: {reset}Starting self-update")
  ensure_install_sh()
  ## os.chdir(Path.home() / ".wahoo/source/wahoo/")
  wahooroot = Path.home() / ".wahoo" / "source" / "wahoo"
  try:
    subprocess.run("./install.sh update", shell=True, check=True, cwd=wahooroot)
  except subprocess.CalledProcessError as e:
    print(f"{wahoo_error}wahoo error: {reset}install.sh failed. {wahoo_error}({e}){reset}")
    sys.exit(3)

def search(pkg, limit=20, sort=True):
  '''
  Searches for a package from the AUR.
  Flow:
  - runs an internet check
  - sends a get request to the AUR
  - calls return if no packages were found
  - prints the details of each package (name, description, and votes)
  Arguments:
  - pkg (the package to be searched for)
  - limit (how many packages to show)
  - sort (if <True>, then will use rapidfuzz's string matching, otherwise will use old sorting)
  '''
  
  if not internet_check():
    print(f"{wahoo_error}wahoo error: {reset}No internet. Aborted.")
    sys.exit(1)

  url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={pkg}"
  
  try:
    response = requests.get(url, timeout=3)
    data = response.json()
    results = data.get("results", [])

    if not results:
      print(f"{wahoo_message}wahoo: {reset}No results found for {pkg}.")
      print(f"{wahoo_message}wahoo: {reset}If it's not an AUR package, try searching for it with pacman.")
      return
      
    # HACK: THIS IF BLOCK DOWN THERE IS A BUG
    # the only reason i haven't fixed this yet, is because this function NEVER runs with sort=False
    # remind future me to fix this
    if any(entry["Name"] == pkg for entry in results) and not sort:
      print(f"{wahoo_success}wahoo! {reset}Found an exact match for {pkg}.")
      name = results("Name", "unknown")
      desc = results("Description", "no description")
      votes = results.get("NumVotes", "???")
      print(f"- {wahoo_success}{name} {reset} ({wahoo_warn}{votes} {reset}votes): {desc} \n") 

    if sort:
      results.sort(
        key=lambda entry: fuzz.WRatio(pkg, entry.get("Name", "unknown")), 
        reverse=True
      )

    shown = results[:limit]

    if len(results) > limit:
      print(f"{wahoo_success}wahoo! {reset}Found {len(results)} results for '{pkg}', showing the first {limit} results.")
    else:
      print(f"{wahoo_success}wahoo! {reset}Found {len(results)} results for '{pkg}'.")
    
    for entry in shown:
      name = entry.get("Name", "unknown")
      desc = entry.get("Description", "no description")
      votes = entry.get("NumVotes", "???")
      print(f" - {wahoo_success}{name} {reset}({wahoo_warn}{votes} {reset}votes): {desc}")
  except Exception as e:
    print(f"{wahoo_error}wahoo error: {reset}Failed to fetch search results. ({wahoo_error}{e}{reset})")
  
def main():
  '''
  CLI component. has a match case block which runs the functions above. if you read the code then this will be easy to understand.
  '''
  
  if getuid() == 0:
    print(f"{wahoo_error}wahoo error: {reset}Don't run wahoo as root. Otherwise, wahoo will exit unexpectedly.")
    # well this is kinda stupid
    # technically, some commands require sudo to be run (like uninstalling a package)
    # i should probably add the sudo check to the functions that require to be run without sudo instead of slapping it here in the CLI
    # v0.5?
    sys.exit(1)
  
  if len(sys.argv) < 2:
    help()
    sys.exit(1)

  cmd = sys.argv[1] if len(sys.argv) >= 2 else "help" # if no command is given, then it just gives you the help message. good UX methinks
  pkg = sys.argv[2] if len(sys.argv) >= 3 else None
  flags = sys.argv[3:] if len(sys.argv) >= 4 else None
  ## cmd = cmd.lower() # removed this because it checks for -S but it sees -s instead
  parsed_flags = flagparsing(flags) if flags else {}

  # FLAGS
  flag_yolo = parsed_flags.get("flag_yolo", False)
  flag_rns = parsed_flags.get("flag_remove_depends", False)

  match cmd:
    # while wahoo is not intended to be a wrapper for pacman, it does have some commands that point straight to pacman (info and list)
    # if i were to stay true to the "wahoo is not a pacman wrapper" philosophy, i would have removed these commands
    # but i figure they're essential enough to keep (good UX, and they make wahoo more useful)
    # that said, wahoo is not a replacement for pacman, never has, never will. if you want that, just use archapt or pacman straight up
    # hell you can just add random aliases to your .bashrc or .zshrc if you REALLY want to use apt syntax with pacman and don't want to install a wrapper
    
    case ("install" | "-S"):
      if not pkg:
        print("wahoo error: No package or invalid package specified.")
        sys.exit(1)
      
      install(pkg, yolo=flag_yolo) 

    case ("remove" | "uninstall" | "-R" | "-Rns" | "autoremove"):
      if not pkg:
        print(f"{wahoo_error}wahoo error: {reset}No package or invalid package specified.")
        sys.exit(1)
      
      if cmd == "-Rns" or cmd == "autoremove":
        uninstall(pkg, yolo=flag_yolo, Rns=True)
      else:
        uninstall(pkg, yolo=flag_yolo, Rns=flag_rns)

    case ("help" | "-H" | "--help" | "--h"):
      help(pkg) # okay i understand if this looks weird, but pkg is = sys.argv[2] and in this case, that would be the command that you want help with. as in, wahoo help install. see what im getting at?
      sys.exit(1)

    case ("version" | "--version"):
      print(f"{wahoo_success}wahoo{reset} v{version}")
      print("made with <3 by spark")
      print(f"{wahoo_warn}tip: {reset}run {wahoo_warn}'wahoo update wahoo'{reset} or {wahoo_warn}'wahoo -Sy wahoo'{reset} to update wahoo to the latest version.") # i think the yellow looks cool

    case ("update" | "-Sy"):
      if not pkg:
        print(f"{wahoo_error}wahoo error: {reset}No package or invalid package specified.")
        return

      if pkg == "wahoo":
        self_update()
      else:
        update(pkg)

    case ("list" | "-Q" | "-Qs"):
      if pkg:
        run(f"pacman -Qs {pkg}", yolo=True)
        return

      run("pacman -Q", yolo=True)

    case ("show" | "-Qi" | "info"): # i forgot to add the "info" alias lmao
      if not pkg:
        print(f"{wahoo_error}wahoo error: {reset}No package or invalid package specified.")
        return

      run(f"pacman -Qi {pkg}", yolo=True) # this literally just runs a pacman command lmao

    case ("search" | "-Ss"):
      search(pkg)

    case ("upgrade" | "-Syu"):
      ## print("wahoo warn: Upgrade command is still a WIP.")
      upgrade(yolo=flag_yolo)

    case _:
      print(f"{wahoo_warn}wahoo: {reset}Invalid command.") # it uses the wahoo warn color despite not being a wahoo warn, but that's because its not really that big of a deal. 
      help()
      return

# MAIN

if __name__ == "__main__":
  try:
    main() # this doesn't run main if wahoo is imported as a module
  except KeyboardInterrupt:
    print(f"{wahoo_message}wahoo: {reset}Interrupted by Ctrl+C, see you next time") # lol
    # yes i even added ansi colors here, deal with it
