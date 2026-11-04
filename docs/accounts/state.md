---
tier: 2
description: The state is every account and what it holds — kept by each node, never carried in a block, and committed to by one 32-byte number.
---

# State

**Fork-proof in substance.** That the state is a mapping from addresses to accounts, and that each block commits to it with a single root, has held since genesis. The *structure* producing that root is the part under active replacement.

!!! info "Current as of Fusaka (December 2025)"

    Nothing here has changed in Ethereum's lifetime. The long-running proposals
    to replace the structure behind the state root — and to let untouched state
    expire — would change the *mechanism* without changing what the root
    promises. None has shipped. [How this site handles forks](../about/forks.md).

!!! definition "State"

    The complete set of **every account and what it holds** — each
    [address](../crypto/addresses.md) paired with its four fields.

    It is **not** stored in the blocks. Every node keeps its own copy and
    updates it as blocks arrive. What a block carries is a **state root**: one
    32-byte fingerprint of the whole state, which lets every node check that
    its copy matches everybody else's.

## The state is one enormous mapping

Nothing more structurally complicated than a dictionary. The key is an address; the value is the four fields the [accounts](accounts.md) page laid out.

```
0x7E5F…95Bdf  →  nonce 3   balance 1500000000000000000   (no code)
0xd8dA…96045  →  nonce 847 balance 2000000000000000      (no code)
0xA0b8…eB48   →  nonce 1   balance 0    code, and storage
      ⋮
```

Hundreds of millions of entries, and that's the lot. Ask "what is Ethereum's state?" and the honest answer is *that table, as it stands right now.*

Two things follow immediately, and both matter more than they look.

**The state has no history in it.** It says 0x7E5F has sent three transactions. It does not say when, to whom, or what they were. It is a snapshot, not a record.

**The state is the only thing you need to go on.** To check whether a new transaction is valid, a node needs balances and nonces — which are in the state. It does not need to know how those values came about.

## The state is not in the blocks

This is the misconception worth killing early, because almost everyone arrives with it.

A block does **not** contain the state. It contains **transactions** — instructions — and each node applies them to the copy of the state it already has. The state is the *result* of running every block ever produced, and it lives on each node's disk, not on the chain.

Which raises the obvious problem. If every node computes the state privately, how does anyone know they all got the same answer? Thousands of independent machines, each with their own copy, each claiming it's correct.

They could exchange their copies and compare. That would work and is completely impractical: the state is measured in hundreds of gigabytes, so agreeing on every balance by sending every balance around is not a mechanism, it's a bandwidth bill. *(No figure is given here on purpose — it's a moving target, and any number printed on this page would be wrong within months.)*

## The state root

So they do the other thing. Each block header carries a single 32-byte value — the **state root** — which is a fingerprint of the entire state after that block's transactions have been applied [(Wood, 2014)](#ref-wood-2014).

<svg viewBox="0 0 470 280" role="img" aria-label="A small block header box contains a 32-byte state root. An arrow leads from it to a large box representing the whole state, holding hundreds of millions of accounts. The 32 bytes commit to all of it, so changing any single value anywhere changes the root." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="10" y="26" width="164" height="96" rx="5"/><rect x="22" y="72" width="140" height="38" rx="4" opacity="0.6"/><rect x="258" y="26" width="202" height="190" rx="5" stroke-dasharray="5 4"/><rect x="272" y="62" width="174" height="26" rx="3"/><rect x="272" y="94" width="174" height="26" rx="3"/><rect x="272" y="126" width="174" height="26" rx="3"/><path d="M174 91 L248 91"/></g><g fill="currentColor" stroke="none"><path d="M248 86 L258 91 L248 96 Z"/><text x="22" y="48" font-size="11" font-weight="700">block header</text><text x="22" y="64" font-size="9" opacity="0.75">a few hundred bytes</text><text x="32" y="90" font-size="11">stateRoot</text><text x="32" y="104" font-size="9" opacity="0.8">32 bytes</text><text x="270" y="48" font-size="11" font-weight="700">the state</text><text x="356" y="48" font-size="9" opacity="0.75">hundreds of gigabytes</text><text x="282" y="79" font-size="10">one account&#8217;s four fields</text><text x="282" y="111" font-size="10">another account</text><text x="282" y="143" font-size="10">another account</text><text x="282" y="172" font-size="10" opacity="0.7">&#8230; hundreds of millions more</text><text x="272" y="200" font-size="9" opacity="0.75">none of this is in the block</text><text x="10" y="244" font-size="10" opacity="0.85">Change one wei in one account and the root changes completely. So two</text><text x="10" y="258" font-size="10" opacity="0.85">nodes agreeing on 32 bytes agree on every balance, every nonce, and</text><text x="10" y="272" font-size="10" opacity="0.85">every byte of every contract&#8217;s storage.</text></g></svg>

