# Maintainer: Spark <spark-aur@proton.me>
SCRIPTNAME=main.py
pkgname=wahoo
pkgver=0.0.3-alpha
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=("x86_64")
url="https://github.com/sparkhere-sys/wahoo"
license=("Modified-MIT")
depends=("python>=3.10" "git" "bash" "python-requests")
source=("$SCRIPTNAME" "LICENSE")
provides=("$pkgname") # no shit sherlock
sha256sums=("SKIP") # im sorry

package() {
  install -Dm755 "$srcdir/$SCRIPTNAME" "$pkgdir/usr/bin/wahoo"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
