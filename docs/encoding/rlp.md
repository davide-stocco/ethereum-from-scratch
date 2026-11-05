---
tier: 1
description: RLP turns nested lists of bytes into one flat string of bytes, and its whole purpose is that each value has exactly one valid encoding.
---

# RLP encoding

**[Permanent](../about/forks.md).** Recursive Length Prefix has not been revised since Ethereum launched in 2015, and cannot be: every hash the network has ever agreed on was taken over bytes it produced.

!!! definition "RLP"

    **Recursive Length Prefix.** A way of turning nested lists of byte strings
    into one flat sequence of bytes, reversibly.

    It encodes exactly two things: a **byte string**, and a **list** of items
    which may themselves be strings or lists. Nothing else — no integers, no
    booleans, no names, no types.

    Its defining property is **canonicality**: each value has exactly one
    valid encoding, and anything else is rejected.

## It encodes two things, and nothing else

Start with what it refuses to do, because that is most of the design.

RLP has **no integers.** No booleans, no decimals, no field names, no types, no maps. The two things it knows about are a run of bytes and a list.

So `nonce: 3` isn't something RLP can express. What gets encoded is the byte `0x03`, in a particular position in a list, and **the position is what makes it the nonce.** Anything wanting to encode a number converts it to bytes first; anything wanting to label a field relies on the reader knowing the order.

That sounds like an omission and is a deliberate narrowing. A format that describes types has to have opinions about them — how big an integer may be, how text is encoded, what a missing field means — and every opinion is something two implementations could implement differently. RLP has almost nothing to disagree about.

## The four rules

That's the whole specification [(Wood, 2014)](#ref-wood-2014), and it fits in a table.

| First byte | Means |
| --- | --- |
| `0x00`–`0x7f` | this byte is the data, encoding itself |
| `0x80`–`0xb7` | a string of **0 to 55 bytes**; length is the byte minus `0x80` |
| `0xb8`–`0xbf` | a **longer string**; the byte minus `0xb7` says how many bytes of *length* follow |
| `0xc0`–`0xf7` | a **list** whose contents are 0 to 55 bytes; length is the byte minus `0xc0` |
| `0xf8`–`0xff` | a **longer list**; same length-of-the-length trick |

Two values worth memorising, because they turn up constantly: **`0x80` is the empty string** and **`0xc0` is the empty list.**

The fourth and fifth rows are the only clever part. A length under 56 fits in the prefix byte itself. Beyond that there isn't room, so the prefix instead says *how many bytes the length takes*, and the length follows. Hence the name: a prefix that describes a length, applied recursively to whatever is inside.

## Worked, byte by byte

**`"dog"`** → three bytes of data, so the prefix is `0x80 + 3`:

```
83 64 6f 67
^^ ^^^^^^^^
|  d  o  g
prefix: short string, 3 bytes
```

**`["cat", "dog"]`** → encode each, then wrap. `"cat"` is `83636174`, `"dog"` is `83646f67`, which is 8 bytes of contents, so the list prefix is `0xc0 + 8`:

```
c8 83 63 61 74 83 64 6f 67
^^ ^^^^^^^^^^^ ^^^^^^^^^^^
|     "cat"       "dog"
prefix: list, 8 bytes of contents
```

**`1024`** → first becomes the bytes `0x04 0x00`, then encodes as a two-byte string: `82 04 00`.

**The single byte `0x0f`** → `0f`. It's below `0x80`, so it encodes as itself with no prefix at all.

**The single byte `0x80`** → `81 80`. It is *not* below `0x80`, so it needs the prefix, and the result is two bytes where the input was one.

??? example "Try it: take any RLP apart"

    <div class="tool" markdown="0">
      <label for="rlp-in">RLP bytes, as hex</label>
      <input id="rlp-in" type="text" autocomplete="off" spellcheck="false" value="c88363617483646f67">
      <div class="tool__row">
        <button type="button" data-rlp="83646f67">"dog"</button>
        <button type="button" data-rlp="c88363617483646f67">["cat","dog"]</button>
        <button type="button" data-rlp="c7c0c1c0c3c0c1c0">nested lists</button>
        <button type="button" data-rlp="80">empty string</button>
        <button type="button" data-rlp="8100">non-canonical</button>
      </div>
      <p class="tool__out" id="rlp-out"></p>
    </div>

    Highlighted bytes are **prefixes** — structure rather than content. The
    number at the start of each line is the byte offset, so you can find any
    piece in the original hex.

    **Step 1 — press *nested lists*.** `c7c0c1c0c3c0c1c0` is eight bytes and
    contains six lists, three of them nested two deep. Every byte is either a
    prefix or a prefix inside a prefix: there is no data at all.

    **Step 2 — press *non-canonical*.** `8100` says "a one-byte string
    containing `0x00`". That value already has an encoding — the byte `0x00`
    on its own — so this one is rejected rather than tolerated. **The refusal
    is the feature**, for reasons the next section explains.

    **Step 3 — break something deliberately.** Change `c8` to `c9` in the
    second example: the list now claims nine bytes of contents and only eight
    follow, so it fails. RLP has no padding and no end markers, which means a
    single wrong byte is detected rather than silently reinterpreted.

## Why not JSON?

The obvious question. JSON exists, every language reads it, and it would have been free.

