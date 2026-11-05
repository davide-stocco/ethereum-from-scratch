---
tier: 1
description: A node is a computer that holds the state and checks every block against the rules itself — which is what makes trusting anyone unnecessary.
---

# What a node is

**[Permanent](../about/forks.md).** What a node does, and why checking rather than trusting is the whole point, follows from the design and has not changed. The software it runs, and what it costs, are the next two pages.

!!! definition "Node"

    A computer running Ethereum's rules. It keeps its own copy of the
    **state**, receives **blocks** from other computers, applies each block's
    transactions to its own copy, and **rejects any block that breaks the
    rules**.

    It holds no keys, signs nothing, and is paid nothing. Those are different
    jobs, done by different things.

This part comes early on purpose. It would read better after [state](../accounts/state.md) and [blocks](../blocks/blocks.md), whose detail makes the argument sharper — but **"node" is load-bearing from the [signatures](../crypto/signatures.md) page onward**, and a word the site leans on repeatedly cannot stay undefined that long.

So it borrows two things from later and states them plainly: the **state** is the record of every account and what it holds, and a **block** is a batch of transactions added to the chain as one unit. Both were introduced on [What is Ethereum?](../foundations/what-is-ethereum.md). Everything else here is built on what you already have.

## What a node actually does

Four steps, repeated indefinitely.

1. **Receive** a block from another computer.
2. **Check** it — are the signatures valid, the nonces in order, the balances sufficient, the rules followed?
3. **Apply** its transactions to its own copy of the state, in the order the block gives.
4. **Keep it, or throw it away.** A block that breaks any rule is rejected outright. Not flagged, not reported to anybody. Discarded.

That is the entire job. The interesting part is what *isn't* in the list: at no point does the node ask another computer whether the block is good. There is nobody to ask, and asking would defeat the point.

<svg viewBox="0 0 470 258" role="img" aria-label="One block is sent to three independent nodes. Each applies the rules to its own copy of the state and computes a state root. All three roots are identical, and no node consulted another." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="8" y="98" width="88" height="56" rx="5"/><rect x="178" y="14" width="192" height="60" rx="5"/><rect x="178" y="96" width="192" height="60" rx="5"/><rect x="178" y="178" width="192" height="60" rx="5"/><path d="M96 126 L136 126 L136 44 L170 44"/><path d="M96 126 L170 126"/><path d="M96 126 L136 126 L136 208 L170 208"/></g><g fill="currentColor" stroke="none"><path d="M170 39 L180 44 L170 49 Z"/><path d="M170 121 L180 126 L170 131 Z"/><path d="M170 203 L180 208 L170 213 Z"/><text x="52" y="122" font-size="11" text-anchor="middle" font-weight="700">one block</text><text x="52" y="138" font-size="9" text-anchor="middle" opacity="0.75">of transactions</text><text x="190" y="34" font-size="11" font-weight="700">node</text><text x="190" y="50" font-size="9" opacity="0.8">applies the rules to its own state</text><text x="190" y="66" font-size="10" font-family="monospace">root 3a7f&#8230;c91</text><text x="190" y="116" font-size="11" font-weight="700">node</text><text x="190" y="132" font-size="9" opacity="0.8">applies the rules to its own state</text><text x="190" y="148" font-size="10" font-family="monospace">root 3a7f&#8230;c91</text><text x="190" y="198" font-size="11" font-weight="700">node</text><text x="190" y="214" font-size="9" opacity="0.8">applies the rules to its own state</text><text x="190" y="230" font-size="10" font-family="monospace">root 3a7f&#8230;c91</text><text x="382" y="122" font-size="9" opacity="0.75">&#8230; and</text><text x="382" y="134" font-size="9" opacity="0.75">thousands</text><text x="382" y="146" font-size="9" opacity="0.75">more</text><text x="8" y="256" font-size="10" opacity="0.85">Same block, same starting state, same rules &#8212; so the same answer. None asked the others.</text></g></svg>

The three results match because the rules are deterministic, which is the property the [state machine](../foundations/what-is-ethereum.md) page opened with. A node doesn't *discover* that it agrees with everyone else. It computes the only answer the rules allow, and therefore agrees by construction.

## What it refuses to do

The shortest accurate description of a node:

> **A machine that refuses to take anybody's word for anything.**

