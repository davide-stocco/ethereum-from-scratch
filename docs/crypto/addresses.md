---
tier: 1
description: An address is the last 20 bytes of the Keccak-256 hash of a public key — plus a checksum hidden in its capitalisation.
---

# Addresses

**Fork-proof.** Address derivation and EIP-55 checksums have never changed.

An address is the thing you actually paste into a wallet:

```
0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

!!! definition "Address"

    The **last 20 bytes of the Keccak-256 hash of a public key** — 40 hex
    characters, conventionally written with `0x` in front.

    It is the identifier everything on Ethereum is recorded against: balances,
    contract code, storage. Nothing distinguishes an address whose key someone
    holds from one nobody has ever computed.

Twenty bytes, forty hex characters. This is the last step of the chain and the simplest one: **hash the public key and keep the end of it.**

## The derivation

```
    private key          32 bytes
         │
         │   × G
         ▼
    public key           64 bytes
         │
         │   keccak256
         ▼
       hash              32 bytes
         │
         │   keep the last 20
         ▼
     address             20 bytes
```

[Private key](private-keys.md) to [public key](public-keys.md) by curve multiplication, public key to hash by [Keccak-256](keccak256.md), then discard all but the last 20 bytes. That's the whole derivation, and it's specified in exactly those terms — the rightmost 160 bits of the hash [(Wood, 2014)](#ref-wood-2014).

??? example "Try it: the whole chain, end to end"

    <div class="tool" markdown="0">
      <label for="addr-priv">Private key (hex)</label>
      <input id="addr-priv" type="text" autocomplete="off" spellcheck="false" value="1">
      <button id="addr-rand" type="button">Random key</button>
      <p class="tool__out" id="addr-out"></p>
    </div>

    Every step runs in your browser — the curve multiplication, the hash, the
    truncation.

    **Step 1 — start at `1` again.** The public key is G, exactly as on the
    previous page, and the address that falls out is
    `0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf`. That is a real address with a
    real transaction history, because private key 1 is the most-guessed key in
    existence.

    **Step 2 — look at the greyed-out part of the hash.** Those first 12 bytes
    are computed and then thrown away. Only the last 20 survive.

    **Step 3 — press Random key** a few times. This is precisely what a wallet
    does when it creates an account: pick a number, derive, hash, truncate.

## One private key gives exactly one address

Worth stating plainly, because the answer isn't obvious and wallets make it look otherwise.

**Every step in that chain is deterministic.** Multiplying by G has one answer. Keccak-256 has one answer. Taking the last 20 bytes has one answer. So a given private key produces one public key, which produces one address, and it will produce the same one on any machine, forever. There's no choice to make and no parameter to vary.

So how does your wallet show you a dozen addresses?

??? note "Because the wallet has a seed, not a key"

    This is the distinction from the [private keys](private-keys.md) page, and
    it's where it starts to matter.

    ```
                     seed
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      key #0       key #1      key #2        ← many keys, from one seed
          │           │           │
          ▼           ▼           ▼
      address 0   address 1   address 2      ← one address each
    ```

    The **seed** sits upstream and can generate an unlimited supply of private
    keys by a repeatable procedure. Each of those keys then yields exactly one
    address, by the chain on this page.

    So "many addresses from one thing" is true of a **seed** and false of a
    **private key**. Which is why writing down twelve words can restore a whole
    wallet, while a single private key only ever restores a single account.

    Mechanics under
    [wallets and seed phrases](../wallets/seed-phrases.md).

??? question "One key can *control* several addresses, though"

    A separate point, and easy to conflate with the above.

    A key is derived into one address. But that address can go on to **create
    contracts**, and each contract gets an address of its own — computed from
    the creator's address and [nonce](../accounts/nonce.md "A per-account counter of transactions already sent"),
    as the contract-addresses section below explains. Deploy ten contracts and
    there are ten more addresses under your control.

    Contracts can also simply be *configured* to obey a particular address,
    which is how multi-signature and smart-contract wallets work.

    So the precise statements are:

    - **derived from** your key: exactly one address, always
    - **controlled by** your key: as many as you care to create

    The chain on this page is about the first. Nothing about control is visible
    in an address.

## Why keep only 20 bytes?

Keccak-256 produces 32 bytes and an address is 20, so 12 bytes — 96 bits — are deliberately thrown away.

The reason is size. As the [public keys](public-keys.md) page argued, an address is an **identifier**: it gets stored, transmitted, logged and typed constantly. Trimming 32 bytes to 20 is a 37% saving, paid out on every transaction and every storage slot, forever.

The cost is a smaller space of possible addresses — 2<sup>160</sup> rather than 2<sup>256</sup>.

??? abstract "Is 2¹⁶⁰ enough?"

    A fair question, since discarding 96 bits is a deliberate weakening.

    ```
    2^160 ≈ 1.46 × 10^48
    ```

    But the number to compare against isn't 2<sup>256</sup>. The questions that
    matter are whether anyone could find **two** public keys hashing to the
    same address, or hit a **specific** address that already holds something.

    Finding a **collision** takes about 2<sup>80</sup> operations by the
    birthday bound — roughly 10<sup>24</sup>. Vastly beyond anything ever
    computed, but a far thinner margin than the 2<sup>128</sup> the rest of the
    stack enjoys. It's the main reason 20 bytes is occasionally criticised as
    too thrifty.

    Finding a **specific** address is 2<sup>160</sup>, which is hopeless in the
    same way guessing a private key is hopeless.

    So: comfortable, but the least comfortable link in the chain. A deliberate
    trade of margin for size.

## Every address already exists

A consequence of this design that surprises people: **nothing creates an address.**

All 2<sup>160</sup> of them are equally valid right now. The overwhelming majority have never been used and never will be. An "unused" address isn't absent from the state — it simply holds nothing, which is indistinguishable from not existing.

So you can send ether to an address nobody controls, and it will sit there permanently. There is no check, because there is nothing to check against: the network cannot tell an address whose private key exists from one whose key nobody has ever computed. They are identical objects.

This is why mistyping an address is unrecoverable, and why the next section exists.

## The capitalisation is a checksum

You'll meet the same address written both ways:

```
0xd8da6bf26964af9d7eed9e03e53415d37aa96045
0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

