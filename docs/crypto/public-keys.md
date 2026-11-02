---
tier: 1
description: A public key is a point on a curve, computed from a private key by a step that is easy forwards and infeasible backwards.
---

# Public keys

**Fork-proof.** secp256k1 has been Ethereum's curve since genesis.

A [private key](private-keys.md) is a number you keep. A **public key** is what you get by running that number through a one-way calculation, and it's safe to publish.

The calculation involves an elliptic curve, which sounds forbidding and mostly isn't. You need three things from this page: what a public key *is*, why the step can't be reversed, and which of its several written forms Ethereum actually uses.

## The curve

secp256k1 is the set of points satisfying one equation:

```
y² = x³ + 7
```

Not over the real numbers, where that would be a smooth curve you could draw, but over a finite field — all arithmetic is done modulo a large prime:

```
p = 2²⁵⁶ − 2³² − 977
```

So the "curve" is really a large, scattered set of integer coordinate pairs. Nothing about it looks curved. That doesn't matter; what matters is that the set has useful structure.

That structure is an **addition** operation: given two points on the curve, a defined procedure produces a third point also on the curve. From addition you get multiplication by a whole number, which is just repeated addition — and multiplication is the whole mechanism.

## Deriving a public key

The curve comes with one fixed, published point called the **generator**, written **G**. Everyone uses the same one.

Your public key is:

```
public key = private key × G
```

That's it. Take G, add it to itself as many times as your private key says, and the point you land on is your public key. Since a private key is about 10⁷⁷, "as many times as your private key says" is not something you'd do literally — more on that below.

??? example "Try it: private key to public key"

    <div class="tool" markdown="0">
      <label for="pub-priv">Private key (hex)</label>
      <input id="pub-priv" type="text" autocomplete="off" spellcheck="false" value="1">
      <button id="pub-rand" type="button">Random key</button>
      <p class="tool__out" id="pub-out"></p>
    </div>

    Things worth trying:

    - Start with **`1`**. The result is G itself — the generator, the same
      published point everyone starts from. You can look it up and check.
    - Then **`2`**, then **`3`**. Watch the coordinates. They don't drift or
      grow steadily; each one is unrelated to the last. **That scattering is
      the security.**
    - Press **Random key** a few times, which is what a real wallet does.
    - Try `0`, or a value above the curve order. Both are rejected, for the
      reason given on the [private keys](private-keys.md) page.

## Why it can't be reversed

Going forwards is fast. Going backwards — given a public key, find the private key — is the **discrete logarithm problem**, and nobody has a practical method.

The reason is the same one that makes [Keccak-256](keccak256.md) one-way, and it's worth noticing the parallel: **the output gives you nothing to follow.**

Try the tool with 1, then 2, then 3. The coordinates jump about with no pattern. They don't increase. "Close to the right answer" doesn't exist, because a private key one away from yours produces a point bearing no resemblance to yours. So there's no gradient to climb, no way to narrow the search, nothing to do but guess — and [guessing is hopeless](private-keys.md) at this scale.

??? abstract "Then how is the forward direction fast?"

    A fair question, since adding G to itself 10⁷⁷ times is obviously not
    happening.

    The trick is **doubling**. Rather than stepping one G at a time, you
    repeatedly double — G, 2G, 4G, 8G, 16G — and add together whichever of
    those you need. Any number up to 2²⁵⁶ is the sum of at most 256 such
    powers, which is exactly what its binary representation tells you.

    So the whole computation is around 256 doublings and at most 256
    additions, and it finishes in well under a millisecond. The tool above is
    doing it in your browser.

    The asymmetry is the entire point: **about 256 operations forwards, no
    known shortcut backwards.** Multiplying is cheap; dividing is not
    available.

## The several written forms

A public key is a pair of coordinates, each 32 bytes, so 64 bytes in total. But you'll meet it written several ways, which is a common source of confusion:

| Form | Size | What it looks like |
| --- | --- | --- |
| **Raw** | 64 bytes | `x` then `y` |
| **Uncompressed** | 65 bytes | `0x04` then `x` then `y` |
| **Compressed** | 33 bytes | `0x02` or `0x03` then `x` |

