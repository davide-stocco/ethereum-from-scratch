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

## Contents

<div class="grid cards" markdown>

- **Foundations**

    What Ethereum actually is, and the units and number formats you'll meet on every page after it.

    [What is Ethereum?](foundations/what-is-ethereum.md) · [Ether, wei and gwei](foundations/ether.md) · [Hex and bytes](foundations/hex-and-bytes.md)

- **Cryptography**

    Hashing, keys, and how an address is derived from them. One worked example carried all the way through.

    [Keccak-256](crypto/keccak256.md) · [Private keys](crypto/private-keys.md) · [Public keys](crypto/public-keys.md) · [Addresses](crypto/addresses.md) · [Signatures](crypto/signatures.md)

- **Keys and wallets**

    What a wallet actually holds, and why there's no password reset.

    [Wallets and seed phrases](wallets/seed-phrases.md) · [What losing your keys means](wallets/losing-your-keys.md)

- **Accounts and state**

    The four fields every account has, and why an account-based design needs a nonce when Bitcoin's doesn't.

    [Accounts](accounts/accounts.md) · [The nonce](accounts/nonce.md) · [State](accounts/state.md)

- **Encoding**

    How Ethereum turns structured data into bytes, and how it fingerprints the whole state in 32 of them.

    [RLP encoding](encoding/rlp.md) · [The Merkle Patricia Trie](encoding/merkle-patricia-trie.md)

- **Transactions**

    The only way anything ever changes — what's inside one, and what it costs.

    [Transactions](transactions/transactions.md) · [Why metering is necessary](transactions/why-metering.md) · [Gas](transactions/gas.md) · [Fees](transactions/fees.md)

- **Blocks**

    How transactions get bundled, chained, and occasionally un-chained.

    [Blocks](blocks/blocks.md) · [The block header](blocks/block-header.md) · [The chain and reorgs](blocks/the-chain.md)

- **Economics**

    Why running this costs anything, who ends up paying, and what capping a supply buys and costs.

    [Why security has to be paid for](economics/security-budget.md) · [Who pays](economics/who-pays.md) · [Fixed cap or flexible supply](economics/supply-cap.md)

</div>

Also: a [glossary](glossary.md) of every term used on the site, and a [reference](reference/gas-costs.md) section holding the numbers that change at upgrades.

---

## Reading paths

The menu is one sensible order, and reading straight down it works. But depending on why you're here, some of it can wait.

**New to Ethereum — read in order.** Start at [What is Ethereum?](foundations/what-is-ethereum.md) and work down. Nothing assumes anything you haven't already read.

**Here for the economics.** The monetary and incentive questions need surprisingly little machinery — just what Ethereum is and what the units are:

> [What is Ethereum?](foundations/what-is-ethereum.md) → [Ether, wei and gwei](foundations/ether.md) → [Why security has to be paid for](economics/security-budget.md) → [Who pays](economics/who-pays.md) → [Fixed cap or flexible supply](economics/supply-cap.md)

Cryptography, encoding and accounts can be skipped and picked up later.

**Here for the technical detail.** Work down Foundations, Cryptography, Accounts and Encoding in order. These are the parts that haven't changed since 2015, so they're worth learning properly once.

**Looking for one specific thing.** Use the search box, or the [glossary](glossary.md) for a quick definition with a link to the page that explains it.

??? note "Why there's no choice to make up front"

    Some sites ask you to pick a track before you begin. This one doesn't,
    because the economics genuinely depends on the technical material — you
    can't weigh what security *costs* without knowing what it *buys* — so the
    paths overlap rather than diverge. There's one set of pages, and these are
    just suggested routes through them.

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
