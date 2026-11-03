---
tier: 1
description: How a signature proves you hold a private key, and how the sender's address is recovered from the signature rather than stated anywhere.
---

# Signatures

**Fork-proof.** ECDSA over secp256k1, unchanged since genesis.

The [private keys](private-keys.md) page described what a signature is *for*: proving you know a secret without revealing it. This page is about how Ethereum actually uses that — and it opens with the fact that surprises nearly everyone.

## A transaction never says who sent it

Transactions get a page of their own later. Only one thing about them matters here.

A transaction is a short list of fields — how much, to whom, what data, how much fee — followed by three numbers called `v`, `r` and `s`, which together are the signature.

**There is no "from" field.** Nowhere does a transaction state its sender.

Instead, the sender's address is **recovered** from the signature. Given the signed message and those three numbers, anyone can compute the public key that must have produced them — and from that, [the address](addresses.md).

This isn't optional or occasional. When a node receives a transaction it has to establish who sent it before it can do anything at all: whose balance to check, whose [nonce](../accounts/nonce.md "A per-account counter of transactions already sent") to compare against, whose account to take the fee from. Recovery is how it finds out, so every node runs it on every transaction it ever sees. The Yellow Paper defines the function for exactly this purpose [(Wood, 2014)](#ref-wood-2014).

So the signature doesn't *accompany* a claim of identity. The signature **is** the claim.

Which is rather elegant once it lands. A forged "from" field would be worthless, so Ethereum doesn't have one. The only way to appear as the sender of a transaction is to produce a signature that recovers to your address, and the only way to do that is to hold the key.

## What actually gets signed

Not the transaction — the **hash** of the transaction, via [Keccak-256](keccak256.md).

That has a useful consequence. Since the hash covers every field, changing any single byte of the transaction changes the hash, and a signature over the old hash recovers to a different address. So the signature protects **all** of it at once: the amount, the recipient, the fee, the nonce. There's no need to sign each field separately, and no way to alter one in transit.

## How a signature is made

The thing doing the work deserves naming — and so do its three outputs, which appear everywhere once you start looking at transactions.

