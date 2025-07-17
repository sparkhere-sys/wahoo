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
        'wahoo.tar.gz')
# i ended up tarring it. i gave up.
provides=("$pkgname")
conflicts=('wahoo') # wahoo cannot coexist with another wahoo installation
sha256sums=('c1823bb0eb6a121de5e24c222db870ae47f8a5a4f9cfc7d27fd3708a61edd80c'
            'fb5d9a672ee9f4b5669d263652adaba135ec35ce1d0a693767caa0a8048f930a'
            'e4d511c99476b2a87b3dba39ad98ad45d8334a2da68fe4297cbf4d220f175fa3')

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
