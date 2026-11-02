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

Before the demonstration, the thing doing the work deserves naming.

Signing and recovery are done with **ECDSA** — the Elliptic Curve Digital Signature Algorithm [(SECG, 2009)](#ref-sec1). It isn't an Ethereum invention or a cryptocurrency one; it's a long-standing standard used for TLS certificates, software signing and much else. Ethereum's contribution is the curve it runs on and the recovery trick below.

What it does, in and out:

```
    signing:      message hash  +  private key   ──►   two numbers, r and s
    verifying:    message hash  +  r, s  +  public key   ──►   yes or no
    recovering:   message hash  +  r, s  +  v   ──►   the public key itself
```

The first two are ordinary ECDSA. The **third** is what Ethereum leans on: rather than being handed a public key to check against, it reconstructs the public key from the signature. That's why no sender field is needed.

This page doesn't derive any of it. The three properties from the [private keys](private-keys.md) page are all you need: anyone can check it, it reveals nothing about the key, and it's bound to one message.

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

    **Step 1 — note what the verifier was given.** Only the message and the
    signature. Not the address, not the public key. The recovered address is
    computed, and it matches.

    **Step 2 — press Sign again**, several times. The signature changes
    completely every time, and **the recovered address never does.** This is
    the point made on the private keys page: a signature isn't a fixed token
    you could copy, it's freshly computed, and there's a random ingredient in
    each one.

    **Step 3 — alter the lower field only**, so the verifier checks a
    different message from the one that was signed. Change "Anna" to "Anne",
    or 1 ether to 2.

    Recovery doesn't fail. It returns **a different address** — some unrelated
    stranger. That's worth sitting with: there's no error state, because
    nothing in the signature says whose it was supposed to be. A tampered
    message simply recovers to somebody who never existed, and the transaction
    is rejected for having a sender who hasn't authorised anything.

## What actually gets signed

Not the transaction — the **hash** of the transaction, via [Keccak-256](keccak256.md).

That has a useful consequence. Since the hash covers every field, changing any single byte of the transaction changes the hash, and a signature over the old hash recovers to a different address. So the signature protects **all** of it at once: the amount, the recipient, the fee, the nonce. There's no need to sign each field separately, and no way to alter one in transit.

## The three values

| | What it is |
| --- | --- |
| `r` | derived from a random point chosen during signing |
| `s` | the part that actually involves the private key |
| `v` | which of two possible public keys to recover |

`r` and `s` are the signature proper, as ECDSA defines it [(SECG, 2009)](#ref-sec1). `v` is the interesting one, and it exists for a very practical reason.

### Why `v` is needed

Recovery starts from `r`, which gives you the *x* coordinate of a point on the curve. But as the [public keys](public-keys.md) page showed, an *x* coordinate has **two** possible *y* values — one even, one odd.

Two candidate points mean two candidate public keys, and therefore two candidate addresses. Only one of them signed. So `v` carries a single bit saying which: *the y was even* or *the y was odd*.

Without it you'd recover two addresses and have no way to choose. One extra bit saves you from that.

??? info "History: v used to carry more than one bit"

    In early Ethereum, `v` was 27 or 28 — the parity bit plus an offset
    inherited from Bitcoin.

    Then came a problem. A transaction signed for Ethereum was equally valid on
    any other chain using the same curve, so a payment could be taken from one
    network and replayed on another, where the same key controlled the same
    address. **EIP-155** [(Buterin, 2016)](#ref-eip155) fixed it by folding the
    **chain id** into `v`, so a signature became valid on exactly one network.

    Modern typed transactions dropped that trick. They carry the chain id as
    its own field and store the parity plainly as 0 or 1 — which is what the
    tool above shows. Cleaner, and the same protection.

    So if you meet `v = 27`, `v = 37` and `v = 1` in different places, none is
    wrong; they're three generations of the same bit.

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

!!! warning "Which is why a signing prompt deserves reading"

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
