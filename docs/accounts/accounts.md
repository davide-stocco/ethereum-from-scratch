---
tier: 2
description: An account is an entry in Ethereum's state with four fields. There are two kinds, and only one of them can start anything.
---

# Accounts

**Fork-proof in its essentials.** The four fields have been the same since genesis. The clean split between the two *kinds* of account is the part that has started to soften.

!!! info "Current as of Fusaka (December 2025)"

    The four fields and the "only an EOA can start a transaction" rule are
    unchanged since 2015. **EIP-7702**, which shipped with Pectra in May 2025,
    weakened the distinction between the two kinds — explained in its own box
    below. Nothing in Fusaka touched accounts.

    If you're reading much later, check [how this site handles
    forks](../about/forks.md).

!!! definition "Account"

    An **entry in Ethereum's state**, looked up by a 20-byte
    [address](../crypto/addresses.md), holding exactly four fields: a
    **nonce**, a **balance**, a **storage root** and a **code hash**.

    Two kinds exist. An **EOA** — externally owned account — is controlled by
    whoever holds the matching [private key](../crypto/private-keys.md). A
    **contract account** is controlled by its own code.

    The address is how you find the account, not something the account stores.

## An account is an entry, not an object

Start here, because the word misleads. "Opening an account" is a thing you do at a bank: an application, an approval, a record created in your name. None of that has an equivalent here.

The [addresses](../crypto/addresses.md) page established that **nothing creates an address** — all 2<sup>160</sup> exist already, and a wallet simply derives one. Accounts work the same way. An account isn't created; it **begins to be recorded** the first time there is something to record about it.

So an address nobody has ever used is not in the state at all. Not stored as a row of zeros — absent. And that is indistinguishable from an account that holds nothing, which is the point: a balance of zero and no stored entry describe exactly the same situation. Ask a node for the balance of an address never touched and it answers zero, because that is the correct answer, not because it found a record saying so.

