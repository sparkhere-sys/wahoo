# wahoo! (v0.4 alpha)
a funny AUR helper i made in python :D

this README is informal by design, if you have any questions pull up an issue or contact me

## DISCLAIMER
me and any contributors are NOT responsible if you break your system using wahoo. if you got a complaint, pull up an issue or yell at me about it in my email.

**wahoo is *not* a wrapper for** `pacman` **commands. if you want that, use [archapt](https://github.com/sparkhere-sys/archapt/)**

## available commands
| Command | Aliases | What it does |
|---------|---------|--------------|
| `install` | `-S` | Installs a package from the AUR. |
| `uninstall` | `-R`, `-remove` | Uninstalls a package (AUR or not) |
| `list` | `-Q`, `-Qs` | Lists all your installed ***AUR*** packages. |
| `show` | `-Qi`, `info` | Shows package information for an installed package. |
| `update` | `-Sy` | Updates an AUR package. |
| `search` | `-Ss` | Searches for a package from the AUR. |
| `version` | none :/ | I- What the hell do you want me to say? |
| `help` | none :/ | Again, what the hell do you want me to say? |

### usage
```bash
wahoo install neofetch
wahoo -S neofetch
wahoo uninstall neofetch
```
> Note: Running `wahoo install wahoo` causes a *fake* segmentation fault. `wahoo` didn't actually crash.
>
> This is just an easter egg, so don't email me about this.

## to do for v0.4 stable

- [ ] add coloring with something like `colorama`
- [ ] add an `upgrade` command that updates every AUR package *installed with wahoo* and (maybe as a prompt) runs `pacman -Syu`

## installation
### from source
open up your terminal, then:
```bash
git clone https://github.com/sparkhere-sys/wahoo.git
cd wahoo
makepkg -si
```
you can replace `makepkg -si` with just `makepkg` if you'd like

### with install.sh
run this:
```
curl -fsSL https://raw.githubusercontent.com/sparkhere-sys/wahoo/refs/heads/main/install.sh -o install.sh
chmod +x install.sh
./install.sh
```

### from AUR
soon™️

wait a minute this is an AUR helper-

## updating wahoo
run:
```bash
wahoo update wahoo
```
yeah yeah i know, recursive syntax, but it works

or you can run `./install.sh update` if you have that downloaded

## [contributing](https://github.com/sparkhere-sys/wahoo/blob/main/CONTRIBUTING.md)
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