Signing and recovery are done with **ECDSA**, the Elliptic Curve Digital Signature Algorithm [(SECG, 2009)](#ref-sec1). It isn't an Ethereum invention or a cryptocurrency one; it's a long-standing standard behind TLS certificates and software signing. Ethereum's contribution is the curve it runs on, and the use it makes of recovery.

### The three operations, side by side

```
    signing:      message hash  +  private key          ──►   r, s
    verifying:    message hash  +  r, s  +  public key   ──►   yes or no
    recovering:   message hash  +  r, s  +  v            ──►   the public key
```

The first two are ordinary ECDSA, used across the internet. The **third** is the one Ethereum leans on, and it gets a section of its own below.

The rest of this section covers **signing**. Recovery follows after it.

### Where `r` and `s` come from

Signing a message hash **z** with a private key **d** goes like this:

1. Pick a **random secret number**, called *k*, used once and then thrown away.
2. Compute the curve point *k* × G, the same multiplication from the [public keys](public-keys.md) page. Call it **R**.
3. **`r` is the x coordinate of R.**
4. **`s` is computed from** the message hash, `r`, the private key and *k*:

```
    s  =  k⁻¹ ( z  +  r · d )      mod n
```

Every term there has already appeared on this site:

| | |
| --- | --- |
| *z* | the message hash, from [Keccak-256](keccak256.md) |
| *d* | the private key — the only secret in the equation |
| *r* | the x coordinate from step 3 |
| *k* | the random number from step 1 |
| *n* | secp256k1's order, from the [private keys](private-keys.md) page |

*k*⁻¹ means the modular inverse — the number that multiplies by *k* to give 1, working modulo *n*. Not a fraction; there are no fractions anywhere in this.

So the two halves have distinct jobs. `r` is a commitment to the random point: it depends on *k* and nothing else. `s` is the half the **private key enters**, mixed with the message hash so that the pair is bound to this message and no other.

And notice that *d* appears exactly once, multiplied by *r* and buried under a *k*⁻¹ you don't know. That's what makes the equation safe to publish.

Neither value reveals *d*, and neither reveals *k*. And because *k* is fresh every time, `r` and `s` are completely different on every signature — which is what you see when you press *Sign again* below.

??? warning "*k* must never repeat — and here is exactly why"

    If one key signs two different messages using the same *k*, **the private
    key falls out of the two signatures.** Not eventually, not with effort:
    immediately, with two subtractions and two divisions.

    Here's the whole attack.

    Since `r` depends only on *k*, two signatures sharing a *k* also share the
    same `r`. So you have two equations:

    ```
    s₁  =  k⁻¹ ( z₁ + r·d )
    s₂  =  k⁻¹ ( z₂ + r·d )
    ```

    Subtract them. The `r·d` terms are identical in both, so they **cancel** —
    and *d* vanishes along with them:

    ```
    s₁ − s₂  =  k⁻¹ ( z₁ − z₂ )
    ```

    Now *k* is the only unknown left, and it's trivially isolated:

    ```
    k  =  ( z₁ − z₂ ) · ( s₁ − s₂ )⁻¹
    ```

    Everything on that right-hand side is public — the two hashes are the
    messages, and the two `s` values came with the signatures.

    Then put *k* back into either original equation and solve for *d*:

    ```
    s₁ · k  =  z₁ + r·d

    d  =  ( s₁·k − z₁ ) · r⁻¹
    ```

    And that is the private key.

    **A worked example**, with real secp256k1 values. One key signs "pay Anna
    1 ether" and "pay Bob 2 ether", reusing *k*:

    ```
    r   (identical in both)  fd1b7de8c449eecd…
    s₁                       e1df25a5e5f1ccc9…
    s₂                       e78cef03efaf0bd8…

    recovered d  1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
    actual    d  1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
    ```

    Note that `r` being the same in two signatures is **visible to anyone**.
    It's the public signal that this attack is available.

    **This is not hypothetical.** Sony's PlayStation 3 code-signing key was
    recovered in 2010 in exactly this way — the same *k* on every signature.
    In 2013 a flaw in Android's random number generator made Bitcoin wallets
    repeat nonces, and keys were emptied.

    Which is why serious implementations don't leave *k* to chance at all.
    **RFC 6979** [(Pornin, 2013)](#ref-rfc6979) derives it deterministically
    from the private key and the message hash: the same message always gives
    the same *k*, two different messages never do, and no random number
    source is involved anywhere.

## How the signer is recovered

The third operation, and the reason a transaction needs no sender field at all.

### Why not simply verify the signature?

A fair objection, and worth answering before going further: **verification would work perfectly well.** It's what the rest of the internet does. So why does Ethereum bother with recovery?

Because verification needs the public key, and recovery doesn't.

Look again at what each operation takes in:

```
    verifying:    message hash  +  r, s  +  public key   ──►   yes or no
    recovering:   message hash  +  r, s  +  v            ──►   the public key
```

To verify, you must already **have** the public key. On the open internet that's usually free — a TLS certificate hands it to you, having been issued in advance by somebody you trust. Ethereum has no certificates and no issuers, so there's nowhere for a verifier to get your public key from. It would have to **travel with every transaction.**

And that costs:

| | Bytes carried |
| --- | --- |
| `r` and `s` | 64 |
| **plus a public key**, to verify | **+ 64** |
| **plus `v`**, to recover | **+ 1** |

So verification would cost **128 bytes** of signature data per transaction, where recovery costs **65**. Sixty-three bytes saved, every transaction, forever, in storage held by thousands of nodes.

Put against a whole transaction the difference is stark. A plain ether transfer is on the order of 110 bytes; carrying the public key would push it past 170 — **more than half again as large**, for information the network can work out by itself.

That's the trade. One extra byte of `v` instead of sixty-four bytes of public key, paid for with a slightly more involved calculation. On a system where every byte is stored permanently and everywhere, it's not a close call.

??? abstract "Is recovery slower than verification?"

    Not meaningfully. Verification works out to two point multiplications;
    recovery needs a modular square root to rebuild **R** from `r`, plus
    comparable multiplication. The same order of work either way.

    Which is why the decision came down to bytes rather than speed. Had
    recovery been dramatically more expensive, 64 bytes might have been the
    cheaper thing to pay.

### So Ethereum never verifies a transaction signature at all

Worth being precise about, because the natural assumption is that recovery happens *first* and verification *then* confirms it. It doesn't. **Recovery stands in place of verification**, and the verification step simply doesn't exist.

Compare the two mental models:

```
    the familiar one      "here is the claimed sender —
                           check the signature matches them"

    Ethereum's            "here is a signature —
                           it determines who the sender is"
```

In the first, there are two pieces of information that might disagree, so there's a check, and the check can fail. In the second **there is only one piece of information.** The sender isn't claimed and then confirmed; the sender is *defined* as whoever the signature recovers to.

So the question "is this signature valid for this sender?" is never asked — and therefore can never fail. That's why, as the tool below shows, a tampered message doesn't produce an invalid-signature error. There's no such error to produce. It produces a different sender.

#### Which is not the same as saying nothing gets checked

An important line to draw, because "verification" covers two different jobs and this page only ever discusses one of them.

**Signature verification** asks a single narrow question: did the holder of this key sign this exact data? That's the cryptographic operation, and it's the only thing recovery replaces.

**Transaction validation** asks whether the transaction is acceptable at all — and that happens in full, every time, unchanged.

And look at what those checks need:

| Check a node makes | Needs to know the sender? |
| --- | --- |
| Is the encoding well-formed? | no |
| Are `r` and `s` in range, with `s` in the lower half? | no |
| **← recovery happens here** | |
| Does the nonce match **this account's** next expected nonce? | **yes** |
| Does **this account's** balance cover the value plus the fee? | **yes** |
| Is the gas limit sane, and the chain id right? | no |

Most of the substantive checks are **about the sender** — their nonce, their balance. So none of them can run until recovery has worked out who that is.

Which recasts the whole section: recovery isn't an alternative to checking a transaction. **It's the step that makes checking possible.** It answers *who*, and everything else is then checked against that answer.

??? note "Valid, versus included-and-failed"

    Worth separating while the distinction is in view, because the two get
    conflated constantly.

    - **Invalid** — fails one of the checks above. Never enters a block,
      costs nothing, as though it never existed.
    - **Valid but failed** — passes every check, is included in a block, and
      then fails *during execution*: it runs out of gas, or the contract
      rejects what it was asked to do. It happened. It's permanent. **You
      paid for it.**

    A failed transaction is not a rejected one. The work was genuinely
    performed by every node on the network, so the fee is genuinely owed. Why
    that has to be the case is the subject of
    [why metering is necessary](../transactions/why-metering.md).


??? note "A few things can still fail outright"

    Recovery replaces the signature check, but it doesn't make a transaction
    unconditionally acceptable. Some structural conditions remain, and a
    transaction breaking any of them is rejected before recovery is even
    attempted:

    - `r` and `s` must each be at least 1 and below the curve order
    - `s` must be in the lower half of its range, per
      [EIP-2](#ref-eip2) — see [malleability](#malleability-and-why-s-has-to-be-small)
    - `r` must actually be the x coordinate of a point on the curve, or
      there is no **R** to rebuild and recovery has nothing to work with

    These are checks on whether the numbers are *well-formed*, not on whether
    they're *yours*. Nothing here compares anything to a sender.

### Where a comparison does happen

One exception worth knowing, because it's the case you'll meet as a user.

When a website asks you to sign a phrase to log in, it **does** compare. It knows which address it expects — the one you claimed to own — so it recovers the address from your signature and checks the two match. That's a genuine verification, built out of recovery.

The difference is that the site has an expectation to test against. A node processing a transaction has none, and needs none.

### Why recovery is possible at all

Here is the part worth understanding, because it looks like magic and isn't.

**Verification and recovery are the same equation, solved for different unknowns.**

ECDSA's check is a relationship between four things: the message hash, `r`, `s`, and the public key **Q**. Ordinarily you are handed all four, substitute them in, and see whether the relationship holds — that's verification.

But an equation with one unknown can be rearranged. Leave **Q** out, and the relationship can be solved *for* **Q** instead:

```
    Q  =  r⁻¹ ( s·R  −  z·G )
```

where **R** is the point whose x coordinate is `r`. Everything on the right is public: `r` and `s` come with the signature, *z* is the message hash, G is the fixed generator. So the public key falls out directly.

Recovery isn't a feature bolted onto ECDSA. It's the same algebra read in the other direction — and since the signing equation is written out above, that claim can be checked rather than taken on faith.

??? abstract "The formal version: from the signing equation to Q, in six lines"

    Start from the equation in the previous section, and remember that the
    public key is **Q = d·G**.

    ```
    s   =  k⁻¹ ( z + r·d )          the signing equation

    s·k =  z + r·d                  multiply both sides by k

    k   =  s⁻¹ ( z + r·d )          divide by s instead

    R   =  k·G
        =  s⁻¹ ( z·G + r·d·G )      multiply through by G
        =  s⁻¹ ( z·G + r·Q )        because d·G is just Q

    s·R =  z·G + r·Q                multiply by s

    r·Q =  s·R − z·G                move z·G across

    Q   =  r⁻¹ ( s·R − z·G )        divide by r
    ```

    Six steps of ordinary rearrangement, and nothing cleverer than multiplying
    both sides by the same thing. The only substitution that matters is
    **d·G = Q** on line four: that's where the private key disappears and the
    public key takes its place.

    Which is the whole point. The signer's equation and the verifier's are the
    same statement; the signer knows *d* and *k* and solves for `s`, while
    everyone else knows `s` and solves for **Q**.

    All of this was checked numerically before publication: both the signing
    equation and the final rearrangement hold for every random key, nonce and
    message tried.

### Which is where `v` comes in

One snag. Recovery needs the point **R**, and the signature only gives you `r` — its *x* coordinate. As the [public keys](public-keys.md) page showed, an *x* coordinate has **two** possible *y* values, one even and one odd.

Two candidate points give two candidate public keys, and so two candidate addresses. Only one of them signed.

So **`v` is one bit saying which**: the *y* was even, or the *y* was odd. That's its whole job. Without it you'd recover two addresses with no way to choose between them.

??? info "History: `v` used to carry more than one bit"

    In early Ethereum, `v` was 27 or 28 — the parity bit plus an offset
    inherited from Bitcoin.

    Then came a problem. A transaction signed for Ethereum was equally valid on
    any other chain using the same curve, so a payment could be taken from one
    network and replayed on another, where the same key controlled the same
    address. **EIP-155** [(Buterin, 2016)](#ref-eip155) fixed it by folding the
    **chain id** — a number identifying which network a signature is for — into
    `v`, so a signature became valid on exactly one chain.

    Modern typed transactions dropped that trick. They carry the chain id as
    its own field and store the parity plainly as 0 or 1 — which is what the
    tool below shows. Cleaner, and the same protection.

    So if you meet `v = 27`, `v = 37` and `v = 1` in different places, none is
    wrong; they're three generations of the same bit.

### Recovering an address, step by step

Spelled out as a procedure, so the tool below isn't a black box:

```
recover(message, r, s, v):

    1.  z  =  keccak256(message)        the hash that was actually signed

    2.  R  =  the curve point whose x coordinate is r
              — two points qualify, one with even y and one with odd,
                so use v to pick the right one

    3.  Q  =  r⁻¹ · ( s·R  −  z·G )     solve the signing relation for Q

    4.  address = last 20 bytes of keccak256(Q)
```

Step 3 is the rearrangement from above. Step 4 is the [addresses](addresses.md) page, unchanged.

Notice what goes **in**: a message, and three numbers. Every one of them public. No key, no secret, nothing that has to be kept safe — which is exactly why any stranger can run this, and why every node does.

### Nothing in this is secret

Worth pausing on, because signing is routinely confused with encrypting.

**The message is public.** A transaction is broadcast to every node on the network in plain text — the amount, the recipient, the data, all of it readable by anyone. Nothing is encrypted at any stage. A block explorer showing you somebody's transfers isn't breaking anything; it's reading what was published.

What a signature provides isn't secrecy, it's **authorship**. It answers *who authorised this*, not *what does it say*. Those are different questions, and Ethereum only needs the first one answered.

The only secret anywhere is the private key, and it never leaves your machine. What travels is `r` and `s`, which [reveal nothing about it](private-keys.md).

So when the tool below hands the verifier the message openly, that isn't a simplification for the demonstration — it's how the system works. **If the message were secret nobody could check it was valid**, and a network that can't check transactions has nothing to agree on.

This page doesn't derive any of it. The three properties from the [private keys](private-keys.md) page are what matter: anyone can check it, it reveals nothing about the key, and it's bound to one message.

??? example "Try it: sign, then recover the signer"

    <div class="tool" markdown="0">
      <label for="sig-msg">Message to sign</label>
      <input id="sig-msg" type="text" autocomplete="off" spellcheck="false" value="send 1 ether to Anna">
      <label for="sig-key">Private key (hex)</label>
      <input id="sig-key" type="text" autocomplete="off" spellcheck="false" value="1">
      <button id="sig-again" type="button">Sign again</button>
      <label for="sig-check">Message the verifier checks</label>
      <input id="sig-check" type="text" autocomplete="off" spellcheck="false" value="send 1 ether to Anna">
      <p class="tool__out" id="sig-out"></p>
    </div>

    **Step 1 — note what the verifier was *not* given.** Not the address, not
    the public key, not any claim about who signed. Just the message — public,
    as always — and three numbers. The address underneath is computed from
    those alone, and it matches.

    **Step 2 — press Sign again**, several times. The signature changes
    completely every time, and **the recovered address never does.** That's
    *k* being fresh on each signature, and it's the claim from the private
    keys page made concrete: a signature is computed, not held.

    **Step 3 — alter the lower field only**, so the verifier checks a
    different message from the one that was signed. Change "Anna" to "Anne",
    or 1 ether to 2.

    **Recovery doesn't fail. It returns a different address.** That's the
    surprising part, and it's worth following through why.

    1. The signature was computed over `keccak256("…to Anna")`.
    2. The verifier now computes `keccak256("…to Anne")` — a completely
       different *z*, because of [avalanche](keccak256.md).
    3. Step 3 of the procedure above uses *z*. Feed in a different *z* and the
       equation returns a different **Q**.
    4. That **Q** is a perfectly valid point on the curve, so it's a perfectly
       valid public key, which gives a perfectly valid-looking address. Just
       not the signer's.

    **So there is no error state, and there couldn't be.** Recovery isn't
    checking anything — it has no idea what answer was expected, and nothing
    to compare against. It is a calculation, and it always returns an answer.
    Tamper with the message and the answer is simply a different address.

    Which raises the obvious question: if nothing fails, what stops the
    tampering working?

    **The address it recovers to is a random point in a space of 2¹⁶⁰.**
    Essentially certainly, nobody holds the key for it, it has never been
    used, and it holds no ether. So when a node treats that address as the
    sender — as [it must](#a-transaction-never-says-who-sent-it) — it finds an
    account with a nonce of zero and a balance of nothing, and rejects the
    transaction for the dullest possible reasons: wrong nonce, can't pay the
    fee.

    The tampering fails, but not because a signature check said "invalid".
    It fails because the altered transaction is now claimed by a stranger who
    has no funds and no history. Which is a stronger guarantee than a check,
    because there's nothing to get wrong.

## Replay protection needs two different things

A signed transaction is a standing instruction. Unless something stops it, anyone who has seen it can submit it again — and it will still be valid, because it's still correctly signed by you. Two different versions of that problem exist, and each needs its own defence.

**Replayed on the same chain.** Someone rebroadcasts your payment hoping it executes twice. The [nonce](../accounts/nonce.md "A per-account counter of transactions already sent") stops this: it's part of what you signed, and once a nonce has been used the network will never accept it again.

**Replayed on a different chain.** This one is less obvious. Ethereum isn't the only network using secp256k1 and this address format — there are testnets, forks such as Ethereum Classic, and unrelated chains built the same way. **Your key controls the same address on all of them.** So a transaction you signed for one network could be lifted and submitted on another, where it would verify perfectly and move real funds.

The defence is the **chain id**: a number identifying the network, included in what gets signed. Sign with Ethereum's chain id and the signature simply isn't valid anywhere else.

| Attack | Defence |
| --- | --- |
| Rebroadcasting your transaction **on this chain** | the **nonce** — once used, that number is spent forever |
| Replaying it **on another chain** | the **chain id** — the signature is valid on one network only |

Neither covers the other. A nonce means nothing across chains, since the other chain keeps its own count. A chain id does nothing about the same transaction being submitted twice on the network it belongs to.

## Malleability, and why `s` has to be small

A quirk with real consequences.

For any valid signature `(r, s)`, the value `(r, n − s)` is **also** a valid signature over the same message — where *n* is the order of secp256k1, the same constant from the [private keys](private-keys.md) page that bounds a valid key. The underlying maths is symmetric, so flipping `s` to the other side of the range and flipping `v` to compensate gives a second, equally valid signature.

Two things make that matter.

**First, anyone can do the flip.** It takes no private key — only arithmetic on a signature you've already seen. So any node relaying your transaction can alter it this way, and the result still verifies as yours.

**Second, a transaction is identified by its hash, and that hash covers the signature.** Change `s`, and you change the transaction's bytes, and therefore its hash — while the transaction still does exactly the same thing on behalf of exactly the same sender.

So before EIP-2, this could happen:

1. You broadcast a payment. Your wallet notes its hash — call it **H1** — because that's how you track a transaction.
2. Some node along the way flips `s`, producing a byte-for-byte different transaction with hash **H2**. Still your payment. Still validly signed by you. Different hash.
3. **H2** is the version that gets included in a block.
4. Your wallet waits for H1. It never appears. As far as the wallet can tell, the payment never happened.
5. So it reports a failure — and if anything automatically retries, you pay twice.

The payment went through the whole time. The accounting was looking for the wrong name for it.

**EIP-2** [(Buterin, 2015)](#ref-eip2) closed this by requiring `s` to lie in the **lower half** of its range. Of the two equivalent signatures, exactly one qualifies, so there is only ever one valid encoding and only one possible hash. The tool above applies that normalisation — press *Sign again* a few times and `s` always starts with a hex digit below `8`.

## Signing things that aren't transactions

A private key will sign any bytes you give it, and plenty of uses have nothing to do with the chain.

"Sign in with your wallet" works this way: a site gives you a phrase, you sign it, and the site recovers your address. No transaction, no gas, no block — just a signature and a recovery, exactly as in the tool above.

??? warning "Which is why a signing prompt deserves reading"

    Because a signature authorises whatever was signed, and your wallet can
    only show you the bytes.

    **ERC-191** [(Van de Sande et al., 2016)](#ref-eip191) protects against one
    specific confusion: a phrase you sign being replayed as a *transaction*
    you never authorised. It does so by prefixing the message before hashing.
    For ordinary personal messages the prefix is:

    ```
    \x19  "Ethereum Signed Message:\n"  <length of the message>
    ```

    So signing `hello` actually hashes
    `\x19Ethereum Signed Message:\n5hello`, not `hello`.

    The leading byte is the load-bearing part. `0x19` cannot begin a valid
    transaction encoding, so the bytes you signed are **structurally incapable**
    of being a transaction. The signature therefore cannot be lifted out and
    presented as authorisation to move funds. The length is included so one
    message can't be reinterpreted as a different, shorter one.

    That's genuine, and it's narrow: it stops signed messages masquerading as
    transactions. It does nothing about a message that is plainly a message and
    still signs away something you didn't intend — which is why reading the
    prompt still matters.

    The tool above hashes the message directly, with no prefix, to keep the
    demonstration about signing rather than about framing.

---

## Recap

- **A transaction has no sender field.** The address is recovered from the signature, so the signature *is* the claim of identity.
- What's signed is the **hash of the transaction**, which protects every field at once.
- `r` and `s` are the signature; `v` is one bit saying which of two possible public keys to recover.
- **Verification would have worked too** — but it needs the public key, and Ethereum has no certificates to supply one. Recovery buys the same guarantee for one byte of `v` instead of 64 bytes of public key in every transaction.
- So Ethereum **never verifies a transaction signature**. Recovery replaces that step: the sender isn't claimed and then checked, it's *defined* as whoever the signature recovers to. A comparison only happens where something has an expectation to test — signing in to a website, for instance.
- That is **not** the same as nothing being checked. Nonce, balance, gas limit and chain id are all still validated — and most of them need the sender, so recovery is what makes those checks possible rather than a substitute for them.
- **The same message signed twice gives different signatures**, both recovering the same address.
- A tampered message recovers **a different address**, not an error — nothing in a signature says whose it should have been.
- Replay needs two defences: the **nonce** within a chain, the **chain id** across chains.
- `s` is restricted to its lower half, because otherwise one transaction would have two valid hashes.

**Next:** [Wallets and seed phrases](../wallets/seed-phrases.md) — where the keys actually come from.

---

## References

<div class="sources" markdown>

- <a id="ref-eip2"></a>**Buterin, V.** (2015). *EIP-2: Homestead hard-fork changes.* Ethereum Improvement Proposals. Among other changes, requires the signature value *s* to lie in the lower half of its range, removing signature malleability. <https://eips.ethereum.org/EIPS/eip-2>
- <a id="ref-eip155"></a>**Buterin, V.** (2016). *EIP-155: Simple replay attack protection.* Ethereum Improvement Proposals. Folds the chain id into the signature so a transaction is valid on one network only. <https://eips.ethereum.org/EIPS/eip-155>
- <a id="ref-rfc6979"></a>**Pornin, T.** (2013). *Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA).* RFC 6979, Internet Engineering Task Force. Derives the per-signature nonce from the key and message, removing the reuse failure described above. <https://www.rfc-editor.org/rfc/rfc6979>
- <a id="ref-sec1"></a>**Standards for Efficient Cryptography Group** (2009). *SEC 1: Elliptic Curve Cryptography*, version 2.0. Specifies ECDSA signing, verification and public key recovery. <https://www.secg.org/sec1-v2.pdf>
- <a id="ref-eip191"></a>**Van de Sande, A., Nita-Rotaru, C., & Logvinov, L.** (2016). *ERC-191: Signed data standard.* Ethereum Improvement Proposals. Prefixes signed messages so they cannot be confused with signed transactions. <https://eips.ethereum.org/EIPS/eip-191>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Appendix F defines the recovery function used to obtain a sender address from a signature. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
