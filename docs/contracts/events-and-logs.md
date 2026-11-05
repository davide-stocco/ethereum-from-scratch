---
tier: 1
description: A log is the one thing a contract can write and never read — a record for the outside world, deliberately kept out of the state.
---

# Events and logs

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**[Permanent](../about/forks.md).** The structure of logs, and the rule that contracts cannot read them, have not changed since 2015.

## The thesis this page exists to argue

Everything else a contract touches, it can touch both ways: it writes storage and reads storage, sends ether and reads its balance. **Logs are the exception, and the asymmetry is the design.**

A contract can emit a log and can never read one — not its own, not any other contract's. Logs are not part of the [state](../accounts/state.md). They are written for the benefit of things outside Ethereum, and that is precisely why they are cheap: no node needs them available in order to execute anything.

So logs are the seam between a system that must be internally reproducible and a world that wants to watch it.

## Questions this page should answer

- What is a log, concretely? (A record attached to a transaction's result rather than to the state: an address, up to four indexed **topics**, and a lump of unindexed data.)
- Why can't a contract read them? (**The central question.** Because a node is not required to keep them. If execution could depend on logs, every node would need all logs forever in order to compute anything — which is exactly the cost the design avoids by putting them outside the state.)
- What's the difference between an *event* and a *log*? (A log is the protocol-level thing. An "event" is the source-language construct that compiles into one — the same relationship as a function and its selector. Worth stating, because the words get used interchangeably.)
- Why are they cheap? (They are never read by the machine, so they impose no permanent lookup cost on anybody. The price reflects that, and this is the clearest example on the site of **cost following structure** rather than convention.)
- How does anybody find a log among millions of blocks? (Each block header carries a **bloom filter** — a compact summary that can say *definitely not here* but only *possibly here*. Letting a searcher skip almost every block is what makes log queries practical. This is the page where that trick gets explained, and [the block header](../blocks/block-header.md) can point back.)
- What are **topics** for, and why only a few? (Indexing. The first topic is conventionally the hash of the event's signature, the same Keccak trick as a [function selector](smart-contracts.md). The limit is a cost decision — indexing is what makes search cheap, so it is rationed.)
- What are logs actually used for? (Wallets showing your token transfers, explorers, anything off-chain that reacts to on-chain activity. Also the only practical answer to *how often has this contract been used* — see the previous page's three counting methods.)
- What can't you rely on? (A contract may do something and emit nothing. Logs record what an author chose to announce, which is **not the same as what happened** — the trap the counting section already flags.)

## Notes to self

- Lead with the asymmetry — write but never read. Everything else on the page follows from it, including the price.
- The **bloom filter** is the best piece of machinery here and it is genuinely elegant: a structure that is allowed to say "maybe" in one direction and never in the other. Explain what that buys rather than how the bits are set.
- Resist drifting into how applications use logs. The protocol-level facts are permanent; the tooling is not.
- Worth the honest closing note: logs look like a record of events and are really a **record of announcements**. Anyone using them as data should know the difference.

**Next:** [Tokens aren't special](tokens.md) — what you actually own when you own one.
