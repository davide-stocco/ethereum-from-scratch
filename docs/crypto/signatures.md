---
tier: 1
description: How a signature proves you hold a private key, and how the sender's address is recovered from the signature rather than stated anywhere.
---

# Signatures

**Fork-proof.** ECDSA over secp256k1, unchanged since genesis.

The [private keys](private-keys.md) page described what a signature is *for*: proving you know a secret without revealing it. This page is about how Ethereum actually uses that — and it opens with the fact that surprises nearly everyone.

!!! definition "Signature"

    Three numbers — `v`, `r` and `s` — computed from a message and a
    [private key](private-keys.md). They prove that the key's holder
    authorised **that exact message**, while revealing nothing about the key.

    On Ethereum they do one thing more: the signer's
    [address](addresses.md) can be **recovered** from them. Which is why a
    transaction never has to state who sent it.

## A transaction never says who sent it

Transactions get a page of their own later. Only one thing about them matters here.

A transaction is a short list of fields — how much, to whom, what data, how much fee — followed by three numbers called `v`, `r` and `s`, which together are the signature.

**There is no "from" field.** Nowhere does a transaction state its sender.

Instead, the sender's address is **recovered** from the signature. Given the signed message and those three numbers, anyone can compute the public key that must have produced them — and from that, [the address](addresses.md).

This isn't optional or occasional. When a node receives a transaction it has to establish who sent it before it can do anything at all: whose balance to check, whose [account nonce](../accounts/nonce.md "A per-account counter of transactions already sent") to compare against, whose account to take the fee from. Recovery is how it finds out, so every node runs it on every transaction it ever sees. The Yellow Paper defines the function for exactly this purpose [(Wood, 2014)](#ref-wood-2014).

So the signature doesn't *accompany* a claim of identity. The signature **is** the claim.

Which is rather elegant once it lands. A forged "from" field would be worthless, so Ethereum doesn't have one. The only way to appear as the sender of a transaction is to produce a signature that recovers to your address, and the only way to do that is to hold the key.

## What actually gets signed

Not the transaction — the **hash** of the transaction, via [Keccak-256](keccak256.md).

That has a useful consequence. Since the hash covers every field, changing any single byte of the transaction changes the hash, and a signature over the old hash recovers to a different address. So the signature protects **all** of it at once: the amount, the recipient, the fee, the account nonce. There's no need to sign each field separately, and no way to alter one in transit.

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

1. Pick a **random secret number**, called *k*, used once and then thrown away. It has a second name you'll meet constantly — the **signing nonce** — on which see the warning below.
2. Compute the curve point *k* × G, the same multiplication from the [public keys](public-keys.md) page. Call it **R**.
3. **`r` is the x coordinate of R.**
4. **`s` is computed from** the message hash, `r`, the private key and *k*:

```
    s  =  k⁻¹ ( z  +  r · d )      mod n
```

Every term there has already appeared on this site:

| Symbol | What it is |
| --- | --- |
| *z* | the message hash, from [Keccak-256](keccak256.md) |
| *d* | the private key — the only secret in the equation |
| *r* | the x coordinate from step 3 |
| *k* | the random number from step 1, also called the signing nonce |
| *n* | secp256k1's order, from the [private keys](private-keys.md) page |

*k*⁻¹ means the modular inverse — the number that multiplies by *k* to give 1, working modulo *n*. Not a fraction; there are no fractions anywhere in this.

So the two halves have distinct jobs. `r` is a commitment to the random point: it depends on *k* and nothing else. `s` is the half the **private key enters**, mixed with the message hash so that the pair is bound to this message and no other.

And notice that *d* appears exactly once, multiplied by *r* and buried under a *k*⁻¹ you don't know. That's what makes the equation safe to publish.

Neither value reveals *d*, and neither reveals *k*. And because *k* is fresh every time, `r` and `s` are completely different on every signature — which is what you see when you press *Sign again* below.

### Two different things get called a nonce

Worth separating before going on, because this page needs both senses and they could hardly be less alike.

| | What it is | Secret? | Chosen how |
| --- | --- | --- | --- |
| ***k***, the **signing nonce** | the random value above, thrown away immediately | **yes**, always | unpredictably, never repeating |
| the **account nonce** | a counter of transactions an account has sent, checked when a transaction is validated | no | by counting |

