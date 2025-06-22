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
sha256sums=('17e51536e40dc509ce57cfb1a0e134af7d9511a937aa4e49cbdb83a18e2e977b'
            '5185e0b407183c9879d4cda5a6c2db8b442616ec4bf3a654c5cb3da68ce92404')

package() {
  install -Dm755 "$srcdir/$SCRIPTNAME" "$pkgdir/usr/bin/wahoo"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

# i obviously do not write commit messages when i update the PKGBUILD, since it'll just get overwritten by github actions updating it lol
