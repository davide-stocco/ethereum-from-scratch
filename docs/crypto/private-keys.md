---
tier: 1
description: A private key is just a very large random number. Why that's enough, how large "large" is, and what owning ether actually consists of.
---

# Private keys

**Fork-proof.** 256-bit keys on the secp256k1 curve, unchanged since genesis.

A private key is **a number**. That's the whole of it.

!!! definition "Private key"

    A randomly chosen integer, 256 bits long — which from
    [hex and bytes](../foundations/hex-and-bytes.md) you'll recognise as 32
    bytes, or 64 hex characters.

    Whoever knows it can produce [signatures](signatures.md) for the matching
    [address](addresses.md), and that is the whole of what owning ether
    consists of.

Not a file, not a password, not a certificate issued by anyone. Nobody assigns it to you and no record exists of it anywhere.

??? example "Try it: make one"

    <div class="tool" markdown="0">
      <button id="key-gen" type="button">Generate a key</button>
      <p class="tool__out" id="key-out"></p>
    </div>

    Press it a few times. Nothing was registered, nobody was asked, no server
    was contacted — your browser picked a random number. **That is the entire
    process**, and it's the first genuinely strange thing about Ethereum: an
    account is not issued to you, it's a number you happened to choose.

!!! danger "Never send anything to a key from this page"

    To be precise about the risk, because it's easy to overstate and easy to
    understate.

    **Nothing is at risk right now.** The key you just generated controls an
    account that has never been used and holds nothing. There is nothing to
    steal.

    **The danger is only if you ever put value behind it.** And it's absolute,
    because of something worth stating plainly: **the private key is the
    complete secret.** There is nothing above it, beneath it, or alongside it
    — no password, no second factor, no account to lock. Anyone holding that
    number can sign for that address, and the network cannot tell them from
    you.

    This key has been generated in a browser and displayed on a screen, in a
    tab that is probably in your history, on a page any installed extension
    could read. That's fine for looking at. It is permanently unfit for
    holding anything, and no amount of later care fixes it.

    For real value, use wallet software that generates a key and never shows
    it to anyone, including you.

## How is one number enough?

A natural objection: if a key is just a number, surely someone can guess it?

They can't, and the reason is the size of the number. Private keys run up to about 2<sup>256</sup>:

```
2^256  =  115,792,089,237,316,195,423,570,985,008,
          687,907,853,269,984,665,640,564,039,457,
          584,007,913,129,639,936
```

Roughly **10<sup>77</sup>**. Written out, it's 78 digits. That number resists intuition completely, so rather than reach for an analogy, here's a calculation you can run yourself.

??? example "Try it: how long to guess a key?"

    Suppose every person alive were hunting for your key, each testing keys as
    fast as a modern machine can manage, for the entire history of the universe.

    <div class="tool" markdown="0">
      <label for="bf-rate">Keys per second</label>
      <input id="bf-rate" type="text" autocomplete="off" spellcheck="false" value="8e18">
      <label for="bf-years">For how many years</label>
      <input id="bf-years" type="text" autocomplete="off" spellcheck="false" value="13800000000">
      <p class="tool__out" id="bf-out"></p>
    </div>

    The defaults are 8 billion people × a billion keys per second each
    (8 × 10<sup>18</sup>), running for 13.8 billion years — the age of the
    universe.

    The result is around **1 in 10<sup>40</sup>**. Not "difficult". Not
    "takes a long time". After exhausting the universe's entire history with
    every human being and every machine, they would have searched a fraction
    of the keyspace too small to write comfortably.

    Try making the numbers absurd — a trillion keys per second, a trillion
    years. It barely moves.

This is why a key needs no protection beyond secrecy. There's no account to lock, no rate limit to enforce, nobody to appeal to. **The number itself is the security**, and guessing is not a strategy.

## The valid range

Almost any 256-bit number works, but not quite all of them. A private key must be at least 1 and **less than a specific constant** called the order of the curve, written *n*:

```
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
```

That's defined by **secp256k1**, the elliptic curve Ethereum uses [(SECG, 2010)](#ref-secg-2010) — the same one Bitcoin uses. Keys have to fall below it because of how the [public key](public-keys.md) is derived; the arithmetic happens in a group with exactly *n* elements, so numbers at or above *n* simply wrap around to ones below it.

??? abstract "How much of the range is excluded? Almost none."

    The gap between *n* and 2<sup>256</sup> is:

    ```
    2^256 - n  =  432,420,386,565,659,656,852,420,866,394,968,145,599
    ```

    Which looks enormous until you compare it to the space it sits in. The
    proportion of 256-bit numbers that are *too large* to be valid keys is
    about:

    ```
    3.7 × 10^-39      —  roughly 1 in 2.7 × 10^38
    ```

    So if you pick a random 256-bit number, the chance it's out of range is
    far smaller than the chance of guessing someone's key. Real
    implementations do check, and loop if the draw fails, but the branch
    essentially never runs.

    This is also why "a private key is a random 256-bit number" is a perfectly
    good working definition, even though it's not exactly true.

