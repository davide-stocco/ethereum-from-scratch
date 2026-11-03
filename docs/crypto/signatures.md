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

## The algorithm has a name

Before the demonstration, the thing doing the work deserves naming — and so do its three outputs, which appear everywhere once you start looking at transactions.

Signing and recovery are done with **ECDSA**, the Elliptic Curve Digital Signature Algorithm [(SECG, 2009)](#ref-sec1). It isn't an Ethereum invention or a cryptocurrency one; it's a long-standing standard behind TLS certificates and software signing. Ethereum's contribution is the curve it runs on, and the use it makes of recovery.

### Where `r` and `s` come from

Signing a message hash **z** with a private key **d** goes like this:

1. Pick a **random secret number**, called *k*, used once and then thrown away.
2. Compute the curve point *k* × G, the same multiplication from the [public keys](public-keys.md) page.
3. **`r` is the x coordinate of that point.**
4. **`s` combines** the message hash, `r`, the private key and *k*, in a single modular equation.

So the two halves have distinct jobs. `r` is a commitment to the random point — it depends on *k* and nothing else. `s` is the half the **private key enters**, mixed with the message so that the pair is bound to this message and no other.

Neither value reveals *d*, and neither reveals *k*. And because *k* is fresh every time, `r` and `s` are completely different on every signature — which is what you see when you press *Sign again* below.

??? warning "k must never repeat"

    If the same *k* is ever used to sign two different messages with the same
    key, the private key can be recovered from the two signatures by
    schoolroom algebra. It's one of the classic ways real systems have lost
    keys, and the reason serious implementations derive *k* deterministically
    from the key and message rather than trusting a random number source.

### Why recovery is possible at all

Here is the part worth understanding, because it looks like magic and isn't.

**Verification and recovery are the same equation, solved for different unknowns.**

ECDSA's check is a relationship between four things: the message hash, `r`, `s`, and the public key **Q**. Ordinarily you are handed all four, substitute them in, and see whether the relationship holds — that's verification.

But an equation with one unknown can be rearranged. Leave **Q** out, and the relationship can be solved *for* **Q** instead:

```
    Q  =  r⁻¹ ( s·R  −  z·G )
```

where **R** is the point whose x coordinate is `r`. Everything on the right is public: `r` and `s` come with the signature, *z* is the message hash, G is the fixed generator. So the public key falls out directly.

Recovery isn't a feature bolted onto ECDSA. It's the same algebra read in the other direction.

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
    **chain id** into `v`, so a signature became valid on exactly one network.

    Modern typed transactions dropped that trick. They carry the chain id as
    its own field and store the parity plainly as 0 or 1 — which is what the
    tool below shows. Cleaner, and the same protection.

    So if you meet `v = 27`, `v = 37` and `v = 1` in different places, none is
    wrong; they're three generations of the same bit.

### The three operations, side by side

```
    signing:      message hash  +  private key          ──►   r, s
    verifying:    message hash  +  r, s  +  public key   ──►   yes or no
    recovering:   message hash  +  r, s  +  v            ──►   the public key
```

The first two are ordinary ECDSA, used across the internet. The **third** is what Ethereum leans on, and it's why a transaction needs no sender field.

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

## What actually gets signed

Not the transaction — the **hash** of the transaction, via [Keccak-256](keccak256.md).

That has a useful consequence. Since the hash covers every field, changing any single byte of the transaction changes the hash, and a signature over the old hash recovers to a different address. So the signature protects **all** of it at once: the amount, the recipient, the fee, the nonce. There's no need to sign each field separately, and no way to alter one in transit.

## Replay protection needs two different things

Worth putting side by side, because they're easily confused and solve different problems.

| Attack | Defence |
| --- | --- |
| Rebroadcasting your transaction **on this chain** | the [nonce](../accounts/nonce.md "A per-account counter of transactions already sent") — once used, that number is spent forever |
| Replaying it **on another chain** | the chain id — the signature is only valid for one network |

Neither covers the other. A nonce is meaningless across chains, since the other chain has its own count. A chain id does nothing about the same transaction being submitted twice on the network it belongs to.

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
- <a id="ref-sec1"></a>**Standards for Efficient Cryptography Group** (2009). *SEC 1: Elliptic Curve Cryptography*, version 2.0. Specifies ECDSA signing, verification and public key recovery. <https://www.secg.org/sec1-v2.pdf>
- <a id="ref-eip191"></a>**Van de Sande, A., Nita-Rotaru, C., & Logvinov, L.** (2016). *ERC-191: Signed data standard.* Ethereum Improvement Proposals. Prefixes signed messages so they cannot be confused with signed transactions. <https://eips.ethereum.org/EIPS/eip-191>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Appendix F defines the recovery function used to obtain a sender address from a signature. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