That last sentence is the whole trick, and it's worth saying twice. **Two nodes that agree on 32 bytes agree on everything.** Comparing state becomes comparing one short number, because the fingerprint depends on every byte beneath it — alter a single wei in a single account and the root is unrecognisable, exactly as the [Keccak-256](../crypto/keccak256.md) page described.

So a node's procedure on receiving a block is:

1. Apply the block's transactions to its own copy of the state.
2. Compute the root of the result.
3. Compare with the root in the block's header.

Match, and it has independently confirmed that its state is identical to the proposer's — every account, without having seen any of theirs. Mismatch, and it rejects the block. **It never has to trust the state it was handed, because it never was handed any.**

??? abstract "Why a plain hash of the whole state wouldn't do"

    A fair question: hash the lot and you get 32 bytes, so why does the next
    section need a special structure?

    Because of what the root is asked to do besides matching.

    **It must be cheap to update.** A node applies a block, changing perhaps a
    few hundred accounts out of hundreds of millions. Re-hashing the entire
    state for each block would be absurd. The real structure lets a change be
    pushed up one path, touching a handful of values.

    **It must support proofs about parts.** Somebody should be able to prove
    *"this account holds this balance"* against the root, without presenting
    the whole state. A flat hash can't: the only way to verify it is to have
    all the data, which defeats the point for anyone running a light client.

    Both needs point to the same answer — a tree of hashes, where each node
    commits to its children. That's the [Merkle Patricia
    Trie](../encoding/merkle-patricia-trie.md), and it gets its own page.

## Storage is a state inside the state

An account's `storageRoot` is where this turns recursive, and it's neater than it first sounds.

A contract's **storage** is its own private mapping: 32-byte keys, called **slots**, to 32-byte values. Nothing else can read or write it directly — only the contract's own code, which is why the [accounts](accounts.md) page could say storage without code never occurs.

```
slot 0x00…00  →  0x00…0539    (say, a stored number)
slot 0x00…01  →  0x00…7E5F…   (say, an address)
      ⋮
```

That mapping is fingerprinted exactly the way the whole state is — same structure, same guarantees — and the resulting root is what sits in the account's `storageRoot` field. So:

- the **state root** commits to every account,
- and each account's **storage root** commits to every slot that account holds.

A tree of accounts, where some leaves carry a tree of their own. Change one slot in one contract and that contract's storage root changes, so that account's entry changes, so the state root changes. **One 32-byte number at the top is a statement about every stored value on Ethereum.**

??? note "Storage keys get hashed too, for the same reason addresses do"

    The state is keyed by `keccak256(address)` rather than the address, as the
    [accounts](accounts.md) page explained, so nobody can choose where in the
    structure their account lands.

    Storage does the same: the trie is keyed by `keccak256(slot)`. And here the
    defence matters *more*, not less. An address takes work to grind; a slot
    number is simply a number a contract writes to, free to choose outright. If
    raw slots were keys, a contract could write to a million slots sharing a
    long prefix and make its own storage pathologically deep for everybody
    storing it.

## State and history are different things

Both get called "the blockchain", and separating them explains what a node actually keeps.

- **History** is the chain of blocks: every transaction ever sent, in order. It only gets added to.
- **State** is where that history has left things. It gets *rewritten* constantly.

History is a recording. State is the current position. And the surprising part:

