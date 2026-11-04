---
tier: 2
description: An account is an entry in Ethereum's state with four fields. There are two kinds, and only one of them can start anything.
---

# Accounts

**Fork-proof in its essentials.** The four fields have been the same since genesis. The clean split between the two *kinds* of account is the part that has started to soften.

!!! info "Current as of Fusaka (December 2025)"

    The four fields and the "only an EOA can start a transaction" rule are
    unchanged since 2015. **EIP-7702** weakened the distinction between the
    two kinds when it shipped in May 2025 — explained in its own box below.
    Nothing in Fusaka touched accounts.

    *EIP* stands for **Ethereum Improvement Proposal**: the numbered documents
    in which every change to Ethereum is proposed, argued over and finally
    specified. They're the primary sources this site cites, and EIP-7702 is
    simply the 7702nd.

    If you're reading much later, check [how this site handles
    forks](../about/forks.md).

!!! definition "Account"

    An **entry in Ethereum's state**, looked up by a 20-byte
    [address](../crypto/addresses.md), holding exactly four fields: a
    **nonce**, a **balance**, a **storage root** and a **code hash**.

    Two kinds exist. An **EOA** is controlled by whoever holds the matching
    [private key](../crypto/private-keys.md). A **contract account** is
    controlled by its own code.

    The address is how you find the account, not something the account stores.

Two words in that box need settling before anything else, because both are doing heavy lifting.

**The state** is the complete record of every account — the thing the [state machine](../foundations/what-is-ethereum.md) page described as "the current situation", as opposed to the history that produced it. Every node keeps a copy. This page only needs that much; [its own page](state.md) comes two pages from here.

**EOA** stands for *externally owned account*, and the name is badly chosen, because it suggests the account is somehow outside Ethereum. It isn't. **An EOA is on the chain exactly as much as any other account** — an entry in the state, with the same four fields, stored by every node.

What's external is only **the thing that controls it**: a private key, sitting on somebody's device, which the network has never seen and knows nothing about. The account is on-chain; its owner is off-chain.

A contract account is the other way round. What controls it is code, and that code is stored *on* the chain in plain view, where every node can read it.

So the two kinds differ in **where the controller lives**, not where the account lives. Both accounts live in the state, and neither could do anything otherwise.

??? note "Nobody says “EOA” out loud"

    It's specification vocabulary. In conversation people say **wallet** — "send
    it to my wallet" — which is loose but unambiguous in context.

    Worth knowing the term anyway, because it's what you'll meet in every EIP,
    every client's source code and every technical discussion, always
    unexplained. This site uses it where precision matters and "wallet" where
    it doesn't.

## What an account actually looks like

Easiest to start with one in front of you. Take the address `0x7E5F…95Bdf` — the one the [addresses](../crypto/addresses.md) page derived from the private key `1`, picked there because it's the simplest number a key can be and makes every step checkable by hand. Ask a node what that address holds — the lookup itself is explained [further down](#how-an-address-finds-an-account):

```
nonce        3
balance      1500000000000000000
storageRoot  56e81f17…b421
codeHash     c5d24601…a470
```

Four values, and that is the entire account. The address isn't in there — it's what you looked the account *up* by, like a word in an index rather than part of the entry. The balance is in [wei](../foundations/ether.md), so it reads as 1.5 ether. The nonce says three transactions have been sent from here. The last two are hashes, and the specific ones shown mean *nothing stored* and *no code* — more on them shortly.

Now a contract account, same four fields:

```
nonce        0
balance      0
storageRoot  ⟨fingerprint of its stored values⟩
codeHash     ⟨fingerprint of its code⟩
```

Neither of those last two is the empty constant, and that is the only thing distinguishing this account from the one above. Same shape, different contents. **There is no fifth field marking it as a contract.** The difference is entirely in those last two values, and we'll come back to exactly how you read it.

A note on those numbers. The address is real — it's the one [private key `1` produces](../crypto/addresses.md), the most-guessed key in existence — but the nonce and balance shown for it are made up for illustration. The two hashes in the wallet account are genuine fixed constants, and you'll meet them again in a moment. The contract's two are written in words rather than invented hex, because a plausible-looking fake hash is worse than no hash at all.

## The four fields

