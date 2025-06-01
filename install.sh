#!/bin/bash
## auto installs wahoo

if [[ $EUID -eq 0 ]]; then
  echo "wahoo error: don't run this with sudo, or else makepkg will fail."
  exit 1
fi

if ! curl -s --head https://example.com | grep "200 OK" > /dev/null; then
  echo "wahoo error: No internet. install.sh requires internet in order to install or update wahoo. If you have already cloned wahoo's GitHub repo, then run makepkg there."
  exit
fi

set -euo pipefail

wahooroot="$HOME/.wahoo/source/"
localrepo="$wahooroot/wahoo"
mkdir -p "$wahooroot"

depends=("git" "sudo") # excluding makepkg
repo="https://github.com/sparkhere-sys/wahoo.git"
dir="wahoo"

for dep in "${depends[@]}"; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "wahoo error: Missing dependency: $dep"
    echo "wahoo: Installing $dep..."
    sudo pacman -Sy $dep --noconfirm
    echo "wahoo: $dep installed. Proceeding with installation..."
  fi
done

if ! command -v makepkg &>/dev/null; then
  echo "wahoo error: Missing dependency: makepkg"
  echo "wahoo: Installing base-devel..."
  sudo pacman -Sy base-devel --noconfirm
  echo "wahoo: base-devel installed. Proceeding with installation..."
fi

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
else
  if [ -d "$localrepo" ]; then
    echo "wahoo warn: Existing source directory found. Removing to avoid conflicts..."
    rm -rf "$localrepo/" # scary!
  fi
  echo "wahoo: Downloading wahoo..."
  git clone "$repo" "$localrepo"
  echo "wahoo: Building and installing wahoo..."
  cd "$localrepo"
  makepkg -si --noconfirm
  echo "wahoo! Successfully installed."
  wahoo version
fi
