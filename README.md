# wahoo! (v0.3 beta)
a funny AUR helper i made in python :D

this README is informal by design, if you have any questions pull up an issue or contact me

## DISCLAIMER
wahoo is still in early development. im not responsible if you break your system using this.

**wahoo is NOT intended to be used as an alias for `pacman` commands. if you want that, use [archapt](https://github.com/sparkhere-sys/archapt/)**

## available commands
- `install` (aliases: `-S`)
- `uninstall` (aliases: `-R`, `remove`)
- `list` (aliases: `-Q`, `-Qs`)
- `show` (aliases: `info`, `-Qi`)
- `update` (aliases: `-Sy`)
- `version`
- `help` (aliases: `-H`, `--help`) (before you ask, `--help` isn't recognized as a flag by wahoo's code. deal with it)

### usage
```bash
wahoo install neofetch
wahoo -S neofetch
wahoo uninstall neofetch
```

## to do for v0.0.3
things that are done will be ~~crossed out~~

- ~~add `list` and `show` commands~~
- add flags
- ~~create install.sh~~

## installation
### with install.sh
run this:
```
curl -fsSL https://raw.githubusercontent.com/sparkhere-sys/wahoo/refs/heads/main/install.sh | bash
```

### from source
open up your terminal, then:
```bash
git clone https://github.com/sparkhere-sys/wahoo.git
cd wahoo
makepkg -si
```
you can replace `makepkg -si` with just `makepkg` if you'd like

### from AUR
soon™️

wait a minute this is an AUR helper-

## updating wahoo
run:
```bash
wahoo update wahoo
```
yeah yeah i know, recursive syntax, but it works

or you can run `./install.sh update`

## contributing
if you'd like to contribute, then feel free to do so!
just follow these basic guidelines:

- use pull requests like a normal human being
- if you're fixing a bug *describe what it did* and *how you fixed it* so everyone can be on the same page
- just don't be a dick, follow the [code of conduct](https://github.com/sparkhere-sys/wahoo/blob/main/CODE_OF_CONDUCT.md)
- remember that this has the [MIT license](https://github.com/sparkhere-sys/wahoo/blob/main/LICENSE). modified sure, but its the MIT license.

# uhhh bye
made with <3 by spark

contact me:

- [my email](mailto:spark-aur@proton.me)
- my discord: **spark-sys**

> I think its important to mention this:
> 
> Please, for the love of all that is holy, do NOT sell my work.
> 
> I'm fine with you doing anything with my stuff, I won't yell at you.
> 
> But if you are trying to use `wahoo` for commercial purposes then I will have to politely ask you to cease.
> 
> Bye! :D
