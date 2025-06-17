#!/usr/bin/python3

## wahoo!
## v0.4 release candidate 1
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

# developer's note again (12/6/2025)
# v0.4 is basically done! the road to v1.0 looks clearer now!
# that being said, i will change v0.4 alpha to v0.4 beta
# stable will release when i add colored output :D

version = "0.4 release candidate 2"

# ANSI COLORS
allow_coloring = True # will add a config file in v0.5 or v0.6
reset = "\033[0m"
wahoo_message = "\033[97m" if allow_coloring else reset # white
# one little thought that i had is that i should add colors for the [Y/n] things you see often
# not now though. programmer laziness at its finest
wahoo_error = "\033[31m" if allow_coloring else reset # red
wahoo_warn = "\033[33m" if allow_coloring else reset # yellow
wahoo_success = "\033[32m" if allow_coloring else reset # green

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
  # that will probably be for the stable release of v0.4, because laziness

  print(msg)
  if not yolo:
    if not use_msg_as_prompt:
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

  
def run(cmd, dir=None, yolo=False, exit_on_abort=False, verbose=True):
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
  
  if prompt(f"{wahoo_message}wahoo: {reset}Running {cmd}", yolo, exit_on_abort):    
    try:
      subprocess.run(cmd, shell=True, check=True, cwd=dir)
    except subprocess.CalledProcessError as e:
      # here comes the error handling. this took a while to write but it was worth it
      # TODO: rewrite this to use match-case
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

          if verbose:
            print(f"details: {wahoo_error}{e}{reset}")

      ## if cmd.startswith("git"):
      ##   print(f"{wahoo_error}wahoo error: {reset}Git ran into an error. Is the package name correct?")
      ## elif cmd.startswith("makepkg"):
      ##   print(f"{wahoo_error}wahoo error: {reset}Failed to build package. Is there an error in the PKGBUILD?")
      ## elif "pacman" in cmd and "-Rns" not in cmd:
      ##   print(f"{wahoo_error}wahoo error: {reset}pacman failed to install package.")
      ## elif "pacman" in cmd:
      ##   print(f"{wahoo_error}wahoo error: {reset}pacman failed to uninstall package. Are you sure it exists on your system?")
      ## else:
      ##   print(f"{wahoo_error}wahoo error: {reset}Command failed.")

      sys.exit(2)

def install(pkg, source="https://aur.archlinux.org/packages", build=True, segfault=True, yolo=False):
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

  if not sourcedir.exists():
    print(f"{wahoo_message}wahoo: {reset}Starting install")
    if source == "https://aur.archlinux.org/packages":
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

    build_only = prompt(f"{wahoo_message}wahoo: {reset}Build package without installing? [y/N]", yolo, False, True, False)
    if build_only:
      print(f"{wahoo_message}wahoo: {reset}Building...")
      run("makepkg -s --noconfirm", sourcedir, True) # -s is used to install missing dependencies
      print(f"{wahoo_success}wahoo! {reset}{pkg} built successfully.")
    else:
      print(f"{wahoo_message}wahoo: {reset}Building and installing...")
      run("makepkg -si --noconfirm", sourcedir, True) # -si both installs missing dependencies and the built package
      print(f"{wahoo_success}wahoo! {reset}{pkg} installed.")

