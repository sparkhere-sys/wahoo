# Maintainer: Spark <spark-aur@proton.me>
pkgname="wahoo"
pkgver="0.5" # semantic versioning is weird.
pkgrel=1
pkgdesc="an AUR helper made in python because why not? made with <3 by spark"
arch=('x86_64') # sorry ARM users
url="https://github.com/sparkhere-sys/wahoo"
license=('Custom:Modified-MIT') # modified MIT license, no commercial usage clause added
depends=('python>=3.11' 'git' 'bash' 'python-requests' 'python-rapidfuzz' 'sudo')
source=("git+${url}.git")
provides=("$pkgname")
## conflicts=('wahoo') # wahoo cannot coexist with another wahoo installation
sha256sums=('SKIP')

package() {
  pythonver=$(python -c "import sys; print(f'python{sys.version_info.major}.{sys.version_info.minor}')")
  ## pythonver=python3.11
  install -Dm755 "$srcdir/wahoo.py" "$pkgdir/usr/bin/$pkgname"
  ## install -Dm755 "$srcdir/wahoo/salmon.py" "$pkgdir/usr/bin/salmon"
  install -d "$pkgdir/usr/lib/$pythonver/site-packages/wahoo/"
  cp -r "$srcdir/wahoo/"* "$pkgdir/usr/lib/$pythonver/site-packages/wahoo/"
  install -Dm644 "$srcdir/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  gzip -f wahoo.1
  install -Dm644 "$srcdir/wahoo.1" "$pkgdir/usr/share/man/man1/wahoo.1.gz"
}

# i obviously do not write commit messages when i update the PKGBUILD,
# since it'll just get overwritten by github actions updating it

# just in case you want to read the old comments,
# here they are!

## # i'd keep the "lol" but i don't smile when i edit this stupid file anymore

### source=('wahoo.py' 'LICENSE') # this. single. goddamn. line. this was hell.
## there's no way i can make this work statically unless i do this god forsaken crap you see down there
## im on the verge of crying as i write this
## i tried literally everything
## i feel like learning whatever language makepkg was written in just so i can add support for something like:
### source=('wahoo.py' 'LICENSE' 'wahoo/*')
## i couldn't care less if it breaks arch package guidelines
## I JUST WANT THIS GODFORSAKEN THING TO WORK.
### source=('wahoo.py'
###         'LICENSE'
###         'wahoo.tar.gz'
###         'wahoo.1')
## i ended up tarring it. i gave up.

## FIXME: we are STILL in checksum hell!!!!!
## makepkg sucks. (good thing its open source so someone smarter than me can make it better)
## point is: when creating wahoo.tar.gz, github actions generated a checksum for *it*,
##           and since the user is expected to create their own tarball,
##           we get checksum mismatches and you have to manually run updpkgsums like a caveman.
## the solution to all this madness?
## just use a git source. and when we get on the AUR, we modify the PKGBUILD. simple as!
## i will not implement this yet (this will probably be in a pull request)
## for now we'll just do a lil' SKIP in the checksums department and disable github actions for a little bit.