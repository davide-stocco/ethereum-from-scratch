---
tier: 1
description: Keccak-256 is Ethereum's hash function — any input in, 32 bytes out. What that buys, why it can't be reversed, and why it is not quite SHA-3.
---

# Keccak-256

**Fork-proof.** Ethereum's hash function since genesis, specified as such throughout the Yellow Paper [(Wood, 2014)](#ref-wood-2014). Addresses, the state root, transaction hashes and function selectors all depend on it, so it cannot be changed.

!!! definition "Keccak-256"

    A **hash function**: it takes any input at all — a word, a book, a
    transaction, a gigabyte of video — and returns a fixed-size fingerprint.
    Keccak-256's output is always exactly **32 bytes**, which is
    [64 hex characters](../foundations/hex-and-bytes.md).

    The same input always gives the same fingerprint. A slightly different
    input gives an unrecognisably different one. And there is no way to work
    backwards from a fingerprint to what produced it.

??? example "Try it: hash anything"

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

**3. Avalanche.** Change the input by the smallest possible amount and **nearly every character of the output changes**. Not "the output changes a bit" — the output is unrecognisable.

**4. One-way.** Given an output, there is no practical way to find an input that produces it. Easy forwards, infeasible backwards.

### Avalanche, demonstrated

The third property is the one people underestimate, so it's worth seeing. Two inputs differing by one letter:

??? example "Try it: the avalanche effect"

    <div class="tool" markdown="0">
      <label for="av-a">Input A</label>
      <input id="av-a" type="text" autocomplete="off" spellcheck="false" value="hello">
      <label for="av-b">Input B</label>
      <input id="av-b" type="text" autocomplete="off" spellcheck="false" value="hellp">
      <p class="tool__out" id="av-out"></p>
    </div>

    `hello` and `hellp` differ in a single letter. Yet **61 of the 64 hex
    characters differ** — the output isn't similar, it's unrelated.

    Worth trying: make the two inputs **identical**. Every character matches,
    every time. That's determinism and avalanche together — wildly sensitive to
    any change, and perfectly stable when there's none.

### Nearly every character, but only half the bits

The tool reports two numbers, and the gap between them is worth a moment: **61 of 64 characters** changed, but only **132 of 256 bits**.

That isn't a contradiction. Recall from [hex and bytes](../foundations/hex-and-bytes.md) that each hex character is exactly four bits. A character *looks* different if **any one** of its four bits flipped — so characters are a much blunter instrument than bits.

If the function is doing its job, each output bit flips with probability one half. The chance that all four bits of a character survive untouched is then:

```
(1/2)^4  =  1/16
```

So a character changes 15 times out of 16, and across 64 characters you'd expect about 64 × 15/16 = **60** of them to change. We observed 61.

**Half the bits is the design target; nearly every character is what that looks like in hex.** The bit figure is the precise statement of the property, and the character figure is what you actually see.

And half is not an accident. If similar inputs produced similar hashes, you could hill-climb your way to a desired output: tweak the input, check whether you got closer, tweak again. Avalanche destroys that strategy, because "closer" carries no information at all.

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

## How it works: the sponge

The page so far has treated the function as a box you drop bytes into. The inside is worth a look, because Keccak's shape is unusual and it's what the next section's one-byte difference actually modifies.