They share only the literal sense of the word: *number used once*. Everything else is opposed — one must be unguessable or your key is recoverable, the other must be guessable or your wallet couldn't build a transaction. The account one has [its own page](../accounts/nonce.md) and appears later in this one, when we get to what a node checks.

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
    repeat *k*, and keys were emptied.

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

Worth being precise about, because the natural assumption is that recovery happens *first* and verification *then* confirms it. It doesn't — and the cleanest way to say why is this:

> **Verification is recovery followed by a comparison.**
>
> Recover the public key from the signature, then check it's the one you were expecting. Ethereum does the recovery and has **nothing to compare against**, so it stops there.

That matters because it settles the obvious worry. Skipping the comparison isn't a weakened check — the two operations establish exactly the same fact, and verification succeeds precisely when recovery returns the expected key. There is no version of this where a forgery slips through recovery but would have been caught by verification. The comparison is omitted because there's no expectation to test, not because a check was dropped.

Compare the two mental models:

```
    the familiar one      "here is the claimed sender —
                           check the signature matches them"

    Ethereum's            "here is a signature —
                           it determines who the sender is"
```

In the first, there are two pieces of information that might disagree, so there's a check, and the check can fail. In the second **there is only one piece of information.** The sender isn't claimed and then confirmed; the sender is *defined* as whoever the signature recovers to.

So the question "is this signature valid for this sender?" is never asked — and therefore can never fail. That's why, as the tool below shows, a tampered message doesn't produce an invalid-signature error. There's no such error to produce. It produces a different sender.

??? failure "A few things can still fail outright"

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

#### Which is not the same as saying nothing gets checked

An important line to draw, because "verification" covers two different jobs and this page only ever discusses one of them.

**Signature verification** asks a single narrow question: did the holder of this key sign this exact data? That's the cryptographic operation, and it's the only thing recovery replaces.

**Transaction validation** asks whether the transaction is acceptable at all — and that happens in full, every time, unchanged.

And here is the part that matters. Some of those checks can be made by looking at the transaction on its own. Others are **about the sender** — and so cannot even be attempted until recovery has worked out who the sender is:

| What the node asks | Can it ask yet? |
| --- | --- |
| Is this well-formed — the right fields, the right shape? | yes |
| Are the signature's numbers within their permitted range? | yes |
| **← recovery happens here, and produces an address** | |
| Has this account already used this transaction number? | only now |
| Does this account hold enough ether to pay? | only now |
| Is the offered fee acceptable to the network? | yes |
| Is this transaction even meant for this network? | yes |

Which recasts the whole section. Recovery isn't an alternative to checking a transaction — **it's the step that makes the important checks possible at all.** It answers *who*, and the account-specific questions are then asked of that answer.

