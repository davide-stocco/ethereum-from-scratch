# Ethereum from Scratch

How Ethereum works, built up from first principles — written while I learn it myself.

**Live site:** not published yet — the repository is private while the first pages are written. It will go live at <https://davide-stocco.github.io/ethereum-from-scratch/>

Most Ethereum introductions either give you a metaphor that collapses under inspection or drop you into Solidity without explaining the machine underneath. This site is built on two rules instead.

**Nothing is explained before its prerequisites.** The ordering is the actual work — see [ROADMAP.md](ROADMAP.md).

**Phase 1 covers only what has never changed.** Ethereum upgrades through hard forks, and plenty of tutorials that were correct when written are now quietly wrong. So the published site starts with the part of Ethereum that has been stable since 2015 and realistically cannot change: hashing, keys, addresses, RLP, units, and the account model. Fork-dependent material waits in `drafts/` until it can be handled properly. See [FORKS.md](FORKS.md).

## Built with

- [MkDocs](https://www.mkdocs.org/) with [Material](https://squidfunk.github.io/mkdocs-material/) — content is plain Markdown, output is static HTML
- Hosted free on GitHub Pages

## Running it locally

```bash
# one-time setup
python3 -m pip install mkdocs-material

# start a local server with live reload
python3 -m mkdocs serve
```

Then open <http://127.0.0.1:8000>. Edit any file in `docs/`, save, and the browser refreshes itself.

## Publishing

```bash
python3 -m mkdocs gh-deploy
```

Builds the site and pushes it to the `gh-pages` branch, which GitHub Pages serves. The `main` branch stays clean Markdown.

## Layout

```
mkdocs.yml          # config — the nav section defines page order
ROADMAP.md          # what's written, what's next, in what order
FORKS.md            # which pages are fork-proof, and the maintenance policy
docs/               # the published site
  index.md
  foundations/      # what Ethereum is, units, hex and bytes
  crypto/           # keccak, private keys, public keys, addresses
  encoding/         # RLP
  accounts/         # accounts, the nonce
  about/            # how this site handles forks
drafts/             # fork-dependent stubs, not published yet
```

## Corrections

If you find a mistake, please open an issue. I'm learning this as I write it, and I'd rather be corrected than confidently wrong.
