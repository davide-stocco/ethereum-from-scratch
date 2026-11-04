---
tier: 1
description: A per-account counter that stops a signed transaction being used twice — and the reason transactions get stuck.
---

# The nonce

**Fork-proof.** Nonce semantics have never been revised.

!!! definition "Nonce"

    Literally **"number used once"** — which is all the word promises, and says
    nothing about how the number is chosen. Ethereum reuses it for several
    unrelated mechanisms, [listed at the end of this
    page](#other-things-called-a-nonce).

    This page is about the **account nonce**: a counter stored in every
    [account](accounts.md). A transaction declares which value it is claiming,
    the network accepts it only if that value is the one the account is due
    next, and the counter then advances — so **no number can ever authorise
    two things.**

    It counts; it is not random. *What* it counts and where it starts depend on
    the kind of account, and both are below.

## The account nonce, concretely

Take an ordinary wallet account. It has sent three transactions. Its nonce is 3. The next transaction you sign must say `nonce: 3`, and once it's in a block the account's nonce becomes 4.

That really is the whole mechanism. The reason it's worth a page is not the counter — it's what the counter prevents, and the very practical trouble it causes when it gets out of step.

??? abstract "Why the name misleads, when most nonces really are random"

    The confusion is reasonable: elsewhere in cryptography a nonce almost
    always *is* a random value, and nothing in the word rules that out.

    The `k` used when [signing](../crypto/signatures.md) is the famous example:
    it must be unpredictable, and reusing one leaks your private key. The
    account nonce is the opposite kind. It counts, it's public, and anybody can
    read yours.

    Being predictable isn't a weakness here, it's a requirement — your wallet
    has to know which number comes next, and so does every node checking your
    transaction. A secret counter would be unusable.

## The problem it solves

The [accounts](accounts.md) page ended on this, so briefly: a signed transaction without a nonce would be a **reusable cheque.**

"Send 1 ether from A to B" names nothing that gets consumed. The instruction is as valid after it executes as before, because A's balance is only a number and the instruction never referred to any particular part of it. So anybody who saw your transaction — and everybody sees every transaction — could submit the identical bytes again. The signature would still verify, because it's a signature over those bytes, and the bytes haven't changed.

Your 1-ether payment becomes a hundred-ether payment, by somebody else's choice, with your valid signature on every copy. [Buterin (2014)](#ref-buterin-2014) names this as the cost of choosing an account model, and the counter as the answer to it.

The nonce closes it completely. Your transaction says `nonce: 3`, and the moment it's included your account is due nonce 4. The replayed copy still says 3, which is now **wrong**, so every node rejects it without even looking at the signature.

### Why Bitcoin needs no such thing

Because of the difference set out on [What is Ethereum?](../foundations/what-is-ethereum.md) — Bitcoin records individual coins, Ethereum records balances.

A Bitcoin transaction names the specific coins it spends. Submit it twice and the second attempt isn't rejected by a rule — it's **meaningless**, because the coins it names no longer exist. The protection is a property of the thing being spent.

Ethereum has nothing consumable to lean on, so it adds a counter instead. Same protection, supplied by bookkeeping rather than by the structure of money.

??? note "The nonce doesn't protect you across chains"

    Worth knowing, since the two defences get confused.

    Many networks run Ethereum's rules with their own history. Your nonce means
    nothing on another chain — it keeps its own count for your address, so a
    transaction valid here could be replayed *there*, where the same key
    controls the same address.

    That's the job of a second field, the **chain id**, introduced by EIP-155
    [(Buterin, 2016)](#ref-eip155) and covered on the
    [signatures](../crypto/signatures.md) page.

    - **nonce** — stops the same transaction twice on *this* chain
    - **chain id** — stops it being carried to *another* chain

    Neither substitutes for the other.

## Strictly in order, no gaps

Here is the part with consequences. The rule isn't "a nonce you haven't used yet" — it's **exactly the next one.**

If your account's nonce is 5, then a transaction with nonce 5 is valid and a transaction with nonce 7 is not. Not invalid forever; invalid *for now*. It becomes valid the instant nonce 6 is included, and not a moment before.

That's a condition of validity rather than a preference: the specification lists a matching nonce among the tests a transaction must pass before it may be applied at all [(Wood, 2014)](#ref-wood-2014).

<svg viewBox="0 0 470 236" role="img" aria-label="A queue of transactions from one account. Nonces 3 and 4 are already included. Nonce 5 is stuck because its fee is too low. Nonces 6, 7 and 8 are fully paid and valid but cannot be included, because the protocol requires nonces in strict order and 5 has not happened yet." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="10" y="60" width="54" height="46" rx="4" opacity="0.45"/><rect x="72" y="60" width="54" height="46" rx="4" opacity="0.45"/><rect x="134" y="60" width="54" height="46" rx="4" stroke-dasharray="4 3"/><rect x="200" y="60" width="54" height="46" rx="4"/><rect x="262" y="60" width="54" height="46" rx="4"/><rect x="324" y="60" width="54" height="46" rx="4"/><path d="M188 83 L196 83" stroke-dasharray="3 2"/><path d="M390 83 L404 83" stroke-dasharray="3 2"/></g><g fill="currentColor" stroke="none"><text x="10" y="22" font-size="11" font-weight="700">one account&#8217;s queue</text><text x="10" y="40" font-size="10" opacity="0.75">the protocol takes them in this order, with no skipping</text><text x="37" y="80" font-size="13" text-anchor="middle">3</text><text x="37" y="98" font-size="8" text-anchor="middle" opacity="0.7">done</text><text x="99" y="80" font-size="13" text-anchor="middle">4</text><text x="99" y="98" font-size="8" text-anchor="middle" opacity="0.7">done</text><text x="161" y="80" font-size="13" text-anchor="middle" font-weight="700">5</text><text x="161" y="98" font-size="8" text-anchor="middle">fee too low</text><text x="227" y="80" font-size="13" text-anchor="middle">6</text><text x="227" y="98" font-size="8" text-anchor="middle" opacity="0.7">waiting</text><text x="289" y="80" font-size="13" text-anchor="middle">7</text><text x="289" y="98" font-size="8" text-anchor="middle" opacity="0.7">waiting</text><text x="351" y="80" font-size="13" text-anchor="middle">8</text><text x="351" y="98" font-size="8" text-anchor="middle" opacity="0.7">waiting</text><text x="412" y="86" font-size="14" opacity="0.6">&#8230;</text><text x="134" y="130" font-size="10" font-weight="700">this one is stuck</text><text x="134" y="146" font-size="10" opacity="0.85">&#8212; and so is everything to its right</text><text x="10" y="178" font-size="10" opacity="0.85">6, 7 and 8 may each offer a generous fee. It makes no difference: the</text><text x="10" y="192" font-size="10" opacity="0.85">protocol will not accept nonce 6 until nonce 5 has happened, so no</text><text x="10" y="206" font-size="10" opacity="0.85">block can contain them. A queue with one jam at the front is a queue</text><text x="10" y="220" font-size="10" opacity="0.85">that has stopped.</text></g></svg>

Why so strict? Because the alternative is ambiguity. If gaps were allowed, a node holding nonces 5 and 7 would have to decide whether 6 is coming, and two nodes could reasonably decide differently — one applying 7, the other waiting. **They would disagree about the state**, which is the one thing the design cannot tolerate. A strict sequence means every node knows, with no judgement involved, exactly which transaction from your account comes next.

## Why transactions get stuck

This is the most useful thing on the page, because nearly everyone meets it and almost nobody is told why.

Suppose you send a transaction with nonce 5 and attach a fee too low for anyone to want to include it. It sits unconfirmed. Annoying, but you'd expect it to affect only that one transaction.

It doesn't. **It blocks every later transaction from the same account**, however much each of those offers, because none of them can legally be included before nonce 5 is. Your whole account is frozen behind one cheap transaction — and nothing in any wallet's interface explains that this is what has happened.

What nodes do with the later ones varies, and this is worth knowing because it shapes what you see:

- The protocol's rule is about **blocks**: a block containing nonce 6 without 5 having happened is invalid. Flat rule, no discretion.
- A node's **waiting room** is softer. Most clients will hold a transaction whose nonce is in the future, hoping the gap fills — often labelled *queued* as against *pending*. They may also drop it after a while, or refuse to hold more than a few.

So "stuck" has two flavours that look identical from outside: the gap transaction nobody will mine, and the later ones no block may legally contain yet.

### Unsticking one

You cannot delete a transaction. Nothing on Ethereum can be withdrawn once broadcast — there's no instruction for it and nobody to ask. What you *can* do is **replace** it.

Sign a new transaction with **the same nonce** and a fee high enough to be worth including. Now two transactions claim nonce 5, and at most one of them can ever be included, since the account's nonce can only pass 5 once. Nodes keeping a waiting room generally prefer the better-paying of the two and discard the other.

Two details that matter in practice:

1. **You must re-sign.** The nonce is part of what you signed, so you cannot edit a broadcast transaction — the signature wouldn't match. A replacement is a genuinely new transaction that happens to reuse the number.
2. **The fee must be meaningfully higher.** Clients won't swap one transaction for a near-identical one, or the network could be flooded with trivial replacements. A small increase is usually refused.

To **cancel** rather than retry, send something harmless at that nonce instead — most wallets do this by sending zero ether to your own address. It still has to be included and still costs a fee, but it consumes the number, and the queue behind it starts moving.

??? warning "Cancelling is a race, not a command"

    The original transaction remains perfectly valid the whole time. If someone
    includes it before your replacement lands, **it happened** — your cancel
    simply becomes the one that's now invalid.

    So a cancellation is an attempt to win a race against your own earlier
    transaction, not an undo. The longer it has been sitting there, and the
    better it pays, the likelier you lose.

??? question "Why did my wallet send two transactions with the same nonce by accident?"

    Because asking "what nonce is next?" has two answers, and tools don't
    always pick the same one.

    - Counting only what's **confirmed on chain** gives you the account's
      actual nonce.
    - Counting confirmed transactions **plus the ones you've already
      broadcast** gives you the next free number.

    Use two wallets, or one wallet and one script, and they can each read the
    confirmed count, each decide the next nonce is the same number, and sign
    two different transactions with it. Only one can ever be included. The
    other is not merely rejected — it becomes permanently invalid the moment
    its rival is mined.

    Which is occasionally useful and mostly an accident. If you're signing from
    more than one place at once, something has to track the count.

## Contract accounts have a nonce too

Same field, different meaning: for a contract, the nonce counts **how many contracts that account has created.**

That isn't an unrelated reuse of the field. It serves the same purpose — making sure a number is never used twice — because a contract's address is computed from **the creating address and that creator's nonce**, as the [addresses](../crypto/addresses.md) page described. The nonce is what stops two deployments from the same account landing on the same address.

??? abstract "A contract's nonce starts at 1, not 0"

    A small asymmetry, and a deliberate one.

    An EOA begins at nonce 0. A newly created contract begins at **1**, a rule
    introduced by EIP-161 [(Wood, 2016)](#ref-eip161) in the same upgrade that
    cleared out empty accounts.

    The reason is the address calculation above. A contract that still had
    nonce 0 could compute an address for its own first deployment that
    collided with an address derived some other way, and starting the count at
    1 removes the overlap. One of those fixes that looks arbitrary until you
    notice what it rules out.

## What the nonce is not

Four things it gets mistaken for:

- **Not a timestamp.** It says how many transactions you've sent, not when. An account that sent three transactions years apart has nonce 3.
- **Not global.** Every account keeps its own, independently. There is no network-wide transaction counter.
- **Not secret.** Anybody can read any account's nonce, and they must be able to.
- **Not a measure of anything but transactions sent.** Receiving ether doesn't change your nonce — receiving requires no transaction from you. An account can hold a fortune and still have nonce 0.

That last one is the useful test: **the nonce counts what you did, never what happened to you.**

## Other things called a nonce

The word is reused all over Ethereum for things that have nothing to do with each other beyond the "used once" promise. Worth having the list in one place.

| Where | What it is | Chosen how |
| --- | --- | --- |
| **Account** | the counter this page is about | counting, 0 upwards |
| **Transaction** | the field in which a transaction *declares* which account nonce it is claiming | copied from the account |
| **Block header** | a leftover from proof of work | now **always zero** |
| **Signing** (`k`) | the secret value in [ECDSA](../crypto/signatures.md) | random, and must be unpredictable |
| **Inside contracts** | whatever a contract's author decided | up to them |

**They share the name and nothing else.** The value is chosen by counting, or at random, or fixed at zero, or however a contract's author felt; by the protocol, your wallet, the signer, or a stranger. And the cost of repeating one ranges from trivial to catastrophic: reuse an account nonce and your second transaction is simply rejected, while reuse a signing `k` and your private key can be reconstructed from the two signatures.

So there's no general account of nonces to give — "used once" is the whole of the overlap, and a page about that would be a page about a word. Each mechanism is instead covered where its own subject lives: `k` with [signatures](../crypto/signatures.md), the dead field with [the block header](../blocks/block-header.md), the declared value with [transactions](../transactions/transactions.md), and contract counters with [contracts](../contracts/smart-contracts.md). This page takes the account nonce because this section is about accounts.

Two of them still deserve a second look here, because they're the two that get mistaken for this one.

**The account nonce and the transaction nonce are different fields.** The account holds the count; the transaction states the number it claims. Validity is the test that the two agree. It's easy to read "the nonce" as one thing in one place, but there are two copies and the whole mechanism is the comparison between them.

**The block header's nonce is a fossil.** Under proof of work, miners searched for a value that made the block's hash small enough — that search *was* mining, and the nonce was where the answer went. Proof of stake abolished the search, and EIP-3675 [(Kalinin et al., 2021)](#ref-eip3675) requires the field to be exactly `0x0000000000000000` from the transition block onward. It stays in the header because the header's shape is baked into too much code to change for nothing, so every block since the Merge carries eight bytes of zeros where the puzzle answer used to be.

**And the contract ones aren't protocol at all.** A contract accepting signed instructions from off-chain has the same replay problem this page opens with, and no account nonce to lean on, because the signature isn't a transaction. So contracts keep their own counters — token approvals, account-abstraction operations, anything with an off-chain signature. Each is a convention its author invented, enforced only by that contract's code.

---

## Recap

- The **account nonce** is a per-account counter. For a wallet account it counts transactions sent and starts at 0, and it's part of what you sign.
- It exists to stop **replay**: without it a signed transaction could be submitted again and again, and every copy would verify.
- Bitcoin needs no equivalent because its transactions name specific coins, which can only be spent once. **Balances offer no such protection**, so a counter supplies it.
- Nonces must be used **in strict order with no gaps** — nonce 7 is invalid until 6 has been included — because gaps would let two nodes reasonably disagree about what comes next.
- Therefore **one underpriced transaction blocks every later one** from the same account, no matter what they pay.
- You can't delete a transaction, only **replace** it: same nonce, higher fee, newly signed. Cancelling means winning a race against your own earlier transaction, which you may lose.
- For a contract the nonce counts **contracts created**, and it starts at 1. It keeps deployment addresses from colliding.
- The nonce counts **what you sent** — never what you received.
- **"Nonce" is reused for several unrelated things**: the account's counter, the transaction field that claims it, the block header's dead proof-of-work field, the secret `k` in signing, and whatever counters contracts keep for themselves.

**Next:** [State](state.md) — the whole collection of accounts, and how a tiny block header commits to all of it.

---

## References

<div class="sources" markdown>

- <a id="ref-buterin-2014"></a>**Buterin, V.** (2014). *Ethereum white paper: A next-generation smart contract and decentralized application platform.* Sets out the account model and the replay problem a counter is needed to solve. <https://ethereum.org/en/whitepaper/>
- <a id="ref-eip155"></a>**Buterin, V.** (2016). *EIP-155: Simple replay attack protection.* Ethereum Improvement Proposals. Adds the chain id, which handles the replay case the nonce cannot — the same transaction carried to a different network. <https://eips.ethereum.org/EIPS/eip-155>
- <a id="ref-eip3675"></a>**Kalinin, M., Ryan, D., & Buterin, V.** (2021). *EIP-3675: Upgrade consensus to Proof-of-Stake.* Ethereum Improvement Proposals. Requires the block header's nonce to be the zero constant from the transition block onward. <https://eips.ethereum.org/EIPS/eip-3675>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Defines the nonce as a field of the account state and makes the matching nonce a condition of transaction validity. <https://ethereum.github.io/yellowpaper/paper.pdf>
- <a id="ref-eip161"></a>**Wood, G.** (2016). *EIP-161: State trie clearing (invariant-preserving alternative).* Ethereum Improvement Proposals. Specifies that a newly created contract's nonce begins at 1, closing an address-collision case. <https://eips.ethereum.org/EIPS/eip-161>

</div>