Every other property follows. It won't accept a balance it was told — it computes balances. It won't accept that a block is valid because a well-known company says so — it checks. It won't accept a chain because that chain arrived first — it applies the rules and sees what survives.

This is what the site has meant, page after page, by *nobody has to trust anybody*. It isn't a claim about people being honest. It's a claim about a particular computer in a particular room being able to **redo the work** — which means the number of such computers is the extent to which the claim is true at all.

## Node, validator, miner, wallet

The distinction most worth getting straight, because nearly all confusion about "who runs Ethereum" is one of these four mistaken for another.

| | What it does | Paid? | Holds keys? |
| --- | --- | --- | --- |
| **Node** | checks blocks, keeps the state | **no** | no |
| **Validator** | proposes blocks and votes on others' | **yes** | yes, staking keys |
| **Miner** | the pre-2022 name for that paid role | yes | yes |
| **Wallet** | holds your keys, builds transactions | no | **yes, yours** |

Three things fall out of that table.

**Nodes are unpaid.** No reward, no registration, and nothing in the protocol that knows you exist. This surprises people, and it's why [what it costs](running-one.md) gets a page of its own.

**A validator is a node plus a job.** It must run a node — you cannot vote on the validity of blocks you haven't checked — and then additionally proposes and attests, for which it is paid and for which it stakes something it can lose. So **every validator is a node; almost no node is a validator.**

**"Miner" is a historical word.** Mining was the paid proposing role under the old consensus rules, retired in 2022. Meeting it in current writing means the author means a validator, or is working from old material.

**A wallet is none of the above.** It holds keys, as the [wallets](../wallets/seed-phrases.md) section laboured, and usually keeps no copy of the state at all — it asks somebody else's node. Which is worth sitting with: **most people using Ethereum are trusting a node they don't run.**