The `0x04` prefix in the second form is a marker meaning "uncompressed point follows". It is **not** part of the key, and this trips people up constantly — see the note below.

**Compressed** form drops `y` entirely, which works because the curve equation nearly determines it. Given `x`, the equation `y² = x³ + 7` has exactly two solutions, and they always have opposite parity — one even, one odd. So a single byte recording which one it was (`02` for even, `03` for odd) is enough to recompute `y`. Half the size, no information lost.

!!! warning "Ethereum hashes the 64-byte form, with no prefix"

    When deriving an [address](addresses.md), Ethereum hashes the **raw 64
    bytes** — `x` followed by `y`, and *no* `0x04` prefix.

    The Yellow Paper is explicit about this — address derivation takes the
    64-byte representation [(Wood, 2014)](#ref-wood-2014).

    Include the prefix and you hash 65 bytes instead of 64, which by the
    avalanche property gives you a completely unrelated hash, and therefore a
    completely wrong address. Nothing errors; you just get an address that
    isn't yours.

    This is probably the single most common mistake when implementing address
    derivation by hand.

## Why this curve?

The name decodes: **sec**urity standards group, **p** for prime field, **256** bits, **k** for Koblitz, and **1** because it's the first such curve in the list [(SECG, 2010)](#ref-secg-2010).

Bitcoin chose it, and Ethereum followed — which brought a decade of implementations, review and hardware support along with it.

??? info "There was another candidate, and the choice is interesting"

    The obvious alternative was **secp256r1**, where `r` stands for random.
    It's the curve NIST recommends and most of the wider internet uses.

    The two were generated differently. secp256k1's parameters are
    structurally derived — a Koblitz curve, with the small constant 7 and a
    prime close to a power of two, chosen because they make the arithmetic
    fast and the choices visible. secp256r1's parameters come from hashing an
    unexplained seed value, and nobody has said where that seed came from.

    There is no published attack on secp256r1, and this is not evidence of
    one. But "we can see exactly why every constant is what it is" is a
    property cryptographers value for its own sake, and it's part of why the
    k1 curve was attractive for a system meant to need no trusted authority.

## When your public key becomes visible

A detail worth knowing, because it isn't obvious.

Receiving ether reveals nothing. People send to your **[address](addresses.md)**, which is a hash of your public key — and a hash can't be reversed, so an unused account exposes only the address.

Your public key becomes known the first time you **sign** something. A [signature](signatures.md) lets anyone recover the public key that produced it; that's how verification works at all. So the moment you send your first transaction, your public key is on the chain for good.

This doesn't put anything at risk — the public key is meant to be public, and the private key is still unreachable behind the discrete logarithm problem. But "my public key is secret until I transact" is true, and occasionally matters.

---

## Recap

- A public key is a **point on the secp256k1 curve**: two coordinates, 32 bytes each.
- It's computed as **private key × G**, where G is a fixed published point everyone shares.
- Forwards takes about **256 doublings**; backwards is the discrete logarithm problem, with no known shortcut.
- It's one-way for the same reason hashing is: **the output offers nothing to follow.** Neighbouring private keys give unrelated points.
- Three written forms — raw (64 bytes), uncompressed with an `0x04` prefix (65), compressed (33).
- **Ethereum hashes the raw 64 bytes.** Including the prefix silently produces the wrong address.

**Next:** [Addresses](addresses.md) — the last step, and the one that finally produces something you'd paste into a wallet.

---

## References

<div class="sources" markdown>

- <a id="ref-secg-2010"></a>**Standards for Efficient Cryptography Group** (2010). *SEC 1: Elliptic Curve Cryptography* and *SEC 2: Recommended Elliptic Curve Domain Parameters*, version 2.0. SEC 1 defines the point encodings used above; SEC 2 defines secp256k1 itself, including the generator G and the field prime. <https://www.secg.org/sec2-v2.pdf>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Appendix F specifies the use of secp256k1 and the 64-byte public key form for address derivation. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
