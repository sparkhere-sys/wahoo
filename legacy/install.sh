#!/bin/bash

## wahoo! install.sh
## v1.0 (yes the install.sh is on a different version than the python script, deal with it)
## installs and updates wahoo

# TODO: add ansi colors to the output

# HACK: currently the whole self-updater is being outsourced to this script (it would be awkward to update it while its running)
#       but this does have its downsides, since this isn't installed when you just casually run `makepkg`
#       i *could* put this in the PKGBUILD, but im not really sure.

echo "WARNING"
echo "wahoo's install.sh has been deprecated in favor of salmon.py (for self-updating)"
echo "continue at your own risk."
sleep 2

if [[ $EUID -eq 0 ]]; then
  echo "wahoo error: don't run this as root, or else makepkg will fail."
  exit 1
fi

if ! curl --silent --fail --head https://archlinux.org > /dev/null; then
  echo "wahoo error: No internet. install.sh requires internet in order to install or update wahoo. If you have already cloned wahoo's GitHub repo, then run makepkg there."
  exit 1
fi

set -euo pipefail

wahooroot="$HOME/.wahoo/source/"
localrepo="$wahooroot/wahoo" # don't even think about making this root.
mkdir -p "$wahooroot"

repo="https://github.com/sparkhere-sys/wahoo.git"
dir="wahoo"
countdown=5

if [[ "${1-}" == "update" ]]; then
  echo "wahoo: Updating wahoo..."
  if [ -d "$localrepo/.git" ]; then
    echo "wahoo: Existing wahoo source found. Updating..."
    cd "$localrepo"
    git reset --hard HEAD
    git pull
    echo "wahoo! Pulled from the latest commit."
  else
    echo "wahoo: Cloning wahoo repo..."
    git clone "$repo" "$localrepo"
    echo "wahoo! Successfully cloned repo."
  fi
  
  echo "wahoo: Removing old wahoo package (if installed)"
  sudo pacman -R --noconfirm wahoo || true
  echo "wahoo: Building and installing wahoo..."
  cd "$localrepo"
  makepkg -si --noconfirm
  echo "wahoo! Successfully updated wahoo."
  wahoo version
else
  if [[ -d "$localrepo" && "$localrepo" != "/" ]]; then # safeguard
    echo "wahoo warn: Existing source directory found. Removing to avoid conflicts..."
    echo "wahoo: Clearing old directory in 5 seconds. Press Ctrl+C to interrupt."
    
    while [ $countdown -gt 0 ]; do
      echo "$countdown"
      sleep 1
      countdown=$((countdown - 1))
    done
    
    rm -rf "$localrepo" # scary!
  fi
  
  echo "wahoo: Downloading wahoo..."
  git clone "$repo" "$localrepo"
  echo "wahoo: Building and installing wahoo..."
  cd "$localrepo"
  makepkg -si --noconfirm
  echo "wahoo! Successfully installed."
  if command -v wahoo > /dev/null; then
    wahoo version
  else
    echo "wahoo: Restart your shell to use wahoo."
  fi
fi