## What it's for

A private key does exactly one useful thing: it produces **signatures**.

A signature is a way of **proving you know a secret without telling anyone the secret.**

That sounds impossible, and with an ordinary password it is. If you prove you know a password by typing it in, whoever is on the other end now knows it too — you've handed over the very thing you were proving you had. Every proof costs you the secret.

A signature escapes that. Give your private key a message — say, "send 1 ether to Anna" — and it computes a value with two properties:

- **Anyone can check** that the value could only have been produced by someone holding the key for a particular [address](addresses.md).
- **The value reveals nothing** about the key. You can publish a thousand signatures and the key stays secret.

And a third property, which matters just as much: **the signature is bound to that one message.** Change a single byte — the amount, the recipient — and it stops checking out. So a signature isn't a reusable token the way a password is. It authorises exactly one thing, once.

??? note "It's not much like a handwritten signature"

    The word is unhelpful, because the everyday version works the opposite way.

    Your handwritten signature is **the same every time**, which is precisely
    its weakness: anyone who has seen it can attempt a copy, and a copy works
    on any document.

    A digital signature is **different for every message**. Signing two
    transactions gives two unrelated values, and neither is any use on a third.
    So there's nothing to copy. Seeing a million of someone's signatures tells
    you nothing you could use.

    Closer analogies are all imperfect, but the useful intuition is a lock that
    produces a different, publicly-checkable receipt for each thing you lock —
    rather than a stamp that leaves the same mark.

Transaction signing on Ethereum has worked this way with secp256k1 keys since the beginning [(Wood, 2014)](#ref-wood-2014). How the computation actually works is the subject of [signatures](signatures.md); for now, only the properties matter.

That's the mechanism behind every claim of ownership on Ethereum. Which leads to a definition worth stating bluntly, because it surprises people:

> **"Owning" ether means knowing a number.**

Nothing in the state records that an account belongs to you. The chain holds only a balance against an [address](addresses.md), entirely public, visible to everybody. What distinguishes you from everyone else looking at it is that you can produce valid signatures for it and they can't.

And the key is the **whole** secret, not one factor among several. Nothing else is checked: no password, no second device, no identity. A signature is valid or it isn't, and producing a valid one requires only the number.

So there's nothing to steal except the number — and nothing to lose except the number, which is the subject of [what losing your keys means](../wallets/losing-your-keys.md).

## What comes next

Two things follow from the key, in order:

1. The key is multiplied into a **[public key](public-keys.md)** — easy to compute forwards, infeasible to reverse.
2. The public key is hashed into an **[address](addresses.md)**.

Each step is one-way, which is why an address reveals nothing about the key behind it.

??? question "Seed phrases are not this"

    If you've used a wallet, you've probably met twelve or twenty-four words
    rather than a 64-character number, and may reasonably assume *that's* the
    private key.

    It isn't. Those words are a **seed**, and a repeatable procedure turns one
    seed into many private keys.

    The direction matters, because it's easy to get backwards. The seed sits
    **upstream** of your keys, not above them as some higher authority:

    ```
    seed  ──►  private key  ──►  address
    ```

    So a seed is a convenient way to *produce and re-produce* keys — which is
    why writing down twelve words can restore a whole wallet. But it is **not
    a second secret guarding them.** Once a private key exists, it stands
    alone: whoever has it can sign, and the seed is irrelevant to that.

    Ethereum itself has never heard of seed phrases. They're a wallet
    convention, and the protocol sees only keys and signatures. Covered under
    [wallets and seed phrases](../wallets/seed-phrases.md).

---

## Recap

- A private key is **a random 256-bit number**. Nothing more.
- Nobody issues it. You pick it, and the network never needs to know you did.
- There are about **10<sup>77</sup>** possibilities, which is why guessing is not a strategy — every human searching for the age of the universe covers around 1 in 10<sup>40</sup> of the space.
- It must be below the curve order *n*, which excludes about **1 in 10<sup>38</sup>** of all 256-bit numbers — so in practice, any random number will do.
- Its one job is producing **signatures**, and therefore **"owning" ether means knowing a number.**

**Next:** [Public keys](public-keys.md) — the one-way step that turns the key into something you can safely publish.

---

## References

<div class="sources" markdown>

- <a id="ref-secg-2010"></a>**Standards for Efficient Cryptography Group** (2010). *SEC 2: Recommended Elliptic Curve Domain Parameters*, version 2.0. Defines secp256k1, including the group order *n* quoted above. <https://www.secg.org/sec2-v2.pdf>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Appendix F specifies the use of secp256k1 for transaction signing. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
