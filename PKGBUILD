# Maintainer: Spark <spark-aur@proton.me>
pkgname="wahoo"
pkgver="0.6" # semantic versioning is weird.
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=('x86_64') # sorry ARM users
url="https://github.com/sparkhere-sys/wahoo"
license=('Apache')
depends=('python>=3.11' 'git' 'bash' 'python-requests' 'python-rapidfuzz' 'sudo')
source=("git+${url}.git")
## provides=("$pkgname") # useless (thank you for telling me this archwiki)
## conflicts=('wahoo') # wahoo cannot coexist with another wahoo installation
sha256sums=('SKIP')

package() {
  pythonver=$(python -c "import sys; print(f'python{sys.version_info.major}.{sys.version_info.minor}')")
  ## pythonver=python3.11
  install -Dm755 "$srcdir/wahoo/wahoo.py" "$pkgdir/usr/bin/$pkgname"
  ## install -Dm755 "$srcdir/wahoo/salmon.py" "$pkgdir/usr/bin/salmon"

  install -d "$pkgdir/usr/lib/$pythonver/site-packages/" # just in case
  cp -r "$srcdir/wahoo/wahoo" "$pkgdir/usr/lib/$pythonver/site-packages/"

  install -Dm644 "$srcdir/wahoo/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"

  gzip -f "$srcdir/wahoo/wahoo.1"
  install -Dm644 "$srcdir/wahoo/wahoo.1.gz" "$pkgdir/usr/share/man/man1/wahoo.1.gz"
}