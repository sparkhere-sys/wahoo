# Maintainer: Spark <spark-aur@proton.me>
SCRIPTNAME=main.py
pkgname=wahoo
pkgver=0.0.2
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=("x86_64")
url="https://github.com/sparkhere-sys/wahoo"
license=("Modified-MIT")
depends=("python>=3.10" "git" "makepkg")
source=("$SCRIPTNAME" "LICENSE.md")
provides=("wahoo") # no shit sherlock
sha256sums=("SKIP") # im sorry

package() {
  install -Dm755 "$srcdir/$SCRIPTNAME" "$pkgdir/usr/bin/wahoo"
  install -Dm644 LICENSE.md "$pkgdir/usr/share/licenses/$pkgname/LICENSE.md"
}
