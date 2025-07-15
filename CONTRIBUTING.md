# contributing

if you'd like to contribute, feel free to do so!

## guidelines

- **use pull requests** for major changes. *don't just randomly commit to main unless its a small change like fixing a typo.*
- if you're fixing a bug, **_describe_ what it did**, and **_how_ you fixed it** so everyone can be on the same page. *and maybe add comments but thats your call honestly*
- just don't be a dick. the [code of conduct](./CODE_OF_CONDUCT.md) exists for a reason.
- certain lines of code will be commented out with two #s, that is an intentional decision, aka me trying to speedrun coding :)
  you can remove those comments if you like, they are just padding at the end of the day
- (optional) improve the docstrings *just leave my comments alone*
- (optional) make funny commit messages *because we deserve to laugh while we suffer*

## style guide

- use `snake_case` and `snake_case` only, for consistency. (i know its python convention to use `CamelCase` for classes but i dont care)
- use `cli.echo()` instead of raw `print()`
- section headers are in all caps (eg, `# THIS IS A SECTION HEADER`)
- do not use emojis. anywhere. in docstrings, in comments, just please don't.

## exit code guide

- 0: success
- 1: general error
- 2: CLI error
- 3: self-update error
- 4: no internet
- 11: ;) i won't spoil it, its an easter egg

### literally everything else

no idea what happened but it was so catastrophic it exitted with an unidentified exit code.

why?

because python likes making us suffer.

___

thanks for contributing.
