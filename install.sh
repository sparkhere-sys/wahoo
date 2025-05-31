#!/bin/bash
## auto installs wahoo

set -euo pipefail

wahooroot="$HOME/.wahoo/source/"
localrepo="$wahooroot/wahoo"
mkdir -p "$wahooroot"

depends=("git" "base-devel" "sudo")
repo="https://github.com/sparkhere-sys/wahoo.git"
dir="wahoo"

for dep in "${depends[@]}"; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "wahoo error: Missing dependency: $dep"
    echo "Please install it first."
    exit 1
  fi
done

if [[ "{$1+-}" == "update" ]]; then
  echo "wahoo: Updating wahoo..."
  if [ -d "$localrepo/.git" ]; then
    echo "wahoo: Existing wahoo source found. Updating..."
    cd "$localrepo"
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
  echo "wahoo: Downloading wahoo..."
  git clone "$repo" "$localrepo"
  echo "wahoo: Building and installing wahoo..."
  cd "$localrepo"
  makepkg -si --noconfirm
  echo "wahoo! Successfully installed."
  wahoo version
fi