??? question "So who gets to propose a block, and when?"

    Deliberately not answered here. That's the **consensus mechanism** —
    [proof of stake](../glossary.md#proof-of-stake) — and it needs its own
    treatment.

    The reason it can wait is that nothing on this page depends on it. The
    checking role is identical under any consensus rule: receive, verify,
    apply, keep or reject. Change how proposers are chosen and every sentence
    above still holds — a good sign the two subjects separate cleanly.

## Where blocks come from

There is no server. Worth saying flatly, because "connecting to Ethereum" sounds like connecting to *something*, and there is nothing there to connect to.

A node connects to a handful of other nodes — **peers** — which are connected to further nodes. Blocks and transactions are passed along those links, each node forwarding to its neighbours, until they've reached everybody. The pattern is called **gossip**, and the word is apt: no announcement, no central source, just repetition until the news is everywhere. Bitcoin's design paper sets out the same arrangement [(Nakamoto, 2008)](#ref-nakamoto-2008), and Ethereum inherits it.

Two consequences:

**Nobody is authoritative.** A node cannot ask "what is the real chain?", because no computer holds that position. It can only apply the rules to what reaches it.

**And there is nothing to switch off.** No operator, no address, no company — which is the practical content of a claim that otherwise sounds like a slogan.

## Each node has its own waiting room

Transactions arrive by gossip too, and one that's been broadcast but not yet included has to wait somewhere. That somewhere is the **mempool** — and the thing to notice is that **it is per-node, not shared.**

There is no single queue. Each node keeps its own set of pending transactions, decides how many to hold and for how long, and may discard yours while another keeps it. This is why the [nonce](../accounts/nonce.md) page could say clients differ in what they'll hold onto, and why a transaction can appear to vanish and then come back: it was never in one place to begin with.

## Catching up

A node starting today has to get from the first block to the present, and that's the slow part — hours at best.

What makes it slow is the arithmetic, not the download. Having the blocks is not the same as having the state: the state is the *result* of applying every transaction ever sent, so a node arriving late must either redo that work or obtain the current state and check it against the chain. **How much history you re-derive is the choice being made**, and it's the distinction [state](../accounts/state.md) draws between history and state.

## If nobody pays them, why does anyone run one?

The honest answer is narrower than the usual one.

**To avoid trusting somebody else's answer.** That's the whole return, and for some parties it plainly covers the cost: an exchange that must be certain of its own deposits, a wallet provider serving millions of lookups, anyone building something where being lied to about the chain is expensive.

For an individual it's thinner. You get certainty that nobody is misreporting your balance, and you stop revealing which addresses you care about to whoever's node you were querying. Real, but modest against an always-on machine with a lot of disk.

Which is exactly why **the number of nodes is watched, and why the cost of running one is a question about the system rather than about your hardware.** If running a node becomes impractical for everyone but large operators, nothing in the rules changes — but *anybody can check for themselves* quietly becomes *anybody with a datacentre can*, and the property that made trust unnecessary ends up resting on fewer and fewer people. [Running one yourself](running-one.md) takes that apart.

### Not every node keeps everything

Which raises a fair question: if catching up means obtaining all that, why don't nodes simply keep it? Many don't, and the reasoning is worth knowing.

**They always drop the oldest, never a selection.** The data a node keeps has to run contiguously backwards from the present, because checking block N requires the state left by block N−1. A node holding a scattered sample of past blocks could do nothing with it. So the only decision is *how far back*, and it's set by whoever runs the node — nothing in the protocol says.

Recency wins because of what each part is *for*. The **current state** is the only thing required to validate new blocks. A **short recent window** is needed in case the tip of the chain changes and work has to be rewound. **Everything older** answers questions about the past, and nothing else.

And discarding it is safe for the same reason the state root works:

> **A node can safely forget anything it can re-obtain and re-verify.**

Old blocks are linked by hash, so a node needing one later asks a peer and checks that what arrives matches what the chain already commits to. No trust required — a lie is detectable. **Verification doesn't require possession**, which is also why a new node can accept a state it was handed and check it against the root instead of replaying years of transactions.

So the trade is never about how much a node can *verify*; it's about which questions it can answer. **Pruning costs you memory, not judgement.**

The catch is collective. If everybody prunes, the history is gone from the network — nobody's copy means nobody's copy. That is exactly the question **EIP-4444** [(Kadianakis et al., 2021)](#ref-eip4444) raises by proposing that clients stop serving old history: it makes keeping it somebody's explicit job rather than an accident of everyone's defaults. [State](../accounts/state.md) sets out the three sizes of node this produces.

---

## Recap

- A node keeps its own copy of the **state**, applies arriving blocks to it, and **rejects** anything breaking the rules [(Wood, 2014)](#ref-wood-2014).
- It never asks another computer whether a block is valid. **Same block, same starting state, same rules, same answer** — agreement by construction, not by consultation.
- Shortest description: **a machine that refuses to take anybody's word for anything.** Every other property follows.
- **Nodes are unpaid and unregistered.** A **validator** is a node plus a paid job, so every validator is a node and almost no node is a validator. **Miner** is the pre-2022 word for that job. A **wallet** is neither — it holds keys and usually asks someone else's node.
- Blocks arrive by **gossip** from a few peers. No server, nobody authoritative, nothing to switch off.
- The **mempool is per-node**, not a shared queue — which is why pending transactions behave inconsistently.
- **Catching up is slow** because the state has to be re-derived or verified, not merely downloaded.
- Many nodes keep only recent data, always dropping the oldest, because **anything re-obtainable and hash-checkable is safe to forget.** Pruning costs you memory, not judgement — though if everybody prunes, the history is gone.
- Nobody pays you to run one. The return is **not having to trust anybody's answer** — and how many people find that worth paying for decides whether the whole arrangement means anything.

**Next:** [Clients and the two layers](clients-and-layers.md) — the software that does all this, and why there are two pieces of it.

---

## References

<div class="sources" markdown>

- <a id="ref-eip4444"></a>**Kadianakis, G., lightclient, & Stokes, A.** (2021). *EIP-4444: Bound Historical Data in Execution Clients.* Ethereum Improvement Proposals. Proposes that clients stop serving block bodies and receipts past a cutoff, which turns history retention from a default into a deliberate role. <https://eips.ethereum.org/EIPS/eip-4444>
- <a id="ref-nakamoto-2008"></a>**Nakamoto, S.** (2008). *Bitcoin: A peer-to-peer electronic cash system.* Sets out the peer-to-peer broadcast arrangement Ethereum inherits, and the principle of accepting the result of applying rules rather than the word of any participant. <https://bitcoin.org/bitcoin.pdf>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Defines the block-level state transition function every node applies independently, and the conditions a block must satisfy to be accepted. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
