# Maintainer: Spark <spark-aur@proton.me>
pkgname=wahoo
pkgver=0.0.1
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=("x86_64")
url="https://github.com/sparkhere-sys/wahoo"
license=("MIT")
depends=("python<=3.10")
source=("core.py") # for now. wahoo will be expanded later so this line will be updated
sha256sums=("SKIP") # im sorry

package() {
  install -Dm755 "$srcdir/$source" "$pkgdir/usr/bin/wahoo"
}
