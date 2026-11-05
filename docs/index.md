---
tier: meta
---

# Ethereum from Scratch

Ethereum is usually explained badly. Most introductions either hand you a metaphor that falls apart the moment you look closely ("it's a world computer!") or drop you straight into Solidity code without saying what the machine underneath is actually doing.

This site tries something different, with two rules.

**Nothing is explained before its prerequisites.** Start at [What is Ethereum?](foundations/what-is-ethereum.md), work down, and each page assumes you've read the ones above it and nothing more. The site is in **seven parts** for that reason — the order is the argument.

**Everything here is permanent.** Ethereum upgrades through hard forks, and plenty of tutorials that were accurate when written are now quietly wrong. So this site begins with the part of Ethereum that has **not changed since 2015** — and realistically cannot, because altering any of it would break every wallet, library and deployed contract at once.

That makes for a narrower site than it could be. It's also the part worth learning first.

## How to read a page

The main text of every page is written to be read start to finish with no prior knowledge, and it stands on its own.

**Every page opens by saying whether it can go out of date.** Ethereum is upgraded every so often, and some of what's true today won't be in five years. So each page says up front whether what follows is **permanent** or has parts that move — and that label links to [the full explanation](about/forks.md) of how this site handles it. Where a page says permanent, you can trust it without checking the date on anything.

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

Seven parts, in order. Each assumes the ones before it and nothing else.

Each part is named for the question it answers, and in order they make a sentence:

> **what it is → who can act → where it runs → what it holds → how it changes → when it's settled → why anyone bothers**

That's the whole site in a line. The topic names under each card are what the material is called elsewhere, in case you're looking for something specific.

<div class="grid cards" markdown>

- **Part 1 · What it is**

    What Ethereum actually is, the units it counts in, and the two tools every later page leans on — how bytes are written, and how they're fingerprinted.

    [What is Ethereum?](foundations/what-is-ethereum.md) · [Ether, wei and gwei](foundations/ether.md) · [Hex and bytes](foundations/hex-and-bytes.md) · [Keccak-256](crypto/keccak256.md)

- **Part 2 · Who can act**

    How control is proved: a secret number, the one-way chain that turns it into an address, and what holding the only copy means.

    *Cryptography* — [Private keys](crypto/private-keys.md) · [Public keys](crypto/public-keys.md) · [Addresses](crypto/addresses.md) · [Signatures](crypto/signatures.md)

    *Wallets* — [Seed phrases](wallets/seed-phrases.md) · [What losing your keys means](wallets/losing-your-keys.md)

- **Part 3 · Where it runs**

    The machines that hold all this and check every block for themselves — what they are, what software they run, and what it takes to be one.

    [What a node is](nodes/what-a-node-is.md) · [Clients and the two layers](nodes/clients-and-layers.md) · [Running one yourself](nodes/running-one.md)

- **Part 4 · What it holds**

    Everything every node stores, how much of it everyone else can see, and how one 32-byte number commits to all of it.

    *Accounts and state* — [Accounts](accounts/accounts.md) · [The nonce](accounts/nonce.md) · [State](accounts/state.md) · [Why accounts, and what they cost](accounts/why-accounts.md) · [What it reveals](accounts/what-it-reveals.md)

    *Contracts* — [What a smart contract is](contracts/smart-contracts.md)

    *How it's written* — [RLP encoding](encoding/rlp.md) · [The Merkle Patricia Trie](encoding/merkle-patricia-trie.md)

- **Part 5 · How it changes**

    The only way anything ever happens: what's inside a transaction, why the work has to be metered, and what it costs.

    [Transactions](transactions/transactions.md) · [Why metering is necessary](transactions/why-metering.md) · [Gas](transactions/gas.md) · [Fees](transactions/fees.md) · [Gas costs](reference/gas-costs.md)

- **Part 6 · When it's settled**

    How changes get batched and chained, who gets to propose one and why anybody must, and what "confirmed" is actually worth.

    [Blocks](blocks/blocks.md) · [The block header](blocks/block-header.md) · [Why somebody has to be chosen](blocks/why-somebody-chosen.md) · [Proof of stake](blocks/proof-of-stake.md) · [The chain and reorgs](blocks/the-chain.md)

- **Part 7 · Why anyone bothers**

    What keeping this running costs, who ends up paying, what capping a supply buys — and who gets to decide any of it when nobody is in charge.

    [Why security has to be paid for](economics/security-budget.md) · [Who pays](economics/who-pays.md) · [Fixed cap or flexible supply](economics/supply-cap.md) · [Who decides, when nobody is in charge](economics/governance.md)

</div>

Then two things that sit outside the reading path: a [glossary](glossary.md) defining every term used anywhere on the site, and **about** — [how upgrades are handled](about/forks.md), [what each one did](reference/fork-history.md), and [who's writing this](about/about-me.md).

---

## Reading paths

Straight through, part by part, is the order the site is built for. But depending on why you're here, some of it can wait.

**New to Ethereum — read in order.** Start at [What is Ethereum?](foundations/what-is-ethereum.md) and work down. Nothing assumes anything you haven't already read.

**Here for the economics.** The monetary and incentive questions need surprisingly little machinery — just what Ethereum is and what the units are:

> [What is Ethereum?](foundations/what-is-ethereum.md) → [Ether, wei and gwei](foundations/ether.md) → [Why security has to be paid for](economics/security-budget.md) → [Who pays](economics/who-pays.md) → [Fixed cap or flexible supply](economics/supply-cap.md)

Parts 2 to 6 can wait, and picking them up later costs nothing.

**Here for the technical detail.** Parts 1 to 4, in order. That's nearly everything on the site that has not changed since 2015 — so it's worth learning properly once rather than twice.

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
