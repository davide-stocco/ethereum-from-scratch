---
tier: 1
description: Keccak-256 is Ethereum's hash function — any input in, 32 bytes out. What that buys, why it can't be reversed, and why it is not quite SHA-3.
---

# Keccak-256

**Fork-proof.** Ethereum's hash function since genesis, specified as such throughout the Yellow Paper [(Wood, 2014)](#ref-wood-2014). Addresses, the state root, transaction hashes and function selectors all depend on it, so it cannot be changed.

A **hash function** takes any input at all — a word, a book, a transaction, a gigabyte of video — and returns a fixed-size fingerprint. Keccak-256's output is always exactly **32 bytes**, which is [64 hex characters](../foundations/hex-and-bytes.md).

???+ example "Try it: hash anything"

    <div class="tool" markdown="0">
      <label for="kec-in">Input</label>
      <input id="kec-in" type="text" autocomplete="off" spellcheck="false" value="hello">
      <p class="tool__out" id="kec-out"></p>
    </div>

    Type anything. Empty the field, paste a paragraph, use emoji. **The output
    is always 32 bytes** — that's the first thing to notice, and it already
    tells you something important: the hash cannot contain the input, because
    the input can be larger than the output.

## The four properties

Everything Ethereum does with hashing rests on these, and nothing else.

**1. Deterministic.** The same input always gives the same output — on every machine, in every language, forever. Hash `hello` here, hash it in ten years on different hardware, and you get the same 32 bytes. This is what makes hashes usable in a system where thousands of computers must [agree](../foundations/what-is-ethereum.md).

**2. Fixed size.** Any input, 32 bytes out. A single character and the complete works of Shakespeare both come out the same length.

**3. Avalanche.** Change the input by the smallest possible amount and roughly **half** the output bits flip. Not "the output changes a bit" — the output is unrecognisable.

**4. One-way.** Given an output, there is no practical way to find an input that produces it. Easy forwards, infeasible backwards.

### Avalanche, demonstrated

The third property is the one people underestimate, so it's worth seeing. Two inputs differing by one letter:

???+ example "Try it: the avalanche effect"

    <div class="tool" markdown="0">
      <label for="av-a">Input A</label>
      <input id="av-a" type="text" autocomplete="off" spellcheck="false" value="hello">
      <label for="av-b">Input B</label>
      <input id="av-b" type="text" autocomplete="off" spellcheck="false" value="hellp">
      <p class="tool__out" id="av-out"></p>
    </div>

    `hello` and `hellp` differ in a single letter — in fact in a single *bit*
    of one byte. Yet **132 of the 256 output bits differ**, which is about
    half, exactly as the property predicts.

    Worth trying: make the two inputs **identical**. Every bit matches, every
    time. That's determinism and avalanche together — wildly sensitive to any
    change, and perfectly stable when there's none.

Half the bits is not an accident, it's the design target. If similar inputs produced similar hashes, you could hill-climb your way to a desired output: tweak, see if you got closer, tweak again. Avalanche destroys that strategy, because "closer" carries no information.

## Why it can't be reversed

The honest answer is simpler than people expect: **the output is too small to hold the input.**

Hash a one-megabyte file and you get 32 bytes. Eight million bits in, 256 bits out. The information is not hidden — it is *gone*. There is no key, nothing encrypted, nothing to decrypt. Most of the input was discarded by construction.

Which means infinitely many inputs share any given hash. That sounds alarming until you ask how you'd *find* one.

??? abstract "Collisions exist, and that's fine. Finding one is the problem."

    Since inputs are unlimited and outputs number only 2<sup>256</sup>,
    collisions must exist — two different inputs with the same hash. This is
    the pigeonhole principle and it isn't a weakness.

    The security claim isn't "no collisions exist". It's that **nobody can find
    one.** And 2<sup>256</sup> is a number that resists intuition:

    ```
    2^256 ≈ 115,792,089,237,316,195,423,570,985,008,
            687,907,853,269,984,665,640,564,039,457,
            584,007,913,129,639,936
    ```

    Roughly 10<sup>77</sup> — comparable to estimates of the number of atoms in
    the observable universe. A machine testing a billion billion hashes per
    second, running since the universe began, would have covered an utterly
    negligible fraction of it.

    So "one-way" is an economic claim, not a mathematical impossibility. The
    same distinction appears everywhere in this subject: not *cannot*, but
    *costs more than any conceivable benefit*.