??? note "The proper names for those checks"

    Each of those questions has a technical name, and each gets a page of its
    own later. Listed here so the terms aren't a surprise when you meet them:

    | The question | What it's called |
    | --- | --- |
    | Has this account already used this transaction number? | the [account nonce](../accounts/nonce.md "A per-account counter of transactions already sent") |
    | Does this account hold enough ether to pay? | the [balance](../glossary.md#balance "How much ether an account holds, counted in wei") |
    | Is the offered fee acceptable? | [gas](../glossary.md#gas "The unit computational work is measured in") limits and fee parameters |
    | Is this meant for this network? | the [chain id](../glossary.md#chain-id "A number identifying which network a transaction is for") |

    The glossary has a one-line definition of each. Nothing on this page
    depends on knowing them — they're here only to show **which** checks need
    a sender and which don't.

??? question "Valid, versus included-and-failed"

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


### Where the comparison does happen

Which brings the other half of that formulation into view, and it's the case you'll meet as a user.

When a website asks you to sign a phrase to log in, it **does** compare. It knows which address it expects — the one you claimed to own — so it recovers the address from your signature and checks the two match.

That is **verification**, assembled exactly as described above: recovery, then a comparison. Not a different mechanism, and not an exception to anything. The site simply has an expectation to test, so it performs the second step that a node processing a transaction has no use for.

So the same operation underlies both. What differs is only whether anyone had an answer in mind beforehand.

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
    equation and the final rearrangement hold for every random key, *k* and
    message tried.

### Which is where `v` comes in

One snag. Recovery needs the point **R**, and the signature only gives you `r` — its *x* coordinate. As the [public keys](public-keys.md) page showed, an *x* coordinate has **two** possible *y* values, one even and one odd.

<svg viewBox="0 0 430 296" role="img" aria-label="The curve y squared equals x cubed plus seven, drawn as two separate branches above and below the horizontal axis. A vertical dashed line at x equals r crosses it at two points. Both share the same x coordinate, so r alone cannot say which point was used; one has an even y and the other an odd y." style="width:100%;max-width:27rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><path d="M20 140 L410 140" opacity="0.3"/><path d="M161 26 L161 268" opacity="0.3"/><path d="M47.1 140.0 L48.3 133.0 L49.5 130.2 L50.7 128.0 L51.9 126.2 L53.1 124.7 L54.3 123.3 L55.5 122.1 L56.7 120.9 L57.8 119.9 L59.0 118.9 L60.2 118.0 L61.4 117.2 L62.6 116.4 L63.8 115.6 L65.0 114.9 L66.2 114.2 L67.4 113.6 L68.6 112.9 L69.8 112.4 L71.0 111.8 L72.2 111.3 L73.4 110.7 L74.6 110.3 L75.8 109.8 L76.9 109.3 L78.1 108.9 L79.3 108.5 L80.5 108.1 L81.7 107.7 L82.9 107.4 L84.1 107.0 L85.3 106.7 L86.5 106.3 L87.7 106.0 L88.9 105.7 L90.1 105.5 L91.3 105.2 L92.5 104.9 L93.7 104.7 L94.9 104.4 L96.1 104.2 L97.2 104.0 L98.4 103.8 L99.6 103.6 L100.8 103.4 L102.0 103.2 L103.2 103.0 L104.4 102.8 L105.6 102.7 L106.8 102.5 L108.0 102.4 L109.2 102.2 L110.4 102.1 L111.6 102.0 L112.8 101.9 L114.0 101.8 L115.2 101.6 L116.4 101.5 L117.5 101.4 L118.7 101.4 L119.9 101.3 L121.1 101.2 L122.3 101.1 L123.5 101.0 L124.7 101.0 L125.9 100.9 L127.1 100.9 L128.3 100.8 L129.5 100.7 L130.7 100.7 L131.9 100.7 L133.1 100.6 L134.3 100.6 L135.5 100.5 L136.6 100.5 L137.8 100.5 L139.0 100.5 L140.2 100.4 L141.4 100.4 L142.6 100.4 L143.8 100.4 L145.0 100.4 L146.2 100.4 L147.4 100.3 L148.6 100.3 L149.8 100.3 L151.0 100.3 L152.2 100.3 L153.4 100.3 L154.6 100.3 L155.8 100.3 L156.9 100.3 L158.1 100.3 L159.3 100.3 L160.5 100.3 L161.7 100.3 L162.9 100.3 L164.1 100.3 L165.3 100.3 L166.5 100.3 L167.7 100.3 L168.9 100.3 L170.1 100.3 L171.3 100.3 L172.5 100.3 L173.7 100.3 L174.9 100.3 L176.1 100.3 L177.2 100.3 L178.4 100.2 L179.6 100.2 L180.8 100.2 L182.0 100.2 L183.2 100.2 L184.4 100.1 L185.6 100.1 L186.8 100.1 L188.0 100.1 L189.2 100.0 L190.4 100.0 L191.6 99.9 L192.8 99.9 L194.0 99.9 L195.2 99.8 L196.3 99.7 L197.5 99.7 L198.7 99.6 L199.9 99.6 L201.1 99.5 L202.3 99.4 L203.5 99.3 L204.7 99.2 L205.9 99.1 L207.1 99.1 L208.3 99.0 L209.5 98.9 L210.7 98.7 L211.9 98.6 L213.1 98.5 L214.3 98.4 L215.5 98.3 L216.6 98.1 L217.8 98.0 L219.0 97.8 L220.2 97.7 L221.4 97.5 L222.6 97.4 L223.8 97.2 L225.0 97.0 L226.2 96.8 L227.4 96.6 L228.6 96.4 L229.8 96.2 L231.0 96.0 L232.2 95.8 L233.4 95.6 L234.6 95.4 L235.8 95.2 L236.9 94.9 L238.1 94.7 L239.3 94.4 L240.5 94.2 L241.7 93.9 L242.9 93.6 L244.1 93.4 L245.3 93.1 L246.5 92.8 L247.7 92.5 L248.9 92.2 L250.1 91.9 L251.3 91.6 L252.5 91.3 L253.7 90.9 L254.9 90.6 L256.0 90.3 L257.2 89.9 L258.4 89.6 L259.6 89.2 L260.8 88.8 L262.0 88.5 L263.2 88.1 L264.4 87.7 L265.6 87.3 L266.8 86.9 L268.0 86.5 L269.2 86.1 L270.4 85.7 L271.6 85.3 L272.8 84.9 L274.0 84.4 L275.2 84.0 L276.3 83.6 L277.5 83.1 L278.7 82.7 L279.9 82.2 L281.1 81.7 L282.3 81.3 L283.5 80.8 L284.7 80.3 L285.9 79.8 L287.1 79.3 L288.3 78.8 L289.5 78.3 L290.7 77.8 L291.9 77.3 L293.1 76.8 L294.3 76.3 L295.5 75.8 L296.6 75.2 L297.8 74.7 L299.0 74.1 L300.2 73.6 L301.4 73.0 L302.6 72.5 L303.8 71.9 L305.0 71.3 L306.2 70.8 L307.4 70.2 L308.6 69.6 L309.8 69.0 L311.0 68.4 L312.2 67.8 L313.4 67.2 L314.6 66.6 L315.7 66.0 L316.9 65.4 L318.1 64.8 L319.3 64.2 L320.5 63.6 L321.7 62.9 L322.9 62.3 L324.1 61.7 L325.3 61.0 L326.5 60.4 L327.7 59.7 L328.9 59.1 L330.1 58.4 L331.3 57.7 L332.5 57.1 L333.7 56.4 L334.9 55.7 L336.0 55.0 L337.2 54.4 L338.4 53.7 L339.6 53.0 L340.8 52.3 L342.0 51.6 L343.2 50.9 L344.4 50.2 L345.6 49.5 L346.8 48.8 L348.0 48.0 L349.2 47.3 L350.4 46.6 L351.6 45.9 L352.8 45.1 L354.0 44.4 L355.2 43.7 L356.3 42.9 L357.5 42.2 L358.7 41.4 L359.9 40.7 L361.1 39.9 L362.3 39.2 L363.5 38.4 L364.7 37.7 L365.9 36.9 L367.1 36.1 L368.3 35.3 L369.5 34.6 L370.7 33.8 L371.9 33.0 L373.1 32.2 L374.3 31.4 L375.4 30.6 L376.6 29.8 L377.8 29.0 L379.0 28.2 L380.2 27.4 L381.4 26.6 L382.6 25.8 L383.8 25.0 L385.0 24.2 L386.2 23.4 L387.4 22.5 L388.2 22.0" stroke-width="1.4"/><path d="M47.1 140.0 L48.3 147.0 L49.5 149.8 L50.7 152.0 L51.9 153.8 L53.1 155.3 L54.3 156.7 L55.5 157.9 L56.7 159.1 L57.8 160.1 L59.0 161.1 L60.2 162.0 L61.4 162.8 L62.6 163.6 L63.8 164.4 L65.0 165.1 L66.2 165.8 L67.4 166.4 L68.6 167.1 L69.8 167.6 L71.0 168.2 L72.2 168.7 L73.4 169.3 L74.6 169.7 L75.8 170.2 L76.9 170.7 L78.1 171.1 L79.3 171.5 L80.5 171.9 L81.7 172.3 L82.9 172.6 L84.1 173.0 L85.3 173.3 L86.5 173.7 L87.7 174.0 L88.9 174.3 L90.1 174.5 L91.3 174.8 L92.5 175.1 L93.7 175.3 L94.9 175.6 L96.1 175.8 L97.2 176.0 L98.4 176.2 L99.6 176.4 L100.8 176.6 L102.0 176.8 L103.2 177.0 L104.4 177.2 L105.6 177.3 L106.8 177.5 L108.0 177.6 L109.2 177.8 L110.4 177.9 L111.6 178.0 L112.8 178.1 L114.0 178.2 L115.2 178.4 L116.4 178.5 L117.5 178.6 L118.7 178.6 L119.9 178.7 L121.1 178.8 L122.3 178.9 L123.5 179.0 L124.7 179.0 L125.9 179.1 L127.1 179.1 L128.3 179.2 L129.5 179.3 L130.7 179.3 L131.9 179.3 L133.1 179.4 L134.3 179.4 L135.5 179.5 L136.6 179.5 L137.8 179.5 L139.0 179.5 L140.2 179.6 L141.4 179.6 L142.6 179.6 L143.8 179.6 L145.0 179.6 L146.2 179.6 L147.4 179.7 L148.6 179.7 L149.8 179.7 L151.0 179.7 L152.2 179.7 L153.4 179.7 L154.6 179.7 L155.8 179.7 L156.9 179.7 L158.1 179.7 L159.3 179.7 L160.5 179.7 L161.7 179.7 L162.9 179.7 L164.1 179.7 L165.3 179.7 L166.5 179.7 L167.7 179.7 L168.9 179.7 L170.1 179.7 L171.3 179.7 L172.5 179.7 L173.7 179.7 L174.9 179.7 L176.1 179.7 L177.2 179.7 L178.4 179.8 L179.6 179.8 L180.8 179.8 L182.0 179.8 L183.2 179.8 L184.4 179.9 L185.6 179.9 L186.8 179.9 L188.0 179.9 L189.2 180.0 L190.4 180.0 L191.6 180.1 L192.8 180.1 L194.0 180.1 L195.2 180.2 L196.3 180.3 L197.5 180.3 L198.7 180.4 L199.9 180.4 L201.1 180.5 L202.3 180.6 L203.5 180.7 L204.7 180.8 L205.9 180.9 L207.1 180.9 L208.3 181.0 L209.5 181.1 L210.7 181.3 L211.9 181.4 L213.1 181.5 L214.3 181.6 L215.5 181.7 L216.6 181.9 L217.8 182.0 L219.0 182.2 L220.2 182.3 L221.4 182.5 L222.6 182.6 L223.8 182.8 L225.0 183.0 L226.2 183.2 L227.4 183.4 L228.6 183.6 L229.8 183.8 L231.0 184.0 L232.2 184.2 L233.4 184.4 L234.6 184.6 L235.8 184.8 L236.9 185.1 L238.1 185.3 L239.3 185.6 L240.5 185.8 L241.7 186.1 L242.9 186.4 L244.1 186.6 L245.3 186.9 L246.5 187.2 L247.7 187.5 L248.9 187.8 L250.1 188.1 L251.3 188.4 L252.5 188.7 L253.7 189.1 L254.9 189.4 L256.0 189.7 L257.2 190.1 L258.4 190.4 L259.6 190.8 L260.8 191.2 L262.0 191.5 L263.2 191.9 L264.4 192.3 L265.6 192.7 L266.8 193.1 L268.0 193.5 L269.2 193.9 L270.4 194.3 L271.6 194.7 L272.8 195.1 L274.0 195.6 L275.2 196.0 L276.3 196.4 L277.5 196.9 L278.7 197.3 L279.9 197.8 L281.1 198.3 L282.3 198.7 L283.5 199.2 L284.7 199.7 L285.9 200.2 L287.1 200.7 L288.3 201.2 L289.5 201.7 L290.7 202.2 L291.9 202.7 L293.1 203.2 L294.3 203.7 L295.5 204.2 L296.6 204.8 L297.8 205.3 L299.0 205.9 L300.2 206.4 L301.4 207.0 L302.6 207.5 L303.8 208.1 L305.0 208.7 L306.2 209.2 L307.4 209.8 L308.6 210.4 L309.8 211.0 L311.0 211.6 L312.2 212.2 L313.4 212.8 L314.6 213.4 L315.7 214.0 L316.9 214.6 L318.1 215.2 L319.3 215.8 L320.5 216.4 L321.7 217.1 L322.9 217.7 L324.1 218.3 L325.3 219.0 L326.5 219.6 L327.7 220.3 L328.9 220.9 L330.1 221.6 L331.3 222.3 L332.5 222.9 L333.7 223.6 L334.9 224.3 L336.0 225.0 L337.2 225.6 L338.4 226.3 L339.6 227.0 L340.8 227.7 L342.0 228.4 L343.2 229.1 L344.4 229.8 L345.6 230.5 L346.8 231.2 L348.0 232.0 L349.2 232.7 L350.4 233.4 L351.6 234.1 L352.8 234.9 L354.0 235.6 L355.2 236.3 L356.3 237.1 L357.5 237.8 L358.7 238.6 L359.9 239.3 L361.1 240.1 L362.3 240.8 L363.5 241.6 L364.7 242.3 L365.9 243.1 L367.1 243.9 L368.3 244.7 L369.5 245.4 L370.7 246.2 L371.9 247.0 L373.1 247.8 L374.3 248.6 L375.4 249.4 L376.6 250.2 L377.8 251.0 L379.0 251.8 L380.2 252.6 L381.4 253.4 L382.6 254.2 L383.8 255.0 L385.0 255.8 L386.2 256.6 L387.4 257.5 L388.2 258.0" stroke-width="1.4"/><path d="M280.7 26 L280.7 268" stroke-dasharray="4 3" opacity="0.75"/><path d="M285.7 81.9 L296.7 81.9" opacity="0.5"/><path d="M285.7 198.1 L296.7 198.1" opacity="0.5"/></g><rect x="296.7" y="68.9" width="112" height="28" rx="3" fill="var(--md-default-bg-color)" stroke="none"/><rect x="296.7" y="185.1" width="112" height="28" rx="3" fill="var(--md-default-bg-color)" stroke="none"/><rect x="258.7" y="274.0" width="44" height="18" rx="3" fill="var(--md-default-bg-color)" stroke="none"/><g fill="currentColor" stroke="none"><circle cx="280.7" cy="81.9" r="4.5"/><circle cx="280.7" cy="198.1" r="4.5"/><text x="302.7" y="80.9" font-size="11" font-weight="700">y is even</text><text x="302.7" y="92.9" font-size="9" opacity="0.75">one candidate key</text><text x="302.7" y="197.1" font-size="11" font-weight="700">y is odd</text><text x="302.7" y="209.1" font-size="9" opacity="0.75">the other one</text><text x="280.7" y="288" font-size="12" text-anchor="middle">x = r</text><text x="20" y="18" font-size="10" opacity="0.75">r is only an x coordinate, and one x has two y values</text></g></svg>

Two candidate points give two candidate public keys, and so two candidate addresses. Only one of them signed.

One caveat the [public keys](public-keys.md) page already made: this smooth curve is a visual aid. Over Ethereum's finite field the two solutions aren't mirror images in any geometric sense — they're two numbers, and what separates them is that one is **even** and one is **odd**. Parity is the thing `v` records.

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
    transaction for the dullest possible reasons: the account nonce doesn't
    match, and there's nothing there to pay the fee with.

    The tampering fails, but not because a signature check said "invalid".
    It fails because the altered transaction is now claimed by a stranger who
    has no funds and no history. Which is a stronger guarantee than a check,
    because there's nothing to get wrong.

## Replay protection needs two different things

A signed transaction is a standing instruction. Unless something stops it, anyone who has seen it can submit it again — and it will still be valid, because it's still correctly signed by you. Two different versions of that problem exist, and each needs its own defence.

**Replayed on the same chain.** Someone rebroadcasts your payment hoping it executes twice. The [account nonce](../accounts/nonce.md "A per-account counter of transactions already sent") stops this: it's part of what you signed, and once an account has used a given nonce the network will never accept that number from it again.

Note which nonce that is. *k* must never repeat either, but for an entirely different reason and with an entirely different enforcer: repeating *k* is dangerous because it **leaks your key**, and nothing in the protocol checks for it. Repeating an account nonce is merely futile, because **every node checks it** and rejects the duplicate.

**Replayed on a different chain.** This one is less obvious. Ethereum isn't the only network using secp256k1 and this address format — there are testnets, forks such as Ethereum Classic, and unrelated chains built the same way. **Your key controls the same address on all of them.** So a transaction you signed for one network could be lifted and submitted on another, where it would verify perfectly and move real funds.

The defence is the **chain id**: a number identifying the network, included in what gets signed. Sign with Ethereum's chain id and the signature simply isn't valid anywhere else.

| Attack | Defence |
| --- | --- |
| Rebroadcasting your transaction **on this chain** | the **account nonce** — once used, that number is spent forever |
| Replaying it **on another chain** | the **chain id** — the signature is valid on one network only |

Neither covers the other. An account nonce means nothing across chains, since the other chain keeps its own count. A chain id does nothing about the same transaction being submitted twice on the network it belongs to.

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
- **Verification is recovery plus a comparison.** Ethereum does the recovery and has nothing to compare against, so a transaction signature is never "verified" in that sense — the sender isn't claimed and then checked, it's *defined* as whoever the signature recovers to. Where something does have an expectation to test, such as a website login, the comparison happens and that is verification.
- That is **not** the same as nothing being checked. Account nonce, balance, gas limit and chain id are all still validated — and most of them need the sender, so recovery is what makes those checks possible rather than a substitute for them.
- **The same message signed twice gives different signatures**, both recovering the same address.
- A tampered message recovers **a different address**, not an error — nothing in a signature says whose it should have been.
- Replay needs two defences: the **account nonce** within a chain, the **chain id** across chains.
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
