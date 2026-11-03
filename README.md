# Ethereum from Scratch

How Ethereum works, built up from first principles — written while I learn it myself.

**Live site:** not published yet — the repository is private while the first pages are written. It will go live at <https://davide-stocco.github.io/ethereum-from-scratch/>

Most Ethereum introductions either give you a metaphor that collapses under inspection or drop you into Solidity without explaining the machine underneath. This site is built on two rules instead.

**Nothing is explained before its prerequisites.** The ordering is the actual work — see [ROADMAP.md](ROADMAP.md).

**It starts with what has never changed.** Ethereum upgrades through hard forks, and plenty of tutorials that were correct when written are now quietly wrong. So the first pages written are the ones that cannot go stale: hashing, keys, addresses, signatures, units, and the account model. Fork-dependent pages are scaffolded but carry date stamps, and every number that a fork can change lives in one place rather than scattered through the prose. See [FORKS.md](FORKS.md).

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
mkdocs.yml            # config — the nav section defines reading order
ROADMAP.md            # what's written, what's next, and every convention
FORKS.md              # which pages a fork can invalidate, and the policy

docs/
  index.md
  foundations/        # what Ethereum is, units, hex and bytes
  crypto/             # keccak, keys, addresses, signatures
  wallets/            # seed phrases, losing your keys
  accounts/           # accounts, the nonce, state
  encoding/           # RLP, the Merkle Patricia Trie
  transactions/       # transactions, metering, gas, fees
  blocks/             # blocks, the header, the chain
  economics/          # the security budget, who pays, supply
  reference/          # gas costs, fork history  (menu: "Costs and upgrades")
  about/              # the fork policy, who's writing this
  glossary.md

  javascripts/        # the interactive tools — no dependencies, plain JS
  stylesheets/        # one file of overrides on the Material theme
```

Every page carries a `tier:` in its frontmatter — `1` for fork-proof, `2` and
`3` for pages an upgrade can invalidate. That makes the post-fork review
mechanical: `grep -rl "^tier: 3" docs/`.

## Corrections

If you find a mistake, please open an issue. I'm learning this as I write it, and I'd rather be corrected than confidently wrong.
