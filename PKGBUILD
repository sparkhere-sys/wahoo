# Maintainer: Spark <spark-aur@proton.me>
SCRIPTNAME=wahoo.py
pkgname=wahoo-dev
pkgver=0.4
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=("x86_64") # sorry ARM users
url="https://github.com/sparkhere-sys/wahoo"
license=("Custom") # modified MIT license, no commercial usage clause added
depends=("python>=3.10" "git" "bash" "python-requests" "python-rapidfuzz" "sudo")
source=("$SCRIPTNAME" "LICENSE")
provides=("wahoo")
sha256sums=('83621217653de8547a5e4f55d78405f6559b27b18710fbbf1a7567476a04f37c'
            '7d58c0581544a88060b883012151056fb309da2dc74eaa2ee5de2b57c0897029')

package() {
  install -Dm755 "$srcdir/$SCRIPTNAME" "$pkgdir/usr/bin/wahoo"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

# i obviously do not write commit messages when i update the PKGBUILD, since it'll just get overwritten by github actions updating it lol
