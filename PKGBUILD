# Maintainer: Spark <spark-aur@proton.me>
pythonver=$(python3 -c "import sys; print(f'python{sys.version_info.major}.{sys.version_info.minor}')")
pkgname="wahoo"
pkgver="0.5" # semantic versioning is weird.
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=('x86_64') # sorry ARM users
url="https://github.com/sparkhere-sys/wahoo"
license=('Custom:Modified-MIT') # modified MIT license, no commercial usage clause added
depends=('python>=3.11' 'git' 'bash' 'python-requests' 'python-rapidfuzz' 'sudo')
source=('wahoo.py' 'LICENSE')
provides=("$pkgname")
conflicts=('wahoo') # wahoo cannot coexist with another wahoo installation
sha256sums=('4a207130ccf2a9e23181029da26975ffb36c737048e76fdf466d2ce13b0b9a90'
            'fb5d9a672ee9f4b5669d263652adaba135ec35ce1d0a693767caa0a8048f930a')

package() {
  install -Dm755 "$srcdir/wahoo.py" "$pkgdir/usr/bin/$pkgname"
  install -Dm755 "$srcdir/wahoo/salmon.py" "$pkgdir/usr/bin/salmon"
  install -d "$pkgdir/usr/lib/$pythonver/site-packages"
  cp -r "$srcdir/wahoo/" "$pkgdir/usr/lib/$pythonver/site-packages/"
  install -Dm644 "$srcdir/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

# i obviously do not write commit messages when i update the PKGBUILD,
# since it'll just get overwritten by github actions updating it lol
