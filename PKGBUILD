# Maintainer: Spark <spark-aur@proton.me>
SCRIPTNAME="wahoo.py"
pkgname="wahoo"
pkgver="0.4"
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=("x86_64") # sorry ARM users
url="https://github.com/sparkhere-sys/wahoo"
license=("Custom") # modified MIT license, no commercial usage clause added
depends=("python>=3.11" "git" "bash" "python-requests" "python-rapidfuzz" "sudo")
source=("$SCRIPTNAME" "LICENSE")
provides=("wahoo")
conflicts=('wahoo') # wahoo cannot coexist with another wahoo installation
sha256sums=('b0fb472c56e177906bde630734b6907ef03037a12d9a330aacd51e7185a5ea6a'
            'fb5d9a672ee9f4b5669d263652adaba135ec35ce1d0a693767caa0a8048f930a')

package() {
  install -Dm755 "$srcdir/$SCRIPTNAME" "$pkgdir/usr/bin/wahoo"
  install -Dm644 "$srcdir/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

# i obviously do not write commit messages when i update the PKGBUILD,
# since it'll just get overwritten by github actions updating it lol