def ensure_install_sh():
  '''
  CLI component. checks if wahoo's install.sh is present in the source directory. if not, then it downloads it straight from source.
  '''
  
  wahooroot = Path.home() / ".wahoo" / "source" / "wahoo"
  install_sh = wahooroot / "install.sh"

  if not install_sh.exists():
    print(f"{wahoo_warn}wahoo warn: {reset}install.sh does not exist in the wahoo directory. Downloading...")
    install("wahoo", "https://github.com/sparkhere-sys", False, segfault=False) # since this uses install() and that chekcks for internet when its called, i don't need to add an internet check in ensure_install_sh()
    print(f"{wahoo_success}wahoo! {reset}Latest update fetched, and install.sh has been downloaded.")
    print(f"{wahoo_message}wahoo: {reset}Making install.sh executable...")
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
    print(f"{wahoo_error}wahoo error: {reset}Trying to uninstall wahoo while wahoo is running isn't a good idea.")
    print("Uninstall it manually with pacman.")
    sys.exit(1)
  
  sourcedir = Path.home() / ".wahoo" / "source" / pkg
  
  run(f"sudo pacman -Rns {pkg} --noconfirm", yolo=yolo) # the print above was commented out since run() already shows what command is being run, so its redundant to have two of them.
  # TODO: add a flag that runs pacman with -R instead of -Rns so it doesn't remove orphaned dependencies
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
  if not cmd:
    print("""
    [Available commands]
    install, -S:                  Installs a package from the AUR.
    uninstall, remove, -R:        Uninstalls an existing package.
    update, -Sy:                  Updates an existing AUR package. You can also update wahoo by running this with wahoo as the package.
    upgrade, -Syu:                Updates all packages installed with wahoo. Does not update packages installed with other AUR helpers.
    list, -Q, -Qs:                Shows all packages installed. If you specify a package, it'll search for packages of the same name that are installed on your system.
    info, show, -Qi:              Shows info for a specific package.
    search, -Ss:                  Searches for a package in the AUR.
    help:                         This message.
    version:                      Prints the version of wahoo you're running.
    [Available flags]
    --yolo, --noconfirm:          Skips all confirmation prompts. Use with caution.
    [Example usage]
    wahoo install <pkg>
    wahoo -Sy <pkg>
    wahoo remove <pkg>
    wahoo -Syu --yolo
    wahoo -Ss <pkg>
    """)
    # you're welcome, future me
  else:
    match cmd:
      ## pass # later.
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
  print(f"{wahoo_message}wahoo: {reset}Self update requested. Updating with install.sh...")
  ensure_install_sh()
  ## os.chdir(Path.home() / ".wahoo/source/wahoo/")
  wahooroot = Path.home() / ".wahoo" / "source" / "wahoo"
  try:
    subprocess.run("./install.sh update", shell=True, check=True, cwd=wahooroot)
  except subprocess.CalledProcessError as e:
    print(f"{wahoo_error}wahoo error: {reset}install.sh failed. {wahoo_error}({e}){reset}")
    sys.exit(3)

def search(pkg, limit=20):
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

    if len(results) > limit:
      print(f"wahoo! Found {len(results)} results for '{pkg}', showing the first {limit} results.")
    else:
      print(f"{wahoo_success}wahoo! {reset}Found {len(results)} results for '{pkg}'.")
    for entry in results[:limit]:
      name = entry.get("Name", "unknown")
      desc = entry.get("Description", "no description")
      votes = entry.get("NumVotes", 0)
      print(f" - {wahoo_success}{name} {reset}({wahoo_warn}{votes} {reset}votes): {desc}")
  except Exception as e:
    print(f"{wahoo_error}wahoo error: {reset}Failed to fetch search results. ({wahoo_error}{e}{reset})")
  
def main():
  '''
  CLI component. has a match case block which runs the functions above. if you read the code then this will be easy to understand.
  '''
  
  if os.geteuid() == 0:
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
  flag_yolo = parsed_flags.get("flag_yolo", False)
  ## no_pkg_error = # i will define this later, hence why its commented out.

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

    case ("remove" | "uninstall" | "-R"):
      if not pkg:
        print(f"{wahoo_error}wahoo error: {reset}No package or invalid package specified.")
        sys.exit(1)
      
      uninstall(pkg, yolo=flag_yolo)

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
      sys.exit(1)

# MAIN

if __name__ == "__main__":
  try:
    main() # this doesn't run main if wahoo is imported as a module
  except KeyboardInterrupt:
    print(f"{wahoo_message}wahoo: {reset}Interrupted by Ctrl+C, see you next time") # lol
    # yes i even added ansi colors here, deal with it
