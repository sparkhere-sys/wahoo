# Maintainer: Spark <spark-aur@proton.me>
SCRIPTNAME=wahoo.py
pkgname=wahoo-dev
pkgver=0.4
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=("x86_64") # sorry ARM users
url="https://github.com/sparkhere-sys/wahoo"
license=("Custom") # modified MIT license, no commercial usage clause added
depends=("python>=3.11" "git" "bash" "python-requests" "python-rapidfuzz" "sudo")
source=("$SCRIPTNAME" "LICENSE")
provides=("wahoo")
sha256sums=('1ed9ecb97727157033f7d84bb927dd3ffa2c1bc36d9202b11289df869cd646e5'
            '5185e0b407183c9879d4cda5a6c2db8b442616ec4bf3a654c5cb3da68ce92404')

package() {
  install -Dm755 "$srcdir/$SCRIPTNAME" "$pkgdir/usr/bin/wahoo"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

# i obviously do not write commit messages when i update the PKGBUILD, since it'll just get overwritten by github actions updating it lol
