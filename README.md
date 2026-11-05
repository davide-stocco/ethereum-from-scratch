> [!IMPORTANT]
> **The site is currently unlisted.** `extra.unlisted: true` in `mkdocs.yml`
> puts a `noindex` tag on every page, so it is readable by anyone with the
> link but kept out of search results. See the publishing checklist below
> before announcing it anywhere.

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
  reference/          # gas costs, fork history  (menu: "Fork-dependent details")
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

---

## Publishing checklist

The site is live but unlisted. Work through this when it's ready to be found.

**1. Make it findable.** Set `extra.unlisted: false` in `mkdocs.yml` and
redeploy. This is the one that matters — leave it `true` and the site stays
invisible to search however long you wait. A forgotten `noindex` is the
standard way a finished site gets no readers.

**2. Submit the sitemap** at `<site>/sitemap.xml` to Google Search Console.
This doesn't *cause* indexing — crawling does that — but it is how you find
out what Google has actually taken, and whether anything is erroring.

**3. Decide about the stubs.** Around twenty pages still say *"Stub — not
written yet"*. Keeping them is defensible: they show the plan, and the notice
is honest. But they will be indexed as thin pages, so either accept that or
trim `nav` to the written pages and restore entries as they're filled in.

**4. Check `site_url`.** It must match where the site actually lives, because
MkDocs uses it for canonical tags and the sitemap. If a custom domain is added
later, this moves with it — otherwise every page tells Google the old address
is the authoritative one.

**5. Grep for internal vocabulary.** Terms invented for maintenance have
reached reader-facing prose three times (`Tier 2`, `Tier 3`, `fork-proof`):

```bash
grep -rn --include="*.md" -E "Tier [0-9]|fork-proof" docs | grep -v "Notes to self"
```

**6. Run the checks.**

```bash
python3 tools/navcheck.py    # every "Next:" link matches the nav order
python3 tools/svgcheck.py    # no diagram text overlapping or off-canvas
mkdocs build --strict        # no broken internal links
```

**If a custom domain is added**, put the domain in `docs/CNAME` rather than
relying on GitHub's settings page. `mkdocs gh-deploy` force-pushes over the
published branch and would delete a `CNAME` written there by the UI; a file in
`docs/` is copied to the site root on every build.
