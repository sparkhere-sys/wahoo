# Maintainer: Spark <spark-aur@proton.me>
SCRIPTNAME=wahoo.py
pkgname=wahoo
pkgver=0.4
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=("x86_64") # sorry ARM users
url="https://github.com/sparkhere-sys/wahoo"
license=("Custom") # modified MIT license, no commercial usage clause added
depends=("python>=3.11" "git" "bash" "python-requests" "python-rapidfuzz" "sudo")
source=("$SCRIPTNAME" "LICENSE")
provides=("wahoo")
sha256sums=('4dc6991561c03bfe2591cda9ccf5200964e46b24f0ca3610dadf2ebd363061ea'
            'fb5d9a672ee9f4b5669d263652adaba135ec35ce1d0a693767caa0a8048f930a')

package() {
  install -Dm755 "$srcdir/$SCRIPTNAME" "$pkgdir/usr/bin/wahoo"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

# i obviously do not write commit messages when i update the PKGBUILD, since it'll just get overwritten by github actions updating it lol