## Keccak-256 is not SHA-3

This causes real confusion and real bugs, so it's worth being precise.

Keccak, designed by Bertoni, Daemen, Peeters and Van Assche [(Bertoni et al., 2011)](#ref-bertoni-2011), won NIST's competition to become SHA-3. Between winning and being published as a standard, **NIST changed the padding** — the bytes appended to the input before hashing [(NIST, 2015)](#ref-fips202). Ethereum had already adopted the original Keccak and kept it.

So Ethereum uses **Keccak-256**, and the NIST standard is **SHA3-256**, and they are *not the same function*. The difference is a single byte: `0x01` where the standard uses `0x06`.

One byte, and the outputs share nothing:

???+ example "Try it: Keccak-256 against SHA3-256"

    <div class="tool" markdown="0">
      <label for="sha-in">Input</label>
      <input id="sha-in" type="text" autocomplete="off" spellcheck="false" value="hello">
      <p class="tool__out" id="sha-out"></p>
    </div>

    Both functions use the identical permutation, the identical structure, the
    identical number of rounds. They differ by one byte of padding — and about
    half the output bits differ as a result. Avalanche doesn't care *where* the
    difference came from.

    The empty string is the pair worth remembering, since both turn up
    constantly in different contexts:

    ```
    keccak256("")  =  c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
    sha3_256("")   =  a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
    ```

**What goes wrong in practice:** a library function named `sha3` may implement either one, depending on its age and author. Call the wrong one and nothing errors — you simply get a hash that no other Ethereum tool agrees with. Addresses won't match, signatures won't verify, and nothing tells you why.

If you take one thing from this page: **when Ethereum says SHA-3, it means Keccak.** Check which your library gives you.

## Where Ethereum uses it

Almost everywhere, which is why this page comes first in the cryptography section:

| Use | What gets hashed |
| --- | --- |
| [Addresses](addresses.md) | a public key — the last 20 bytes of the hash become the address |
| [Address checksums](addresses.md) | the address itself, to detect typos |
| Transaction hashes | the signed transaction |
| [State and storage roots](../accounts/state.md) | every node of the trie |
| Function selectors | a function's name and parameter types |
| Contract addresses | the creator's address and [nonce](../accounts/nonce.md) |

In each case the job is the same: **compress something arbitrary into a fixed-size identifier nobody can forge.**

## What it is not

Two misconceptions worth killing off.

**It isn't encryption.** Encryption is reversible by design — that's its entire purpose. Hashing is not, and there's no key. "Decrypting a hash" is not a difficult problem; it's an incoherent request.

**It isn't random.** It's perfectly predictable: the same input always yields the same output. Hash output *looks* random, and that's useful, but anyone with the input can reproduce it exactly. Using a hash as a source of randomness is a well-trodden route to losing money, because whoever supplies the input chooses the result.

---

## Recap

- Keccak-256 takes **any input** and returns exactly **32 bytes**.
- It is **deterministic** — the same input gives the same output everywhere, forever.
- **Avalanche**: a one-bit change flips about half the output bits, so similar inputs tell you nothing about each other.
- It is **one-way** because the output is too small to hold the input. The information is gone, not hidden.
- Collisions must exist; the claim is that **nobody can find one**, and 2<sup>256</sup> is why.
- **Keccak-256 is not SHA3-256.** One padding byte apart, and completely different outputs.
- It is neither encryption nor a source of randomness.

**Next:** [Private keys](private-keys.md) — where a 256-bit number starts being worth something.

---

## References

<div class="sources" markdown>

- <a id="ref-bertoni-2011"></a>**Bertoni, G., Daemen, J., Peeters, M., & Van Assche, G.** (2011). *The Keccak reference*, version 3.0. The designers' own specification of the sponge construction and the permutation. <https://keccak.team/files/Keccak-reference-3.0.pdf>
- <a id="ref-fips202"></a>**National Institute of Standards and Technology** (2015). *SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions.* FIPS PUB 202. The standard whose padding differs from Ethereum's. <https://doi.org/10.6028/NIST.FIPS.202>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Specifies Keccak-256 as Ethereum's hash function throughout. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
