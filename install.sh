#!/bin/bash
## auto installs wahoo

if [[ $EUID -eq 0 ]]; then
  echo "wahoo error: don't run this with sudo, or else makepkg will fail."
  exit 1
fi

set -euo pipefail

wahooroot="$HOME/.wahoo/source/"
localrepo="$wahooroot/wahoo"
mkdir -p "$wahooroot"

depends=("git" "makepkg" "sudo")
repo="https://github.com/sparkhere-sys/wahoo.git"
dir="wahoo"

for dep in "${depends[@]}"; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "wahoo error: Missing dependency: $dep"
    echo "Please install it first."
    exit 1
  fi
done

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
    rm -rf "$localrepo" # scary!
  fi
  echo "wahoo: Downloading wahoo..."
  git clone "$repo" "$localrepo"
  echo "wahoo: Building and installing wahoo..."
  cd "$localrepo"
  makepkg -si --noconfirm
  echo "wahoo! Successfully installed."
  wahoo version
fi
