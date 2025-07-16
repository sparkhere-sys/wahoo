# Maintainer: Spark <spark-aur@proton.me>
pkgname="wahoo"
pkgver="0.5" # semantic versioning is weird.
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=('x86_64') # sorry ARM users
url="https://github.com/sparkhere-sys/wahoo"
license=('Custom:Modified-MIT') # modified MIT license, no commercial usage clause added
depends=('python>=3.11' 'git' 'bash' 'python-requests' 'python-rapidfuzz' 'sudo')
## source=('wahoo.py' 'LICENSE') # this. single. goddamn. line. this was hell.
# there's no way i can make this work statically unless i do this god forsaken crap you see down there
# im on the verge of crying as i write this
# i tried literally everything
# i feel like learning whatever language makepkg was written in just so i can add support for something like:
## source=('wahoo.py' 'LICENSE' 'wahoo/*')
# i couldn't care less if it breaks arch package guidelines
# I JUST WANT THIS GODFORSAKEN THING TO WORK.
source=('wahoo.py'
        'LICENSE'
        'wahoo/__init__.py'
        'wahoo/cli.py'
        'wahoo/constants.py'
        'wahoo/main.py'
        'wahoo/pacwrap.py'
        'wahoo/parser.py'
        'wahoo/salmon.py'
        'wahoo/utils.py')
# be glad i had the sanity remaining to do this in alphabetical order.
# FIXME: just tar it you dumbass
provides=("$pkgname")
conflicts=('wahoo') # wahoo cannot coexist with another wahoo installation
sha256sums=('3b7bce0f5718919875c2da5566aec859ac11888224ef2ad255e7258ccf6d7885'
            'fb5d9a672ee9f4b5669d263652adaba135ec35ce1d0a693767caa0a8048f930a')

package() {
  pythonver=$(python -c "import sys; print(f'python{sys.version_info.major}.{sys.version_info.minor}')")
  ## pythonver=python3.11
  install -Dm755 "$srcdir/wahoo.py" "$pkgdir/usr/bin/$pkgname"
  ## install -Dm755 "$srcdir/wahoo/salmon.py" "$pkgdir/usr/bin/salmon"
  install -d "$pkgdir/usr/lib/$pythonver/site-packages/wahoo/"
  cp -r "$srcdir/wahoo/"* "$pkgdir/usr/lib/$pythonver/site-packages/wahoo/"
  install -Dm644 "$srcdir/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

# i obviously do not write commit messages when i update the PKGBUILD,
# since it'll just get overwritten by github actions updating it
# i'd keep the "lol" but i don't smile when i edit this stupid file anymore