The design is called a **sponge** [(Bertoni et al., 2011)](#ref-bertoni-2011), for the obvious reason: it absorbs, then it squeezes.

<svg viewBox="0 0 470 306" role="img" aria-label="The sponge. One state of 1600 bits, drawn as a bar split into a rate of 136 bytes and a capacity of 64 bytes, together making 200 bytes. Message blocks are exclusive-ored into the rate only. Between blocks a permutation mixes all 1600 bits. The hash is read from the rate at the end." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="46" y="14" width="76" height="26" rx="3"/><rect x="150" y="14" width="76" height="26" rx="3"/><rect x="254" y="14" width="76" height="26" rx="3"/><path d="M84 40 L84 86"/><path d="M188 40 L188 86"/><path d="M292 40 L292 86"/><rect x="40" y="92" width="340" height="58" rx="4"/><rect x="40" y="150" width="340" height="40" rx="4" stroke-dasharray="4 3"/><path d="M380 120 L414 120"/><path d="M40 202 L40 210 L380 210 L380 202"/></g><g fill="currentColor" stroke="none"><path d="M79 86 L84 96 L89 86 Z"/><path d="M183 86 L188 96 L193 86 Z"/><path d="M287 86 L292 96 L297 86 Z"/><path d="M414 115 L424 120 L414 125 Z"/><text x="84" y="31" font-size="10" text-anchor="middle">block 1</text><text x="188" y="31" font-size="10" text-anchor="middle">block 2</text><text x="292" y="31" font-size="10" text-anchor="middle">block 3</text><text x="338" y="31" font-size="11" opacity="0.7">&#8230;</text><text x="46" y="58" font-size="9" opacity="0.75">136 bytes each, XORed in &#8212; nothing else enters</text><text x="52" y="116" font-size="11" font-weight="700">RATE</text><text x="52" y="132" font-size="10" opacity="0.85">136 bytes (1088 bits) &#183; input in, hash out</text><text x="52" y="168" font-size="11" font-weight="700">CAPACITY</text><text x="52" y="182" font-size="10" opacity="0.85">64 bytes (512 bits) &#183; the input never reaches it</text><text x="210" y="228" font-size="10" text-anchor="middle">136 + 64 = 200 bytes, which is the whole state: <tspan font-weight="700">1600 bits</tspan></text><text x="384" y="112" font-size="9">32 bytes out</text><text x="40" y="256" font-size="10" opacity="0.85">After each block the permutation stirs all 1600 bits together, so the capacity</text><text x="40" y="270" font-size="10" opacity="0.85">does change &#8212; but only as a side effect of input that went into the rate.</text><text x="40" y="294" font-size="10" opacity="0.6">24 rounds of the permutation per block &#183; state is 25 lanes of 64 bits</text></g></svg>

**There is a state of 1600 bits**, starting at all zeros. That's the whole memory of the function — no matter how much data you hash, this is all it ever holds.

The 1600 isn't arbitrary. The permutation is defined over a 5 × 5 grid of 64-bit **lanes**, and 25 × 64 = 1600. That grid is the shape the five round steps are written in terms of, so the state size follows from the design rather than the other way round. In bytes it's 200, which is the number to hold onto: **136 + 64.**

The state is split in two, and the split is the entire security story:

- the **rate**, 1088 bits or 136 bytes, which your input is allowed to touch
- the **capacity**, 512 bits, which it is **not**

Hashing then goes:

1. **Pad** the message so its length is a multiple of 136 bytes.
2. **Absorb.** Take the first 136-byte block and XOR it into the rate. Leave the capacity alone.
3. **Permute.** Run the whole 1600 bits through a fixed scrambling function, 24 rounds of it. This mixes rate into capacity and back.
4. Repeat 2 and 3 for every remaining block.
5. **Squeeze.** Read the first 256 bits of the state. That's your hash.

### Why the capacity is the point

An attacker trying to steer the output controls the input — and therefore controls what gets XORed into the rate, exactly. If that were the whole state, they would have complete knowledge of it at every step, and the function would be a calculation they could run backwards.

The capacity denies them that. **512 bits of the state are never written by the message directly.** They change constantly, but only as a side effect of the permutation stirring the rate into them. So each block arrives into a state the attacker has not fully specified, and that gap compounds with every block absorbed.

### Nothing here is random

Worth heading off straight away, because "the attacker can't control the capacity" sounds like it must involve randomness somewhere. It doesn't. **There is no randomness anywhere in Keccak** — that would contradict the determinism at the top of this page, which is the property the whole of Ethereum rests on.

The state begins at all zeros. Every step afterwards is fixed arithmetic. Anybody who hashes the same input gets the same 1600 bits at every stage, capacity included, on any machine, forever. You could print the capacity out at each step and compare notes; two people doing it would agree exactly. It is neither secret nor unpredictable, and there is nothing to "check for randomness" because nothing claims to be random.

What the capacity actually is, is **not independently choosable.** The attacker picks the input and thereby fixes everything, including the capacity — but only *via* the permutation. To make the capacity take some particular value they'd have to work backwards from that value to an input producing it, and that is precisely the problem the permutation is built to make infeasible. They can always compute what the capacity will be. They cannot choose the rate and the capacity to suit them at the same time.

So the security doesn't come from hidden information. It comes from the input and the state being tied together by something that is cheap to run forwards and hopeless to run backwards — the same asymmetry the [one-way section](#why-it-cant-be-reversed) above described, applied to the function's own internals.

That's also why the number is 512 rather than something smaller: it's sized so the capacity is never the weakest link. With a 256-bit output, the binding limit is the birthday bound on the output itself — the 2<sup>128</sup> of the collisions box above — not anything about the internal state.

??? abstract "The permutation, in one paragraph"

    Each of the 24 rounds applies five steps, traditionally named with Greek
    letters: **θ** mixes each bit with the parity of two nearby columns, **ρ**
    rotates each of the 25 lanes by a different fixed amount, **π** moves the
    lanes around, **χ** is the only non-linear step and the one that makes the
    whole thing irreversible in practice, and **ι** XORs in a round constant so
    that the rounds aren't identical to each other.

    You don't need the detail to use the function, and this site's
    implementation doesn't need you to trust it — the rotation amounts and
    round constants are **computed from the specification's own formulas**
    rather than copied from a table, then checked against the published test
    values. A transcription error in a table of 24 constants would be invisible
    on inspection and fatal in use.

## Keccak-256 is not SHA-3

This causes real confusion and real bugs, so it's worth being precise.

Keccak, designed by Bertoni, Daemen, Peeters and Van Assche [(Bertoni et al., 2011)](#ref-bertoni-2011), won an open competition to become SHA-3. The competition was run by **[NIST](../glossary.md#nist "The US government agency that publishes technical standards, cryptography included")** — the United States standards agency, which publishes the cryptographic standards most of the world ends up using.

Between Keccak winning and the standard being published, **NIST changed the padding**: the bytes appended to the input before hashing [(NIST, 2015)](#ref-fips202). Ethereum had already adopted the original Keccak and kept it.

So Ethereum uses **Keccak-256**, and the NIST standard is **SHA3-256**, and they are *not the same function*. The difference is a single byte: `0x01` where the standard uses `0x06`.

One byte, and the outputs share nothing:

??? example "Try it: Keccak-256 against SHA3-256"

    <div class="tool" markdown="0">
      <label for="sha-in">Input</label>
      <input id="sha-in" type="text" autocomplete="off" spellcheck="false" value="hello">
      <p class="tool__out" id="sha-out"></p>
    </div>

    Both functions use the identical permutation, the identical structure, the
    identical number of rounds. They differ by one byte of padding — and almost
    every character of the output differs as a result. Avalanche doesn't care
    *where* the difference came from.

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
- **Avalanche**: a one-letter change rewrites nearly every character of the output — half the bits, which in hex means about 60 of the 64 characters. Similar inputs tell you nothing about each other.
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
