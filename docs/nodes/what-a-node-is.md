---
tier: 1
description: A node is a computer that holds the state and checks every block against the rules itself — which is what makes trusting anyone unnecessary.
---

# What a node is

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**[Permanent](../about/forks.md).** What a node does, and why checking rather than trusting is the whole point, follows from the design and has not changed. The *software*, and what it costs to run, are the next two pages.

This part comes early on purpose. It would read better after [state](../accounts/state.md) and [blocks](../blocks/blocks.md), whose detail makes the argument sharper — but **"node" is load-bearing from the [signatures](../crypto/signatures.md) page onward**, and a word the site leans on repeatedly cannot stay undefined that long.

So this part borrows two things from later and states them plainly, exactly as the state page borrows four facts about blocks: the **state** is the record of every account, and a **block** is a batch of transactions added to the chain as one unit. Both were introduced on [What is Ethereum?](../foundations/what-is-ethereum.md). Everything else here is built on what you already have.

## Why this page exists at all

The word **node** appears on nearly every page of this site, and until now nothing defined it. Worse, several arguments lean on it hard: the [state](../accounts/state.md) page's entire case is that each node computes the state privately and compares one 32-byte number, and the [determinism](../foundations/what-is-ethereum.md) argument is about thousands of them reaching identical answers. The reader has been asked to accept a load-bearing word on trust.

## Questions this page should answer

- What is a node, concretely? (A computer running software that holds a copy of the [state](../accounts/state.md), receives blocks, applies them to its own copy, and rejects any that don't follow the rules.)
- What does "validating for yourself" actually buy? (The thing the whole site keeps asserting: you need not trust anybody, because you recompute the answer. This is the page where that stops being a slogan.)
- What does a node *not* do? (It doesn't hold your keys, doesn't sign anything, and isn't paid. Those are separate roles — see below.)
- Where does it get blocks from? (Other nodes. Peer-to-peer gossip, no central server, no canonical source — worth saying plainly, since "connecting to Ethereum" sounds like connecting to something.)
- What is the **mempool**, and why is it per-node rather than a shared thing? (Each node keeps its own set of broadcast-but-not-included transactions, which is why the [nonce](../accounts/nonce.md) page can say clients differ in what they'll hold.)
- **Node, validator, miner, wallet — which is which?** (The one most worth getting straight. A node checks; a validator proposes and attests and is paid; a wallet holds keys. One machine can do several, and the words get used interchangeably by people who should know better.)
- How does a new node catch up? (Syncing: it has to get from genesis to now. The *how* is implementation, but that it must happen, and that it's the slow part, is worth stating.)
- If nodes are unpaid, why does anyone run one? (Honest answer: to not have to trust somebody else's answer. Which is a real reason for exchanges, wallet providers and anyone building — and a thin one for most individuals, which is exactly why the count matters and is watched.)

## Notes to self

- **Don't duplicate the node-type table.** [State](../accounts/state.md) distinguishes archive, full and pruned as a point about *history versus state* — and now comes **after** this page, so mention that nodes differ in how much history they keep and promise the distinction rather than making it here.
- The **node/validator distinction** is the single most clarifying thing here, in the same way "only an EOA can start a transaction" was on the accounts page. Give it room. Most confusion about "who runs Ethereum" is this distinction missing.
- Resist explaining Proof of Stake. Who gets to propose a block, and when, is the consensus mechanism, and it needs its own treatment. This page is about the *checking* role, which is the same under any consensus rule.
- Keep client names out of this page entirely — they belong on the next one, and they date.
- The strongest framing: **a node is a machine that refuses to take anybody's word for anything.** Every other property follows from that.
- Likely diagram: one block arriving at several independent nodes, each applying it to its own state and computing the same root — the picture the state page argues in prose.

**Next:** [Clients and the two layers](clients-and-layers.md) — the software that does all this, and why there are two pieces of it.
