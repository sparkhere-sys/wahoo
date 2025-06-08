# Maintainer: Spark <spark-aur@proton.me>
SCRIPTNAME=wahoo.py
pkgname=wahoo
pkgver=0.4 # early alpha
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=("x86_64")
url="https://github.com/sparkhere-sys/wahoo"
license=("Custom")
depends=("python>=3.10" "git" "bash" "python-requests" "sudo")
source=("$SCRIPTNAME" "LICENSE")
provides=("$pkgname") # no kidding sherlock
sha256sums=("SKIP" "SKIP") # checksums in v1.0 i promise

package() {
  install -Dm755 "$srcdir/$SCRIPTNAME" "$pkgdir/usr/bin/wahoo"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
