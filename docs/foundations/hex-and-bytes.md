---
tier: 1
description: Bytes, hexadecimal and the 0x prefix — how to read the long strings of characters that Ethereum is written in.
---

# Hex and bytes

**Fork-proof.** This isn't an Ethereum rule at all. It's how computers represent data, and it predates all of this by decades.

Everything on Ethereum is eventually a string of characters like this:

```
0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

This page is about how to read that. It's short, and it exists so that later pages can say "32 bytes" and have it mean something.

## A byte is eight bits

A **bit** is a single one or zero. A **byte** is eight of them together.

Eight bits can be arranged in 2<sup>8</sup> = **256** different ways, so one byte holds one of 256 possible values — conventionally read as a number from 0 to 255.

The byte is the unit everything is measured in. Not because it's mathematically special, but because it's what hardware settled on, and the whole stack has counted in bytes ever since.

## Hexadecimal

**Hex** is counting in base 16 instead of base 10. It needs sixteen digits, and since we only have ten, the first six letters fill in. The encoding is standardised, as Base16 [(Josefsson, 2006)](#ref-josefsson-2006), though you'll never see it called that outside a specification:

| Hex | Decimal | | Hex | Decimal |
| --- | --- | --- | --- | --- |
| `0`–`9` | 0–9 | | `d` | 13 |
| `a` | 10 | | `e` | 14 |
| `b` | 11 | | `f` | 15 |
| `c` | 12 | | | |

So `f` is 15, and `10` in hex is sixteen.

### Why base 16, and not 10

Because of one tidy coincidence: **one byte is exactly two hex characters.**

A byte holds 256 values. Two hex characters give 16 × 16 = 256 possibilities. They correspond perfectly, with nothing left over:

```
byte value 0   ->  00
byte value 255 ->  ff
```

Decimal has no such alignment. A byte in decimal takes one, two, or three digits depending on its value, so you can't look at a decimal string and see where one byte ends and the next begins. In hex you can, always: **chop it into pairs.**

```
d8 dA 6B F2 69 64 aF 9D 7e Ed 9e 03 E5 34 15 D3 7a A9 60 45
```

That's the address from the top of the page, as the twenty bytes it actually is.

Hex is also case-insensitive as a number — `aF` and `AF` are the same value. (Mixed case in an address *does* carry meaning, but as a checksum rather than as part of the number. That's covered under [addresses](../crypto/addresses.md).)

## The `0x` prefix

`0x` means "what follows is hexadecimal". That's all. It is **not part of the value** — it's a label, so that `0x11` isn't mistaken for eleven.

The convention comes from the C programming language and is used nearly everywhere. Ethereum tooling puts it on essentially everything.

## The two lengths worth memorising

Almost every long string you meet on Ethereum is one of two sizes:

| Bytes | Hex characters | What it usually is |
| --- | --- | --- |
| **20** | 40 | an [address](../crypto/addresses.md) |
| **32** | 64 | a hash, or one slot of contract storage |

Worth doing once, by hand: count the characters after the `0x` in the address above. There are forty. That's twenty bytes, and from now on "20 bytes" and "40 hex characters" should feel like the same statement.

The 32-byte figure turns up constantly because it's the output size of [Keccak-256](../crypto/keccak256.md), Ethereum's hash function, and also the width of a single machine word in the EVM.

## One trap worth knowing about

`0x1234` can mean two different things, and conflating them causes real bugs.

**As a number**, it's 1×4096 + 2×256 + 3×16 + 4 = **4660**.

**As bytes**, it's two bytes — `0x12` and `0x34` — and the sensible questions are about its length rather than its magnitude.

Which one is meant depends entirely on context. A balance is a number. An address is bytes. A hash is bytes. Addresses are never arithmetic, even though they look like enormous numbers, and nothing good comes of adding two of them together.

??? abstract "Leading zeros, and why they sometimes matter"

    The distinction above has a sharp edge: **as a number, leading zeros are
    meaningless; as bytes, they are not.**

    `0x01` and `0x0001` are the same number — one. But they are different byte
    strings: one byte versus two. So a 32-byte hash beginning `00` has not
    somehow lost a byte, and padding a value to 32 bytes changes its length
    without changing its value.

    This matters more than it sounds. [RLP](../encoding/rlp.md) requires that
    integers be encoded with **no leading zeros**, precisely so that each value
    has exactly one valid encoding. Without that rule, `0x01` and `0x0001`
    would both be valid encodings of the same number, two nodes could hash the
    same data and get different answers, and consensus would break.

    So "is this a number or a byte string?" isn't pedantry — the answer
    determines whether `0x0001` is well-formed.

??? abstract "Big-endian, and why the direction is a choice"

    Given several bytes making up one number, you have to agree which end is
    the most significant. There are two conventions:

    - **Big-endian** puts the most significant byte first, the way we write
      decimal numbers: in `0x1234`, the `12` is the large part.
    - **Little-endian** puts the least significant byte first, which some
      processors prefer internally.

    **Ethereum is big-endian** — integers are serialised most-significant-byte
    first throughout the specification [(Wood, 2014)](#ref-wood-2014). So hex
    strings read in the familiar direction, and `0x1234` is 4660 rather than
    13330.

    You can go a long way without thinking about this. It becomes unavoidable
    the moment you write code that converts between numbers and bytes, which is
    where most beginner mistakes in this area live.

## Why not binary?

You could write everything in bits, and occasionally that's clearer — it's the only way to see a single flag being set.

But bits are unmanageably long. The address at the top of this page is twenty bytes, which is **160 bits**:

```
1101100010011010011010111111001001101001011001001010111110011101...
```

Forty hex characters, or a hundred and sixty ones and zeros. Hex is the compromise: compact enough to read aloud, and still exactly aligned to byte boundaries.

---

## Recap

- A **byte** is 8 bits, holding one of 256 values.
- **Hex** is base 16, using `0`–`9` and `a`–`f`.
- **One byte is exactly two hex characters** — the reason hex is used at all.
- **`0x`** means "hex follows" and isn't part of the value.
- **20 bytes = 40 characters = an address. 32 bytes = 64 characters = a hash.**
- Whether a hex string is a **number** or a **byte string** is a real distinction, and leading zeros are where it bites.

**Next:** [Keccak-256](../crypto/keccak256.md) — the function that turns any input into 32 of these bytes.

---

## References

<div class="sources" markdown>

- <a id="ref-josefsson-2006"></a>**Josefsson, S.** (2006). *The Base16, Base32, and Base64 Data Encodings.* RFC 4648, Internet Engineering Task Force. Specifies Base16 — hexadecimal — as a data encoding. <https://www.rfc-editor.org/rfc/rfc4648>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Appendix B sets out the big-endian convention and the no-leading-zeros rule for integer serialisation. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