Because of what Ethereum does with these bytes: **it hashes them.** The state root, every transaction hash, every block hash — all are hashes of RLP-encoded data. And [Keccak-256](../crypto/keccak256.md) gives a completely different output for a single changed byte.

Now consider two programs encoding the same transaction as JSON. One writes `{"nonce":3,"gas":21000}`, the other `{"gas":21000, "nonce":3}`. Same data, different bytes, **different hash**. Add whitespace, key order, `3` versus `3.0`, escaped versus literal characters, and you have dozens of ways to write one value.

For an API that is harmless. For Ethereum it is fatal: two nodes with identical state would compute different state roots and reject each other's blocks, and the network would stop. The [state](../accounts/state.md) page's whole argument — *two nodes agreeing on 32 bytes agree on everything* — holds only if identical data always produces identical bytes.

So RLP is built around the opposite priority. **One value, one encoding, and every alternative rejected.** It isn't a better JSON; it's a format for a job JSON cannot do.

### Which is why there are no leading zeros

The same reasoning, applied to numbers.

The number 1 encodes as the byte `0x01`. It must *not* also be encodable as `0x0001`, or `0x000001` — because those are different bytes, and different bytes hash differently. So the rule is that a number's byte form carries no leading zeros, and an encoder that emits them has produced something a strict decoder will refuse.

Every canonicality rule has this shape. **A rule exists wherever a value could otherwise have been written two ways:** no leading zeros in numbers, no leading zeros in lengths, no long form where the short form fits, no prefix on a byte that encodes itself. Together they leave exactly one path from any value to its bytes.

## What RLP doesn't tell you

A thing people assume and shouldn't: **the bytes don't say what they mean.**

Decode a transaction and you get a list of byte strings. Nothing in it says which is the nonce, which is the recipient, or that the twenty-byte one is an address at all. A decoder returns structure; interpretation comes from the reader knowing what shape to expect.

Which is why the tool above can tell you that something is a three-item list of strings and not what any of it is *for*. Meaning lives in the specification and in the code, never in the encoding — the same division as the [ABI](../contracts/smart-contracts.md), where the protocol sees bytes and the convention supplies the names.

## Where it's used

Everywhere the execution layer writes something down:

- **Transactions**, so that signing has a defined set of bytes to sign
- **Block headers**, so that a block hash is the hash of something definite
- **Account entries** in the state, which is why the [accounts](../accounts/accounts.md) page described a state value as `RLP[nonce, balance, storageRoot, codeHash]`
- **Every node of the trie** — the [next page](merkle-patricia-trie.md) builds on this one for exactly that reason

So RLP is underneath every hash this site has mentioned. It is also the reason the trie page has to come after this one.

??? warning "RLP is no longer the only answer"

    Worth knowing, because "Ethereum uses RLP" is close to true and not quite.

    **Newer transactions are not plain RLP.** Since **EIP-2718**
    [(Zoltu, 2020)](#ref-eip2718), a transaction may be a single **type byte**
    followed by a payload, and the specification deliberately treats that
    payload as opaque bytes so that future types need not use RLP at all.
    Current types do use RLP inside the envelope, so in practice you decode
    the first byte, then decode the rest as RLP.

    **And the consensus layer doesn't use RLP at all.** It uses a different
    serialisation, chosen partly because RLP is awkward to produce proofs
    about. So the two halves of a node described on [clients and the two
    layers](../nodes/clients-and-layers.md) differ even in how they write
    bytes down.

    Neither changes anything on this page. RLP still encodes what it encodes,
    unchanged — it simply isn't the only format in the building any more.

---

## Recap

- RLP turns **nested lists of byte strings** into one flat byte sequence. It encodes strings and lists, and nothing else — no integers, no names, no types.
- A field is identified by **its position**, not by a label.
- **Four rules**, keyed on the first byte: self-encoding bytes below `0x80`, short strings from `0x80`, long strings from `0xb8`, lists from `0xc0`. `0x80` is the empty string; `0xc0` the empty list.
- Lengths under 56 fit in the prefix; beyond that the prefix says **how many bytes the length takes**.
- The reason for all of it is **canonicality**: one value, one encoding. Ethereum hashes these bytes, so two spellings of the same data would mean two different hashes and a network that cannot agree.
- Hence **no leading zeros**, no long form where short fits, no prefix on a self-encoding byte. **A rule exists wherever a value could have been written two ways.**
- JSON cannot do this job — key order and whitespace alone give one value many spellings.
- RLP carries **no meaning.** Decoding gives structure; what the fields *are* comes from the specification, like the ABI.
- Used for transactions, block headers, account entries and every trie node — so it sits underneath every hash on this site.
- **Not universal any more**: typed transactions wrap an opaque payload, and the consensus layer uses something else entirely.

**Next:** [The Merkle Patricia Trie](merkle-patricia-trie.md) — what the state root actually is, built out of RLP and hashes.

---

## References

<div class="sources" markdown>

- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Appendix B defines RLP in full, including the canonicality requirements this page describes. <https://ethereum.github.io/yellowpaper/paper.pdf>
- <a id="ref-eip2718"></a>**Zoltu, M.** (2020). *EIP-2718: Typed transaction envelope.* Ethereum Improvement Proposals. Introduces the type-byte prefix and deliberately treats the payload after it as opaque bytes, so that future transaction types need not be RLP. <https://eips.ethereum.org/EIPS/eip-2718>

</div>
