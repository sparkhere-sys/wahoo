# <p align=center>wahoo! v0.4</p>

<p align=center>
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/sparkhere-sys/wahoo/main.yml?branch=main&style=for-the-badge&logo=github-actions&logoColor=black&label=build&labelColor=white&color=%23b7bdf8&link=https%3A%2F%2Fgithub.com%2Fsparkhere-sys%2Fwahoo%2Fblob%2Fmain%2F.github%2Fworkflows%2Fmain.yml">
<img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/sparkhere-sys/wahoo?style=for-the-badge&logo=github&logoColor=black&label=issues&labelColor=white&color=%23f38ba8">
<img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues-pr/sparkhere-sys/wahoo?style=for-the-badge&logo=git&logoColor=black&label=pull%20requests&labelColor=white&color=%23a6e3a1">
</p>

___

<p align=center>yet another AUR helper.</p>

<p align=center>written in python for :sparkles:vibes:sparkles:</p>

___

this README is informal by design, if you have any questions, pull up an issue or contact me.

wahoo isn't intended to be used as a wrapper for pacman. fork it if you want that

roadmap: [click me](./ROADMAP.md)

> [!IMPORTANT]
> me and the contributors are NOT responsible if you break your system using wahoo. that includes the github actions bot. read the [license](./LICENSE), my friend
> 
> if you got a complaint, pull up an [issue](https://github.com/sparkhere-sys/wahoo/issues) or yell at me about it in my [email](mailto:spark-aur@proton.me).
>
> also, any packages you install with wahoo are not under the same license as wahoo unless its explicitly stated. follow others' licenses, please.

## available commands

| Command | Aliases | What it does | Usage |
|---------|---------|--------------|-------|
| `install` | `-S` | Installs a package from the AUR. | `wahoo install foo` |
| `uninstall` | `-R`, `-remove`, `-Rns`, `autoremove` | Uninstalls a package. (this just calls pacman lol) If you run this with `autoremove` or `-Rns` instead, wahoo will use the `--dont-remove-depends` flag. | `wahoo uninstall foo` |
| `list` | `-Q`, `-Qs` | Lists all your installed packages. | `wahoo list`, `wahoo list foo` (which searches for an installed package) |
| `show` | `-Qi`, `info` | Shows package information for an installed package. | `wahoo show foo` |
| `update` | `-Sy` | Updates an AUR package. | `wahoo update foo`, and to update wahoo itself, `wahoo update wahoo` |
| `upgrade` | `-Syu` | Updates all installed AUR packages *installed by wahoo* | `wahoo upgrade` |
| `search` | `-Ss` | Searches for a package from the AUR. | `wahoo search foo` |
| `version` | none :/ | I- What the hell do you want me to say? | `wahoo version` |
| `help` | none :/ | Again, what the hell do you want me to say? | `wahoo help`, will also trigger if you run wahoo with no arguments. |

> Note: Running `wahoo install wahoo` causes a *fake* segmentation fault. `wahoo` didn't actually crash.
>
> This is just an easter egg, so don't email me about this.

### available flags

suggest flags to add [here!](https://github.com/sparkhere-sys/wahoo/issues/1)

| Flag | Aliases | What it does |
|------|---------|--------------|
| `--yolo` | `--noconfirm` | Skips all confirmation prompts. |
| `--dont-remove-depends` | none :/ | Doesn't remove orphaned dependencies when running `wahoo uninstall`. |

## dependencies

- Python 3.11+ (you probably already have this)
- `git`
- `bash`
- `sudo`
- Requests (`python-requests` from pacman)
- Rapidfuzz (`python-rapidfuzz` from pacman)

## installation
### from source
open up your terminal, then:
```bash
git clone https://github.com/sparkhere-sys/wahoo.git
cd wahoo
makepkg -si
```

### with install.sh
run this:
```
curl -fsSL https://raw.githubusercontent.com/sparkhere-sys/wahoo/refs/heads/main/install.sh -o install.sh
chmod +x install.sh
./install.sh
```
or, y'know, just download it.

### from AUR
soon™️

wait a minute this is an AUR helper-

## updating wahoo
run:
```bash
wahoo update wahoo
```
or,
```bash
wahoo -Sy wahoo
```
or you can run `./install.sh update` if you have that downloaded

## why wahoo?

Short answer: Because yes

### the long answer

because wahoo is lightweight, doesn't depend on much, and has *personality*

honestly i wrote this for fun, it doesn't matter to me if you use this or not.

give it a shot and see if it works for you :)

## [contributing](./CONTRIBUTING.md)

if you'd like to contribute, then feel free to do so!
just follow these basic guidelines:

- use pull requests for major changes
- if you're fixing a bug *describe what it did* and *how you fixed it* so everyone can be on the same page
- just don't be a dick, follow the [code of conduct](./CODE_OF_CONDUCT.md)
- (optional) make funny commit messages

# uhhh bye
made with <3 by spark

contact me:

- [my email](mailto:spark-aur@proton.me)
- my discord: **spark-sys**

> [!IMPORTANT]
> 
> Please, for the love of all that is holy, do NOT sell my work.
> 
> I'm fine with you doing anything with my stuff, I won't yell at you.
> 
> But if you are trying to use `wahoo` for commercial purposes then I will have to politely ask you to cease.
>
> Read the [License](./LICENSE), please.
> 
> Bye! :D

___

<p align=center><img alt="License: MIT" src="https://img.shields.io/badge/license-mit-blue?style=for-the-badge&labelColor=white&color=%2374c7ec"></img></p>