> You can throw away the history and keep using the chain. You cannot throw away the state.

To validate the next block, a node needs balances, nonces, code and storage — all present-tense, all in the state. It does not need last year's transactions. They produced the state it's holding, and having done so, they are no longer load-bearing.

This isn't a thought experiment. **EIP-4444** [(Kadianakis et al., 2021)](#ref-eip4444) proposes exactly it: execution clients stop serving and may delete block bodies and receipts past a cutoff, keeping the chain fully functional. That the proposal is even coherent is the clearest evidence the two things are separable.

Hence the kinds of node you'll meet, which are differences in **how much history** is retained:

| | Keeps | Can tell you |
| --- | --- | --- |
| **Archive** | state at every past block | what your balance was two years ago |
| **Full** | current state, plus enough history to re-derive | everything, but old queries need recomputation |
| **Pruned** | current state, little history | the present, authoritatively |

All three validate new blocks identically, because all three hold the current state. The difference is only what questions about the past they can answer.

??? question "So is Ethereum's data permanent or not?"

    Both, in different senses, and the distinction is worth having because the
    word *immutable* gets used far too loosely.

    **What cannot be altered** is the history, by anyone, because every block
    commits to the one before it. Nobody can quietly rewrite a transaction from
    2017.

    **What is not guaranteed to be retained** is a copy of it on any particular
    machine. Pruning is a local choice about disk, not a change to the chain.
    The data is immutable; your access to it depends on somebody having kept it.

    So "stored on the blockchain forever" is two claims wearing one coat: *it
    can't be changed* is a protocol guarantee, while *it will always be
    available to you* is a bet on other people's storage.

## The state only grows

One closing fact with consequences all over the rest of the site.

**Nothing removes an account.** A balance can fall to zero, a contract can become useless, a key can be lost — and the entry stays, because the protocol has no notion of state going out of date. The only deletions in Ethereum's history were the narrow cleanup of genuinely empty accounts that the [accounts](accounts.md) page described.

So the state rises monotonically, every node stores all of it, and the requirement to run one rises with it. That is the **state growth** problem, and it isn't a bug anybody introduced — it's a direct consequence of having chosen accounts, which [the next page](why-accounts.md) takes apart properly. Responses fall into three classes: charging **rent** for state you occupy, letting untouched state **expire**, and **statelessness** — arranging that validators needn't hold the state at all. Which, if any, ships is exactly the kind of thing this page's date stamp is for.

---

## Recap

- The state is a **mapping from every address to its four fields** — a snapshot of the present, containing no history.
- **Blocks don't contain the state.** They contain transactions; each node applies them to its own copy.
- Each block header carries a **state root**: 32 bytes fingerprinting the whole state. **Two nodes agreeing on it agree on everything.**
- A node applies a block, computes the root, and compares. So it verifies the state **without ever being sent any**.
- A plain hash wouldn't work: the root must be cheap to update and must support proofs about parts. Both need a tree — the [Merkle Patricia Trie](../encoding/merkle-patricia-trie.md).
- **Storage nests the same idea**: each contract's slots have their own root, which sits in its account entry.
- Storage keys are hashed like addresses, and the defence matters more there, because a contract picks its slot numbers freely.
- **History can be discarded; state cannot.** Nodes differ in how much history they keep, not in whether they hold the state.
- *Immutable* conflates two claims: the data can't be changed, but your access depends on somebody retaining it.
- **The state only ever grows**, because nothing expires. That's the price of accounts.

**Next:** [Why accounts, and what they cost](why-accounts.md) — the trade this whole section has been describing.

---

## References

<div class="sources" markdown>

- <a id="ref-eip4444"></a>**Kadianakis, G., lightclient, & Stokes, A.** (2021). *EIP-4444: Bound Historical Data in Execution Clients.* Ethereum Improvement Proposals. Proposes that clients stop serving and may prune block bodies and receipts past a cutoff — which is only coherent because state and history are separable. <https://eips.ethereum.org/EIPS/eip-4444>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Defines the world state as a mapping from addresses to account states, and the state root as the header field committing to it. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
