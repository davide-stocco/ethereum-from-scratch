---
tier: meta
---

# Ethereum from Scratch

Ethereum is usually explained badly. Most introductions either hand you a metaphor that falls apart the moment you look closely ("it's a world computer!") or drop you straight into Solidity code without saying what the machine underneath is actually doing.

This site tries something different, with two rules.

**Nothing is explained before its prerequisites.** Start at [What is Ethereum?](foundations/what-is-ethereum.md), work down the menu, and each page assumes you've read the ones above it and nothing more.

**Everything here is permanent.** Ethereum upgrades through hard forks, and plenty of tutorials that were accurate when written are now quietly wrong. So this site begins with the part of Ethereum that has **not changed since 2015** — and realistically cannot, because altering any of it would break every wallet, library and deployed contract at once.

That makes for a narrower site than it could be. It's also the part worth learning first.

## How to read a page

The main text of every page is written to be read start to finish with no prior knowledge, and it stands on its own.

Some pages also carry **collapsible boxes**, closed by default, in two kinds:

- **The formal version** — the precise, specification-level statement of what the page just explained in plain language. Exact notation, exact field widths, edge cases.
- **History** — how something used to work, and why it changed. Often the clearest explanation of why the current design is the way it is.

**If you're new to Ethereum, you can leave every one of them closed and lose nothing.** They aren't continuations of the main text, and they're not material you're expected to get through — they're there for readers who want the exact definition or the reasoning behind a decision. Open them when a page leaves you wanting more precision, and ignore them otherwise.

## If a word is unfamiliar

Technical terms are linked the first time each page uses one, and every link does two things:

- **Hover it** and a short definition appears, without leaving the page. Usually that's enough to carry on reading.
- **Click it** and you go to the full entry — either the page that explains the term properly, or the [glossary](glossary.md).

So you need never lose your place to look something up, and you can go deeper when a one-line reminder isn't enough.

The [glossary](glossary.md) also stands alone: it defines every term used anywhere on the site.

---

## Where to start

<div class="grid cards" markdown>

- **[Foundations](foundations/what-is-ethereum.md)**

    What Ethereum actually is — a state machine — plus the units and the number formats you'll meet on every page after this.

- **[Cryptography](crypto/keccak256.md)**

    Hashing, private keys, public keys, and how an address is derived from them. One worked example, carried all the way through.

- **[Encoding](encoding/rlp.md)**

    RLP: how Ethereum turns structured data into bytes, and why it needed its own format rather than using JSON.

- **[Accounts](accounts/accounts.md)**

    The four fields every account has, and why an account-based design needs a nonce when Bitcoin's coin-based design doesn't.

</div>

---

## What's missing, and why

Gas costs, the fee market, transaction types, the EVM, Proof of Stake and rollups aren't here yet. They're all important, and they're all coming.

They're also the parts that **change at hard forks** — so they need a different treatment: numbers kept in one place, pages stamped with the upgrade they were written against, and changes taught as history rather than patched over.

[How this site handles forks](about/forks.md) explains the approach in full.

---

## Who's writing this

I'm **Davide Stocco**, and I'm learning Ethereum — this site is how I'm doing it. My reasoning is that you don't really understand something until you can explain it in an order that makes sense to someone who knows nothing, so instead of taking notes I'm writing the explanation I wanted when I started.

The obvious caveat follows: **this is written by a learner, not an expert.** Pages marked *stub* are outlines I haven't filled in yet, and if you find a mistake I'd genuinely rather know — corrections are the most useful thing you can send me.

[More about me →](about/about-me.md){ .md-button } [My website →](https://sites.google.com/view/davidestocco/){ .md-button }