**Both are the same address.** Hex is case-insensitive, so as a number they're identical and either will work.

But the mixed-case version carries information. **EIP-55** [(Van de Sande & Velicanu, 2016)](#ref-eip55) hides a checksum in the *choice* of which letters are capitalised:

1. Take the lowercase address and hash it with Keccak-256.
2. Walk the address and the hash together, one character at a time.
3. Where the address has a letter `a`–`f`, capitalise it if the matching hash character is 8 or more. Leave digits alone.

The capitalisation is therefore determined entirely by the address — so a wallet can recompute it and compare.

??? example "Try it: check or compute a checksum"

    <div class="tool" markdown="0">
      <label for="sum-in">Address</label>
      <input id="sum-in" type="text" autocomplete="off" spellcheck="false" value="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045">
      <p class="tool__out" id="sum-out"></p>
    </div>

    **Step 1** — as given, the checksum is valid.

    **Step 2 — break it.** Change one capital letter to lowercase, or the
    reverse. The checksum fails and the offending character is highlighted.

    **Step 3 — paste an all-lowercase address.** It reports no checksum
    present, which is correct: a single-case address is valid and simply
    carries no protection.

    **Step 4 — change a *digit*** rather than the capitalisation. Now it's a
    different address, so the tool computes a different, perfectly valid
    checksum for it. Which is the point of the next section.

### What it catches, and what it doesn't

**It catches typos.** Mistype a character in a checksummed address and the capitalisation almost certainly stops matching, so a wallet refuses it before anything is sent. The chance of a random error still checksumming correctly is around 1 in 2<sup>40</sup>.

**It does not catch substitution.** Hand someone a *different* address, correctly checksummed, and it validates perfectly — because it is a correct checksum, for the wrong address. EIP-55 protects you from your own slips, not from being deceived.

That distinction is worth being firm about, because "the checksum passed" gets treated as a safety guarantee and is nothing of the kind.

??? info "History: EIP-55 is retrofitted, and it shows"

    Addresses had no checksum at all for Ethereum's first year. Mistype one
    and the funds went somewhere nobody controlled, with no warning.

    Fixing that properly would have meant changing the address format — which
    would have broken every wallet, contract and tool simultaneously. EIP-55's
    trick is that it changes **nothing**. The bytes are identical. The
    capitalisation was free information nobody was using. An old tool handing a
    lowercase address to a new one still works.

    The price of that compatibility is that the checksum is **optional**. A
    lowercase address remains valid, so a wallet cannot insist on a checksum —
    only verify one when it happens to be present. A format designed with a
    checksum from the outset would have made it mandatory.

    Neat engineering, and a good illustration of what retrofitting costs: not
    the mechanism, but its enforceability.

## Contract addresses

Contracts have addresses that look identical — 20 bytes, same format, same checksum rules — but they can't be derived from a public key, because a contract has no private key.

A contract's address comes instead from **the address that created it and that creator's [nonce](../accounts/nonce.md "A per-account counter of transactions already sent")**, hashed in much the same way. Which makes it predictable before the contract exists: you can know the address of your next deployment in advance.

Nothing in an address reveals which kind it is. The two are told apart by [what the account holds](../accounts/accounts.md), not by how the address looks.

---

## Recap

- An address is the **last 20 bytes of the Keccak-256 hash of the 64-byte public key.**
- The hash's first 12 bytes are computed and discarded, to keep identifiers short.
- There are 2<sup>160</sup> addresses and **all of them already exist.** Sending to an unowned one loses the funds permanently, and nothing can warn you.
- Mixed-case addresses carry an **EIP-55 checksum** in which letters are capitalised. Lowercase addresses are equally valid, with no protection.
- The checksum catches **typos**, not **deception**.
- **Contract addresses** derive from the creator's address and nonce, and look exactly the same.

**Next:** [Signatures](signatures.md) — how a private key proves control of an address without revealing itself.

---

## References

<div class="sources" markdown>

- <a id="ref-eip55"></a>**Van de Sande, A., & Velicanu, V.** (2016). *EIP-55: Mixed-case checksum address encoding.* Ethereum Improvement Proposals. Specifies the capitalisation rule, and supplies the test vectors used to verify the tool above. <https://eips.ethereum.org/EIPS/eip-55>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Defines an address as the rightmost 160 bits of the Keccak-256 hash of the public key, and gives the separate rule for contract addresses. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