Every account, of either kind, holds these and nothing else [(Wood, 2014)](#ref-wood-2014):

| Field | What it holds |
| --- | --- |
| `nonce` | A counter — transactions sent, or contracts created |
| `balance` | Ether owned, in [wei](../foundations/ether.md) |
| `storageRoot` | Fingerprint of everything in storage |
| `codeHash` | Fingerprint of the code |

The first two are plain numbers, but the word **nonce** needs defusing immediately, because it invites exactly the wrong guess.

**It does not mean "random number" here.** The account nonce is a plain sequential counter: it starts at 0 and goes up by one each time the account sends a transaction — 0, 1, 2, 3. It is public, anyone can read yours, and it is *meant* to be predictable, since your wallet has to know which number comes next and so does every node checking your transaction. A secret or random counter would be unusable.

The confusion is the vocabulary's fault. *Nonce* is merely short for **"number used once"**, which promises nothing about *how* the number is chosen.

??? abstract "This site has already used “nonce” in the other sense"

    So the collision is worth naming, rather than letting you trip over it
    later.

    - **Random, and necessarily unpredictable.** The `k` in [signing a
      message](../crypto/signatures.md) is this kind. Reuse one and your
      private key can be recovered — that page shows the arithmetic. Bitcoin's
      mining nonce is similar: a value searched for, essentially at random.
    - **Sequential, and entirely predictable.** The account nonce on this page.
      Counting, not guessing.

    What they share is only the guarantee in the name: **each value is used
    exactly once.** For `k` that's achieved by drawing unpredictably from a
    space too large to repeat by accident. For an account it's achieved by
    adding one. Same promise, opposite methods — and for `k`, secrecy is
    essential, while for the account nonce it would break everything.

    Two more nonces exist in Ethereum's vicinity, for completeness: the
    proof-of-work block nonce, now historical, and the per-contract counter
    described above, which counts deployments rather than transactions.

### The two fingerprints

These are the fields that needed groundwork, and the groundwork is now in place.

A contract can hold a great deal — thousands of stored values, and a program of some size. **None of it is in the account entry.** What the account holds is a *hash* of each: the kind of fingerprint the [Keccak-256](../crypto/keccak256.md) page described, where changing any input byte produces a completely different output.

That buys one specific thing. The account entry stays small and fixed-size no matter how much the contract stores, while still **committing** to every byte of it — you cannot alter one stored value without changing `storageRoot`, and you cannot change the code without changing `codeHash`.

What's still deferred is how you hash a *collection*. Hashing one lump of bytes is simple; hashing a mapping of thousands of keys and values, such that you can prove one entry belongs without presenting all the others, needs a structure. That structure is the [Merkle Patricia Trie](../encoding/merkle-patricia-trie.md), and it has a page. Here, it's enough that a fingerprint exists and nothing can change beneath it unnoticed.

An account with no storage and no code still has both fields. They hold the fingerprints **of emptiness**, which are two fixed constants:

```
codeHash — the hash of no code at all
    c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470

storageRoot — the root of an empty trie
    56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421
```

The first is Keccak-256 of nothing at all — the empty-input hash the Keccak page used to check its own implementation against the published value. The second is the root of an empty trie. **Every ordinary wallet account on Ethereum carries that identical pair**, which is what makes the next section possible.

### So one account can hold code *and* storage

Yes, and for a contract that's the normal case. The two fields are independent, which gives the combinations you actually meet:

| Account | `codeHash` | `storageRoot` |
| --- | --- | --- |
| Ordinary wallet | empty constant | empty constant |
| Contract holding data | its code | its storage |
| Freshly deployed contract | its code | empty constant |

The missing fourth row — storage but no code — isn't something you meet, because the only thing that can write to an account's storage is that account's own code.

### And yes, a contract can hold ether

Worth being explicit, since it surprises people. **The `balance` field is on every account**, because there is only one kind of entry in the state. A contract isn't a different sort of object with a different shape; it's an account that happens to have code.

It also has to be that way for contracts to be good for anything. An escrow must actually hold the money it's holding. A trading pool must own the assets it trades. If contracts couldn't own ether they could only ever direct other people's, which is a far weaker thing to be.

What differs is **how the ether gets out**. An EOA's balance moves when its key signs a transaction. A contract's balance moves only if the contract's own code contains instructions to send it — and if the code has no such path, the ether stays there permanently, as unreachable as if the key had been lost. That has happened at scale more than once, and the reason is worth remembering: nobody can override the code, for precisely the reasons the [previous page](../wallets/losing-your-keys.md) set out.

How contracts work beyond that — what the code is, how it runs, what it costs — is [its own page](../contracts/smart-contracts.md).

## How an address finds an account

This page has twice said "ask a node" without saying what that involves, and the answer is more specific than *it looks it up in a list*.

The state is a key–value mapping. The value is the four fields, written out with [RLP](../encoding/rlp.md) — Ethereum's way of encoding structured data as bytes, which has its own page. The key is the part worth noticing: **it is not the address.** It's the address put through [Keccak-256](../crypto/keccak256.md) first.

```
address      0x7E5F…95Bdf
    │
    │  keccak256
    ▼
key          a 32-byte value, which is where to look
    │
    ▼
value        RLP[ nonce, balance, storageRoot, codeHash ]
```

So nothing about the account is *computed* from the address. The contents are whatever transactions have put there over time, and no amount of arithmetic on an address could tell you a balance. What the address gives you is **where to look** — and the precise structure it's looking in, which makes that lookup provable rather than merely fast, is the [Merkle Patricia Trie](../encoding/merkle-patricia-trie.md).

### Why hash the address first?

It seems like a pointless step — the address is already a hash, and already a fixed 20 bytes. There's a reason, and it's a defence.

**Without it, anybody could choose where in the structure their account lands.** That sounds harmless until you notice that *creating an account costs almost nothing and needs no key*: send one wei to any address and an entry appears, as the empty-accounts box above describes. Nobody has to control an address to put something at it.

So an attacker could pick a million addresses sharing a long leading prefix, dust each one, and force the structure into a single pathologically deep branch — making every lookup along it slow, for every node, permanently. Choosing the keys was free, and the cost landed on everybody else.

Hashing removes the choice. To place two accounts near each other you'd now have to find two addresses whose *hashes* share a long prefix, and that's a brute-force search for every account you want to add. The attack goes from free to expensive, which is the whole of the defence.

A secondary benefit falls out: hash outputs are spread evenly, so keys distribute evenly and no region of the structure ends up much deeper than another even by accident.

## Which kind is it? Look at one field

Suppose somebody hands you an address and you want to know whether it's a person's wallet or a contract. You cannot tell by looking: [addresses](../crypto/addresses.md) are 20 bytes either way, and that page made the point that nothing in one reveals which kind it is.

The answer is in the account, and it takes one comparison. Ask any node for the account, then look at `codeHash`:

- It equals `c5d2…a470` → there is **no code** → it's an **EOA**.
- It's anything else → there **is** code → it's a **contract**.

That's the entire test. Which is worth dwelling on for a second, because of what it implies: **no field says which kind of account this is.** Nothing was declared when the account came into being, and there's no flag anybody set. The kind is *read off* from what the account holds.

Everything else follows from that one difference:

| | EOA | Contract account |
| --- | --- | --- |
| Controlled by | whoever holds the private key | its own code |
| Comes into being when | an address derived from a key is first used | a transaction deploys code |
| Can start a transaction | **yes** | **no** |
| Its nonce counts | transactions sent | contracts created |

Both can hold ether, both are addressed identically, and both appear in the state the same way.

??? abstract "Why there's no type field — or an owner, or a name"

    Four fields is a strikingly short list, so it's worth asking what *isn't*
    there. Each absence is deliberate.

    **No type**, as above. It would be redundant, and redundancy in consensus
    data is a liability: two fields that can disagree need a rule for which
    one wins. Deriving the type from `codeHash` makes disagreement impossible.

    **No owner.** For a contract there's nothing to put — control is whatever
    the code says, which might be one key, five keys, a vote, or nobody. For an
    EOA it would be the public key, which is exactly what the address already
    commits to.

    **No name, no creation date, no history.** The state answers *what is true
    now* and nothing else. How an account reached its current contents is
    recoverable from the blocks, so putting it in the state would mean every
    node storing a second copy of something it already has.

    The pattern recurs all over Ethereum: **the state holds the minimum from
    which everything else can be derived.** Anything inferable is left out,
    because storing it anyway only creates a way for a node to be wrong.

## Nothing creates an account

With the concrete picture in place, one consequence is worth drawing out.

"Opening an account" is a thing you do at a bank — an application, an approval, a record created in your name. None of that has an equivalent here. The [addresses](../crypto/addresses.md) page established that **nothing creates an address**: all 2<sup>160</sup> exist already, and a wallet merely derives one. Accounts inherit that. An account isn't created; it **begins to be recorded** the first time there's something to record.

So an address nobody has ever used is not in the state at all. Not stored as a row of zeros — absent. Which is indistinguishable from an account holding nothing, and that's the point: zero balance and no stored entry describe the same situation. Ask a node for the balance of an untouched address and it answers zero, because that's the correct answer, not because it found a record saying so.

??? abstract "Which makes “empty” an awkward category"

    A case where a tidy idea needed patching.

    Early on you could create entries that existed while holding nothing: send
    zero ether to an untouched address and a record appeared with a zero
    balance, a zero nonce and no code. Functionally identical to absence, but
    occupying space on every node — and millions were made cheaply as a
    result.

    **EIP-161** [(Wood, 2016)](#ref-eip161) fixed it in the [Spurious Dragon
    upgrade](../reference/fork-history.md "The 2016 hard fork that introduced state-trie clearing")
    of 2016, by deleting such accounts at the end of any transaction that
    touched them — so "holds nothing" and "isn't recorded" converged again.

    More than trivia, because of what it reveals: **everything in the state is
    something every node must store, forever, at a real cost.** Storing nothing
    therefore has to cost nothing, or the accounting breaks. That pressure
    turns up again and again once you reach [gas](../transactions/gas.md).

## Only an EOA can start anything

This is the most clarifying fact about how Ethereum runs, and it's routinely assumed to work the other way.

**Nothing on Ethereum happens by itself.** There are no timers, no scheduled jobs, no background processes. A contract cannot wake up at midnight, cannot poll a price, cannot notice that a deadline has passed. It has no thread of its own and no way to get one.

A contract's code runs only when something **calls** it. Follow any chain of calls back far enough and it begins in the same place: a transaction, signed by a private key, sent from an EOA. Contracts can call other contracts, and one transaction can touch dozens — but all of it descends from a single signature at the root.

Two reasons it has to be this way:

- **Somebody has to pay.** Execution is metered and the fee comes from the account that sent the transaction. Self-starting code would be work with no payer.
- **Somebody has to be the cause.** Every node must reach the same result, so all of them must run the same operations in the same order. Spontaneous execution would require agreement on *when* it fired — and there is no shared clock to agree with.

??? question "Then how do things that look automatic work?"

    Somebody is sending transactions. The useful question is why they bother,
    and the answer is that they're paid to.

    Take a lending contract that must sell somebody's collateral when its value
    falls too far. The contract can't watch the price — per the rule above, it
    cannot do anything at all unless called. So it's built the other way round:
    it exposes a function **anybody may call**, which checks the price and
    performs the sale only if the condition genuinely holds. Until called, it
    sits inert.

    But the contract still *needs* that sale to happen, and promptly, or it
    takes a loss. So it offers a cut of the proceeds to whoever makes the call
    at the right moment. **That converts "something must watch the price" into
    a paid job, open to anyone** — which is the only way to get it done, since
    the contract cannot employ anybody and cannot act alone.

    Hence the racing. The reward goes to the caller whose transaction lands
    **first**, and only the first: every later call re-checks the condition,
    finds it no longer true, and does nothing. So the people doing this run
    software watching for the condition and compete to get their transaction
    in ahead of the others, because second place pays nothing.

    The pattern has a name — **keepers**, or bots. The automation is economic,
    not technical. Which makes "it executes automatically" a claim worth
    examining: the honest version is usually *somebody is paid to make it
    execute, and so far somebody has.* Let the reward stop covering the fee and
    the automation quietly stops.

??? warning "One thing here is changing: EIP-7702"

    The rule above holds. The tidy *statement* of the previous section doesn't,
    quite.

    **EIP-7702** [(Buterin et al., 2024)](#ref-eip7702), live since Pectra in
    May 2025, lets an EOA set its `codeHash` to point at contract code. So
    "EOAs have no code" is no longer strictly true, and the
    compare-against-the-constant test now has an exception.

    What it's for: giving ordinary wallets abilities that used to require a
    contract account — batching several actions into one transaction, letting
    somebody else pay your fee, setting spending permissions. The same goals
    ERC-4337 [(Buterin et al., 2021)](#ref-erc4337) pursues as a layer on top.

    What it does **not** change: an EOA still needs a key to authorise
    anything, and transactions still originate only from EOAs. Both rules this
    page rests on survive. What's blurring is the tidy two-kinds taxonomy —
    which is why this page carries a date stamp at the top, and why you should
    hold that taxonomy loosely.

??? question "So is an account the same thing as a wallet?"

    No, and the words get used interchangeably constantly.

    - An **account** is the entry in the state. It exists whether or not any
      software knows about it.
    - A **[wallet](../wallets/seed-phrases.md)** is the program on your device.
      It holds keys and builds transactions, and Ethereum has never heard of
      it.
    - An **EOA** is an account whose key some wallet happens to hold.

    So "my wallet has three accounts" means one piece of software holding keys
    for three addresses. The accounts aren't *in* the wallet, and losing the
    wallet doesn't touch them — as the [previous
    page](../wallets/losing-your-keys.md) laboured.

    Harmless in conversation. A problem the moment you read a specification,
    where "account" never means "app".

## Why this design needs a nonce

One last consequence, to set up the next page.

Ethereum records **balances** where Bitcoin records individual coins. The [state machine](../foundations/what-is-ethereum.md) page covered the comparison, and [Buterin (2014)](#ref-buterin-2014) argues the case at length. Here is what the choice costs.

The difference is roughly **cash versus a bank statement.** Bitcoin is the cash: you hold particular notes, paying someone means handing over specific notes, and you get different ones back as change. The notes *are* the money, and each individual one either exists or has been spent. Ethereum is the statement: there are no notes at all, just a number beside your address that goes up and down.

That distinction decides whether replay is even possible.

A Bitcoin transaction consumes specific coins — it names them. Submit it twice and the second attempt fails on its own terms, because the coins it names are already gone: not merely disallowed, but meaningless, like trying to hand over a note you no longer have. **The protection is a property of the thing being spent.**

An account has no such property. "Send 1 ether from A to B" names nothing that gets used up. It's a valid instruction before it executes and an equally valid instruction afterwards, because A's balance is just a number and the instruction never referred to any particular part of it. A signed transaction would be a **reusable cheque**: anyone who saw it could submit it again, and every copy would verify perfectly.

So the protection has to be supplied separately, and it's supplied as a counter. That's the [nonce](nonce.md).

---

## Recap

- An account is an **entry in the state**, looked up by address, with exactly four fields: **nonce, balance, storageRoot, codeHash.** The address isn't one of them.
- The lookup key is **`keccak256(address)`**, not the address — so nobody can choose where their account sits, which stops an attacker dusting a million chosen addresses to force one deep, slow branch.
- **EOA** means *externally owned* — what controls it sits outside Ethereum, namely a person with a key. A contract's controller is code on the chain.
- The account **nonce is a sequential counter**, not a random number. It shares only the "used once" guarantee with the random nonces elsewhere in cryptography.
- `storageRoot` and `codeHash` are **fingerprints**, letting a fixed-size entry commit to unbounded data. The structure behind them is the [Merkle Patricia Trie](../encoding/merkle-patricia-trie.md).
- An account with neither carries the two constants for empty — `c5d2…a470` and `56e8…b421`.
- **The kind of account is read off `codeHash`**, not declared. There is no type field, because the type is derivable.
- **Nothing creates an account.** An unused address is absent from the state, which is indistinguishable from holding nothing.
- **Only an EOA can start a transaction.** No timers, no scheduled jobs. Anything that looks automatic is somebody paid to send a transaction, racing others for the reward.
- **EIP-7702 has begun blurring the EOA/contract split** without changing either rule above.
- Balances aren't consumable the way coins are, so replay protection must be added separately — by the **nonce**.

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
