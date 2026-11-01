---
tier: 1
description: Bytes, hexadecimal and the 0x prefix — how to read the long strings of characters that Ethereum is written in.
---

# Hex and bytes

**Fork-proof.** This isn't an Ethereum rule at all — it's how computers represent data.

Everything on Ethereum is eventually a string of characters like this:

```
0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

This page is about how to read that. It's short, and it exists so that later pages can say "32 bytes" and have it mean something.

## A byte is eight bits

A **bit** is a single one or zero. A **byte** is eight of them in a row:

```
0 1 1 0 1 0 0 1
```

How many different bytes are possible? Each position is independently a 0 or a 1, so every position you add doubles the number of patterns. Small cases first, because the pattern is easier to see than to state:

| Bits | Patterns | All of them |
| --- | --- | --- |
| 1 | 2 | `0` `1` |
| 2 | 4 | `00` `01` `10` `11` |
| 3 | 8 | `000` `001` `010` `011` `100` `101` `110` `111` |
| 8 | **256** | `00000000` … `11111111` |

Each extra bit doubles it: 2, 4, 8, 16, 32, 64, 128, **256**. That's 2<sup>8</sup>.

By convention each pattern is read as a number, counting up from zero:

```
00000000  =    0
00000001  =    1
00000010  =    2
00000011  =    3
   ...
11111110  =  254
11111111  =  255
```

So "one byte" and "a number from 0 to 255" are two descriptions of the same thing. The byte is the unit everything gets measured in — not because eight is mathematically special, but because it's what hardware settled on, and the whole stack has counted in bytes since.

## Hexadecimal

**Hex** is counting in base 16 instead of base 10. It needs sixteen digits, and since we only have ten, the first six letters fill in. The encoding is standardised, as Base16 [(Josefsson, 2006)](#ref-josefsson-2006), though you'll never see it called that outside a specification:

| Hex | Decimal | | Hex | Decimal |
| --- | --- | --- | --- | --- |
| `0`–`9` | 0–9 | | `d` | 13 |
| `a` | 10 | | `e` | 14 |
| `b` | 11 | | `f` | 15 |
| `c` | 12 | | | |

So `f` is 15, and `10` in hex is sixteen.

### Reading a hex number

It works exactly like decimal, except each position is worth **16 times** the one to its right instead of 10 times.

In decimal, `1234` means 1×1000 + 2×100 + 3×10 + 4. The place values are 1, 10, 100, 1000 — powers of ten.

In hex the place values are powers of sixteen: 1, 16, 256, 4096. So `0x2f`:

```
0x2f
  │└─ f  = 15,  in the ones place      →  15 × 1   =  15
  └── 2  =  2,  in the sixteens place  →   2 × 16  =  32
                                                      ──
                                                      47
```

And a four-character example, `0x1234`:

```
4 × 1     =     4
3 × 16    =    48
2 × 256   =   512
1 × 4096  =  4096
             ─────
              4660
```

That's all there is to it. Nothing about hex is conceptually different from decimal — only the number of digits available.

### Why base 16, and not 10

Because of one tidy coincidence: **one byte is exactly two hex characters.**

A byte holds 256 values. Two hex characters give 16 × 16 = 256 possibilities. They correspond perfectly, with nothing left over:

| Bits | Hex | Decimal |
| --- | --- | --- |
| `00000000` | `00` | 0 |
| `00001111` | `0f` | 15 |
| `00010000` | `10` | 16 |
| `10101010` | `aa` | 170 |
| `11111111` | `ff` | 255 |

Notice that two hex characters also split the byte neatly in half: the left character is the first four bits, the right character the last four. `aa` is `1010` then `1010`.

**Decimal has no such alignment**, and the consequence is worth seeing rather than being told.

Suppose you want to write down three bytes whose values are 5, 255 and 7.

In **hex**, each one takes exactly two characters, so you get `05 ff 07`, which you'd write as:

```
05ff07
```

Now recover the original three bytes. Easy — chop it into pairs: `05`, `ff`, `07`.

In **decimal**, those same three values take one, three and one digits:

```
52557
```

Now recover them. You can't. Is that 5, 25, 57? Or 52, 5, 57? Or 5, 255, 7? Nothing in the string tells you where one byte ends and the next begins, because decimal digits per byte varies with the value.

That's the whole reason hex is used: **the boundaries are always visible.**

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

**As a number**, it's 4660 — the calculation from earlier.

**As bytes**, it's two bytes: `0x12` and `0x34`.

Both readings are valid. Which is meant depends on context — and the context is really *what you intend to do with it.*

**A number is a quantity.** You add to it, subtract from it, ask whether it's bigger than another one. A balance is a quantity: 2.5 ether plus 1 ether is a meaningful thing to compute.

**A byte string is an identifier.** You compare it for equality and you check its length. That's all. An address isn't a quantity — the only questions worth asking are *"is this 20 bytes?"* and *"is this the same address as that one?"*

Which is why "is this address larger than that address?" is not a meaningful question, even though both look like enormous numbers. It's the same category error as asking whether one phone number is bigger than another: the digits are there to identify, not to count.

So: balances are numbers. Addresses, hashes and storage keys are byte strings. Nothing good comes of doing arithmetic on the second group.

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

    Here's the problem. Take the two bytes `0x12` and `0x34`, in that order,
    and read them as one number. **There are two defensible answers**, because
    you first have to agree which end carries the large part.

    **Big-endian** treats the *first* byte as the most significant:

    ```
    0x12 × 256  +  0x34        =  18 × 256 + 52  =  4660
    ```

    **Little-endian** treats the *last* byte as the most significant, so the
    same two bytes are read in the other order:

    ```
    0x34 × 256  +  0x12        =  52 × 256 + 18  =  13330
    ```

    Same bytes on disk. Two different numbers. Which is why it has to be
    agreed rather than assumed.

    **Ethereum is big-endian** — integers are serialised most-significant-byte
    first throughout the specification [(Wood, 2014)](#ref-wood-2014).

    The convenient consequence is that hex strings read in the direction you
    already expect. In decimal `1234`, the leftmost digit carries the largest
    place value; big-endian does the same thing with bytes, so `0x1234` is
    4660, exactly as the place-value calculation earlier gave.

    You can go a long way without thinking about this. It becomes unavoidable
    the moment you write code converting between numbers and bytes, which is
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
