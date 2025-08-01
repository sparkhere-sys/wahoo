#!/usr/bin/env python3
'''
The installer class, split up from pkgmgr.py (for a reason)
'''

# LIBRARIES AND MODULES

from pathlib import Path
import sys
import subprocess

## wahoo stuff

from wahoo.constants import *
import wahoo.utils as utils
import wahoo.cli as cli

# CLASSES

# idk if i should flatten this
# make a pull request if you think so and i'll push it, no questions asked

class installer:
  '''
  installs a package from the AUR
  is called by the install() function in pkgmgr.py
  '''

  def __init__(self, pkg, source="https://aur.archlinux.org", yolo=False, build=True, segfault=True, silent=False, verbose=True):
    '''
    does this SERIOUSLY need a docstring
    '''

    self.pkg = pkg
    self.source = source
    self.yolo = yolo
    self.build = build
    self.segfault = segfault
    self.silent = silent
    self.verbose = verbose

    self.sourcedir = wahooroot / pkg

    self.aur_sources = ["https://aur.archlinux.org", "ssh://aur@aur.archlinux.org"]
  
  def segfault_easter_egg(self):
    '''
    hehe
    '''

    if self.pkg == "wahoo" and self.segfault:
      # muahahahahahaha
      cli.echo("Bold of you to try to install wahoo with wahoo.", color=None, prefix=None)
      cli.echo("Segmentation fault (core dumped)", color=None, prefix=None)
      sys.exit(11) # SIGSEGV
  
  def main(self):
    '''
    does this SERIOUSLY need a docstring
    just read the code dude...
    '''

    try:
      self.segfault_easter_egg()
      self.clone()
      self.resolve_depends()
      self.build_and_install()
    except Exception as e:
      cli.echo("Installation failed.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
      if self.verbose:
        cli.echo(f"Details: {e}", color=None, prefix=None)

      sys.exit(1)

  def resolve_depends(self):
    '''
    resolves AUR package dependencies
    dependencies that are in the official pacman repos are just installed by makepkg
    TODO: flatten this to make it more pythonic and DRY
    '''

    def parse_srcinfo():
      '''
      parses the .SRCINFO for dependencies
      '''

      # mmmm... nested functions...
      deps = []
      makedeps = []
      optdeps = []

      install_optdeps = cli.prompt("Install optional dependencies?", yolo=self.yolo, use_msg_as_prompt=True)

      with srcinfo_path.open('r') as f:
        for line in f:
          line = line.strip()
          if line.startswith("depends ="):
            dep = line.split('=', 1)[1].strip()
            deps.append(dep)

          elif line.startswith("makedepends ="):
            dep = line.split('=', 1)[1].strip()
            makedeps.append(dep)

          elif install_optdeps and line.startswith("optdepends ="):
            opt = line.split('=', 1)[1].strip()
            if ':' in opt:
              name, desc = opt.split(':', 1)
              optdeps.append((name.strip(), desc.strip()))
            else:
              optdeps.append((opt, None))
      
      return deps, makedeps, optdeps

    def is_installed(pkg):
      '''
      checks if a package is installed
      '''

      result = utils.run(f"pacman -Qi {pkg}", silent=True, text=True, return_result=True)
      return result and result.returncode == 0
    
    def is_in_pacman(pkg):
      '''
      checks if a package is in the official pacman repos
      '''

      result = utils.run(f"pacman -Si {pkg}", silent=True, text=True, return_result=True)
      return result and result.returncode == 0
    
    def install_aur_dep(pkg):
      '''
      in order to avoid recursion, this does NOT create a new instance of the class
      just to install the package.

      instead, it just runs the two commands needed to build and install a package.
      '''

      depdir = self.sourcedir

      # clone
      if not depdir.exists():
        utils.run(f"git clone {self.source}/{pkg}.git", dir=wahooroot, silent=self.silent, dont_exit=False)

      # build
      utils.run("makepkg -si", dir=depdir, silent=self.silent, dont_exit=False)

    try:
      cli.echo("Resolving dependencies...")
      srcinfo_path = self.sourcedir / ".SRCINFO"
      if not srcinfo_path.exists():
        result = utils.run("makepkg --printsrcinfo", yolo=True, dir=self.sourcedir, verbose=self.verbose, 
                           silent=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, return_result=True)
        
        if result and result.stdout:
          srcinfo_path.write_text(result.stdout)
        else:
          cli.echo("Failed to generate .SRCINFO", color=wahoo_colors["wahoo_warn"], prefix="wahoo warn")

      deps, makedeps, optdeps = parse_srcinfo()
      alldeps = deps + makedeps + [name for name, _ in optdeps]

      for dep in alldeps:
        if is_installed(dep):
          if self.verbose:
            cli.echo(f"{dep} already installed, skipping.")
          continue
          
        elif is_in_pacman(dep):
          if self.verbose:
            cli.echo(f"{dep} is in official repos, skipping.")
          
          # wahoo will refuse to run without -s on makepkg
          # so i see no point in running utils.run here
          continue
        
        else:
          if self.verbose:
            cli.echo(f"{dep} not found in official repos, installing from AUR...")
          
          install_aur_dep(dep)

    except Exception as e:
      cli.echo("Dependency resolution failed.", color=wahoo_colors["wahoo_error"], prefix="wahoo error")
      if self.verbose:
        cli.echo(f"Details: {e}", color=None, prefix=None)

  def clone(self):
    '''
    clones the git repo of the package to be installed
    '''

    cli.prompt("Starting install...", yolo=self.yolo, dont_exit=False)
    cli.echo(f"Installing {self.pkg}" + (f" from {self.source}..." if self.source not in self.aur_sources else "..."))
    if not self.sourcedir.exists():
      if self.verbose:
        cli.echo(f"Cloning {self.pkg} git repo ({self.source}/{self.pkg}.git) to {self.sourcedir}")

      utils.run(f"git clone {self.source}/{self.pkg}.git", dir=wahooroot, yolo=self.yolo, dont_exit=False, silent=self.silent)
    else:
      cli.echo(f"Source directory for {self.pkg} already exists, skipping clone.", color=wahoo_colors["wahoo_warn"], prefix="wahoo warn")
  
  def build_and_install(self):
    '''
    Build step.

    Flow:
    * stops if self.build is false
    * builds and installs automatically if yolo is on
    * asks the user to build the package without installing
    * build the package without installing then stop
    * otherwise, build and install the package
    '''

    if not self.build:
      return
    
    if self.yolo:
      # assume the user wants to build and install the package (-si)
      cli.echo("Building and installing package...")
      utils.run("makepkg -si --noconfirm", dir=self.sourcedir, yolo=self.yolo, dont_exit=True, silent=self.silent, verbose=self.verbose)
      cli.echo(f"Successfully installed {self.pkg}!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
      return

    if cli.prompt(f"Build {self.pkg} without installing?", use_msg_as_prompt=True, default=False, promptmsg="[y/N]", show_abort_msg=False):
      cli.echo("Building package...")
      utils.run("makepkg -s", dir=self.sourcedir, silent=self.silent, verbose=self.verbose)
      cli.echo(f"{self.pkg} built successfully!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")
      return
        
    cli.echo("Building and installing package...")
    utils.run("makepkg -si", dir=self.sourcedir, silent=self.silent, verbose=self.verbose)
    cli.echo(f"Successfully installed {self.pkg}!", color=wahoo_colors["wahoo_success"], prefix="wahoo!")