??? abstract "Which makes \"empty\" a surprisingly awkward category"

    Worth a look, because it's a case where a tidy idea needed patching.

    Early on it was possible to create entries that existed in the state while
    holding nothing — send zero ether to an untouched address and you'd get a
    record with a zero balance, a zero nonce and no code. Functionally
    identical to absence, but occupying space, and millions were created
    cheaply as a result.

    **EIP-161** [(Wood, 2016)](#ref-eip161) dealt with it in Spurious Dragon
    (2016) by deleting such accounts at the end of any transaction that
    touched them, so that "holds nothing" and "isn't recorded" converged again.

    The reason this is more than trivia: it shows the state is a thing somebody
    pays to store, and that storing nothing has to cost nothing or the
    accounting breaks. That pressure reappears constantly once you reach
    [gas](../transactions/gas.md).

## The four fields

Every account, of either kind, holds these and nothing else [(Wood, 2014)](#ref-wood-2014):

| Field | What it holds | Size |
| --- | --- | --- |
| `nonce` | How many transactions this account has sent — or, for a contract, how many contracts it has created | integer |
| `balance` | Ether owned, in [wei](../foundations/ether.md) | integer |
| `storageRoot` | A fingerprint of everything the account has in storage | 32 bytes |
| `codeHash` | A fingerprint of the account's code | 32 bytes |

Two of those are plain numbers. The [nonce](nonce.md) is a counter with its own page next, and the balance is a whole number of wei, exactly as the [ether](../foundations/ether.md) page insisted.

The other two are the ones that needed groundwork, so here it is.

### The two fingerprints

A contract can hold a great deal: thousands of stored values, and a program of some size. Neither is in the account entry. What the account holds is a **hash of each** — the kind of fingerprint the [Keccak-256](../crypto/keccak256.md) page described, where any change to the data produces a completely different output.

That buys a specific thing. The account entry stays a fixed, small size no matter how much the contract stores, while still **committing** to every byte of it: you cannot alter one stored value without changing the `storageRoot`, and you cannot change the code without changing the `codeHash`. So a 32-byte field stands in for unbounded data and remains an exact statement about it.

**What a hash of a *collection* is, exactly**, is the part being deferred. Hashing one lump of bytes is simple. Hashing a mapping of thousands of keys and values — such that you can prove one entry belongs without presenting the rest — needs a structure, and that structure is the [Merkle Patricia Trie](../encoding/merkle-patricia-trie.md). It gets its own page. For now: a fingerprint exists, and nothing can change underneath it unnoticed.

An account with no storage and no code still has both fields. They hold the fingerprints of emptiness, which are two fixed constants you'll meet again:

```
codeHash     c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
storageRoot  56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421
```

The first is Keccak-256 of nothing at all — the empty-input hash the Keccak page used to check its own implementation. The second is the root of an empty trie. Every ordinary wallet account on Ethereum carries that identical pair.

## Two kinds, told apart by one field

Both kinds are 20-byte addresses and look identical written down. The [addresses](../crypto/addresses.md) page made that point: nothing in an address reveals which kind it is.

The difference is in the account, and it is one field:

| | EOA | Contract account |
| --- | --- | --- |
| Controlled by | whoever holds the private key | its own code |
| `codeHash` | the empty-input hash above | the hash of its code |
| Created by | deriving an address from a key — nothing is recorded until it's used | a transaction that deploys code |
| Can start a transaction | **yes** | **no** |
| Can hold ether | yes | yes |
| Has a nonce | yes — transactions sent | yes — contracts created |

**So "does this account have code?" is the whole test**, and it's a comparison against a constant. There is no field declaring a type, and no flag to set. The kind of account is a consequence of what it holds rather than a property it was assigned.

??? abstract "Why there's no \"type\" field — or an owner, or a name"

    Four fields is a strikingly short list. It's worth asking what *isn't*
    there, because each absence is deliberate.

    **No type.** It would be redundant, and redundancy in consensus data is a
    liability: two fields that can disagree need a rule for which one wins.
    Deriving the type from `codeHash` makes disagreement impossible.

    **No owner.** For a contract there is nothing to put — control is whatever
    the code says, which might be one key, five keys, a vote, or nobody. For an
    EOA it would be the public key, and that is exactly what the address
    already commits to.

    **No name, no creation date, no history.** The state answers *what is true
    now*, and nothing else. How an account reached its current contents is
    recoverable from the chain of blocks, so storing it in the state would mean
    every node keeping a second copy of something it already has.

    The pattern is worth noticing because it recurs: **the state holds the
    minimum from which everything else can be derived.** Anything inferable is
    left out, and storing it anyway would only create a way for a node to be
    wrong.

## Only an EOA can start anything

This is the single most clarifying fact about how Ethereum runs, and it is routinely assumed to work the other way.

**Nothing on Ethereum happens by itself.** There are no timers, no scheduled jobs, no background processes. A contract cannot wake up at midnight, cannot poll a price, cannot check whether a deadline has passed. It has no thread of its own and no way to acquire one.

A contract's code runs only when something **calls** it. Follow any chain of calls back far enough and it begins in the same place: a transaction, signed by a private key, from an EOA. Contracts can call other contracts, and a single transaction can touch dozens of them — but every one of those calls descends from one signature at the root.

The reasons it must be this way:

- **Somebody has to pay.** Execution is metered, and the fee comes from the account that sent the transaction. Self-starting code would be work with no payer.
- **Somebody has to be the cause.** Every node must reach the same result, which means they must all run the same operations in the same order. Spontaneous execution would need agreement on *when* it fired — and the network has no shared clock to agree with.

??? question "Then how do things that look automatic work?"

    They aren't automatic. Somebody is sending transactions.

    A contract that "liquidates positions when the price drops" has a function
    anybody may call, which checks the price and acts if the condition holds.
    It sits inert until called. What makes it feel automatic is that the
    function **pays whoever calls it** — so people run software watching for
    the condition, racing to call it first and collect.

    That pattern has a name: **keepers**, or bots. The automation is economic,
    not technical. The protocol provides no scheduling; a reward provides the
    incentive, and competing outsiders provide the labour.

    Which is why "it executes automatically" is a claim worth examining
    whenever you meet it. Usually the honest version is *somebody is paid to
    make it execute, and so far somebody has*. If the reward stops covering
    the fee, the automation quietly stops.

??? warning "One thing here is changing: EIP-7702"

    The rule above holds. The clean *statement* of it doesn't, quite.

    **EIP-7702** [(Buterin et al., 2024)](#ref-eip7702), live since Pectra in
    May 2025, lets an EOA set its `codeHash` to point at contract code. So
    "EOAs have no code" is no longer strictly true, and the tidy
    codeHash-is-the-test rule now has an exception.

    What it is for: giving ordinary wallets abilities that previously required
    moving to a contract account — batching several actions into one
    transaction, letting somebody else pay your fee, setting spending
    permissions. The same goals ERC-4337
    [(Buterin et al., 2021)](#ref-erc4337) pursues as a layer on top.

    What it does **not** change: an EOA still needs a key to authorise
    anything, and transactions still originate only from EOAs. The two rules
    this page rests on survive. What's blurring is the clean taxonomy — which
    is why this page sits at Tier 2 and why that taxonomy is worth holding
    loosely.

??? question "So is an account the same thing as a wallet?"

    No, and the words get used interchangeably constantly.

    - An **account** is the entry in the state. It exists whether or not any
      software knows about it.
    - A **[wallet](../wallets/seed-phrases.md)** is the program on your
      device. It holds keys and builds transactions, and Ethereum has never
      heard of it.
    - An **EOA** is an account whose key some wallet happens to hold.

    So "my wallet has three accounts" means one piece of software holding keys
    for three addresses. The accounts aren't *in* the wallet, and losing the
    wallet doesn't touch them — as the [previous page](../wallets/losing-your-keys.md)
    laboured.

    The confusion is harmless in conversation and becomes a problem the moment
    you read a specification, where "account" never once means "app".

## Why this design needs a nonce

One consequence, to set up the next page.

Ethereum records **balances**, where Bitcoin records individual coins. The [state machine](../foundations/what-is-ethereum.md) page covered the comparison and [Buterin (2014)](#ref-buterin-2014) argues the case at length. Here is the cost of the choice.

A Bitcoin transaction consumes specific coins. Try to submit it twice and the second attempt fails on its own terms — the coins it names are already gone, so the transaction is not merely disallowed but meaningless. The protection is a property of the thing being spent.

An account has no such property. "Send 1 ether from A to B" doesn't name anything that gets used up. It is a valid instruction before it executes and an equally valid instruction afterwards, because A's balance is just a number and the instruction never referred to a particular part of it. A signed transaction would be a **reusable cheque**: anybody who saw it could submit it again, and every copy would verify perfectly.

So the protection has to be added, and it is added as a counter. That's the [nonce](nonce.md).

---

## Recap

- An account is an **entry in the state**, looked up by address. Nothing creates it; it begins to be recorded when there is something to record.
- An unused address isn't stored as zeros — it's **absent**, which is indistinguishable from holding nothing.
- Every account has exactly four fields: **nonce, balance, storageRoot, codeHash.** The address isn't one of them.
- The last two are **fingerprints**, so a fixed-size entry commits to unbounded storage and code. The structure making that possible is the [Merkle Patricia Trie](../encoding/merkle-patricia-trie.md).
- An account with neither carries the two constants for empty — `c5d2…a470` and `56e8…b421`.
- **Two kinds, distinguished by `codeHash` alone.** No type field exists, because the type is derivable.
- **Only an EOA can start a transaction.** No timers, no scheduled jobs. Everything that looks automatic is somebody being paid to send a transaction.
- **EIP-7702 has begun blurring the EOA/contract split**, without changing either rule this page relies on.
- Balances aren't consumable the way coins are, so replay protection has to be supplied separately — by the **nonce**.

**Next:** [The nonce](nonce.md) — the counter that stops a signed transaction being reused.

---

## References

<div class="sources" markdown>

- <a id="ref-erc4337"></a>**Buterin, V., Weiss, Y., Tirosh, D., Nacson, S., Forshtat, A., Gazso, K., & Hess, T.** (2021). *ERC-4337: Account Abstraction Using Alt Mempool.* Ethereum Improvement Proposals. Pursues contract-account capabilities for ordinary users without a protocol change. <https://eips.ethereum.org/EIPS/eip-4337>
- <a id="ref-buterin-2014"></a>**Buterin, V.** (2014). *Ethereum white paper: A next-generation smart contract and decentralized application platform.* Argues the case for an account model over Bitcoin's transaction outputs, including the replay problem it creates. <https://ethereum.org/en/whitepaper/>
- <a id="ref-eip7702"></a>**Buterin, V., Wilson, S., Dietrichs, A., & lightclient** (2024). *EIP-7702: Set Code for EOAs.* Ethereum Improvement Proposals. Lets a key-controlled account carry contract code, weakening the EOA/contract distinction. <https://eips.ethereum.org/EIPS/eip-7702>
- <a id="ref-eip161"></a>**Wood, G.** (2016). *EIP-161: State trie clearing (invariant-preserving alternative).* Ethereum Improvement Proposals. Activated in Spurious Dragon; deletes accounts left empty at the end of a transaction, so that "holds nothing" and "not recorded" describe the same thing. <https://eips.ethereum.org/EIPS/eip-161>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. §4.1 defines the account state as the four-field tuple, and gives the empty-code and empty-trie constants. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
