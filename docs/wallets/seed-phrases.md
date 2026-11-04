---
tier: 1
description: What a wallet actually holds, and how twelve ordinary words can stand behind an unlimited number of private keys.
---

# Wallets and seed phrases

**Fork-proof.** None of this is part of Ethereum. These are conventions built on top, and they haven't changed since they were written.

The [cryptography](../crypto/private-keys.md) section ended with a loose thread. A [private key](../crypto/private-keys.md) is one number and gives [exactly one address](../crypto/addresses.md) — yet every wallet you've used shows a list of addresses, and offers to restore all of them from twelve words.

This page is how those two facts fit together.

!!! definition "Wallet"

    Software that **stores private keys and signs things with them.** Not a
    container for money, and not an account — your ether is recorded on the
    network, not inside any app.

    A wallet's whole job is to keep your keys safe and use them when you ask.
    *Keyring* would have been the better word.

## A wallet doesn't hold your money

Worth unpacking that, because the usual word is actively misleading.

Your ether isn't in your wallet. It's a number recorded against your [address](../crypto/addresses.md) by every computer on the network — and your wallet is not one of them. Delete the app and the number is untouched. Install a different app and it still doesn't move.

What a wallet holds is **keys**, and what it does is sign things with them. A better name would be a keyring.

Which explains something that otherwise seems odd: you can load the same seed phrase into three different wallets at once and see the same balances in all three. Nothing was copied between them. All three can derive the same keys, so all three can produce the same [signatures](../crypto/signatures.md) — and all three are reading the same public records.

## What the phrase actually is

Before the tree: a seed phrase is **a number, written as words.** Twelve of them usually, sometimes twenty-four.

That's worth stressing, because the words look like something a person chose, and they aren't. Making a phrase goes like this:

1. Generate **random bits** — 128 of them for a twelve-word phrase.
2. Append a short **checksum** calculated from those bits.
3. Chop the result into groups of **11 bits**.
4. Read each group as a number from 0 to 2047, and use it to pick a word from a fixed list of exactly **2048 words**.

<svg viewBox="0 0 470 300" role="img" aria-label="128 random bits, here all zeros, with four checksum bits appended to make 132. The 132 bits are chopped into twelve groups of eleven. Each group is read as a number and picks that word from the list, so the first eleven groups are all zeros and give abandon, while the last group contains the four checksum bits, reads as three, and gives about." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="10" y="14" width="330" height="26" rx="3"/><rect x="348" y="14" width="40" height="26" rx="3" opacity="0.55"/><rect x="10" y="112" width="70" height="44" rx="3"/><rect x="86" y="112" width="70" height="44" rx="3"/><rect x="162" y="112" width="70" height="44" rx="3"/><rect x="238" y="112" width="70" height="44" rx="3"/><rect x="314" y="112" width="70" height="44" rx="3"/><rect x="390" y="112" width="70" height="44" rx="3"/><rect x="10" y="168" width="70" height="44" rx="3"/><rect x="86" y="168" width="70" height="44" rx="3"/><rect x="162" y="168" width="70" height="44" rx="3"/><rect x="238" y="168" width="70" height="44" rx="3"/><rect x="314" y="168" width="70" height="44" rx="3"/><rect x="390" y="168" width="70" height="44" rx="3" opacity="0.55"/><path d="M235 56 L235 76"/><path d="M368 46 L368 62 L300 62"/></g><g fill="currentColor" stroke="none"><path d="M230 76 L235 86 L240 76 Z"/><text x="175" y="32" font-size="11" text-anchor="middle">128 random bits &#8212; here, all zeros</text><text x="368" y="32" font-size="11" text-anchor="middle">+4</text><text x="296" y="66" font-size="9" text-anchor="end" opacity="0.8">4 checksum bits, worked out from those 128</text><text x="235" y="104" font-size="11" text-anchor="middle">132 bits, chopped into 12 groups of 11</text><text x="45" y="129" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="45" y="146" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="121" y="129" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="121" y="146" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="197" y="129" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="197" y="146" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="273" y="129" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="273" y="146" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="349" y="129" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="349" y="146" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="425" y="129" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="425" y="146" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="45" y="185" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="45" y="202" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="121" y="185" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="121" y="202" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="197" y="185" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="197" y="202" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="273" y="185" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="273" y="202" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="349" y="185" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000000</text><text x="349" y="202" font-size="10" text-anchor="middle" font-style="italic">abandon</text><text x="425" y="185" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.8">00000000011</text><text x="425" y="202" font-size="10" text-anchor="middle" font-style="italic">about</text><text x="10" y="240" font-size="10" opacity="0.85">Each group is a number from 0 to 2047, and it picks that word from the list.</text><text x="10" y="256" font-size="10" opacity="0.85">Eleven zero bits give word 0, which is <tspan font-style="italic">abandon</tspan>.</text><text x="10" y="280" font-size="10" opacity="0.85">The checksum lands inside the <tspan font-weight="700">last</tspan> group, making it 3 rather than 0 &#8212;</text><text x="10" y="294" font-size="10" opacity="0.85">which is why the phrase ends <tspan font-style="italic">about</tspan>, and not a twelfth <tspan font-style="italic">abandon</tspan>.</text></g></svg>

So `abandon` doesn't mean anything. It's word number 0 in the list, and it's there because eleven of your random bits happened to come out as zeros.

Nothing is remembered, chosen or looked up. The phrase **is** the number, in a form a human can copy onto paper without making mistakes.

## One phrase, many keys

Here's the structure, and the direction is what matters:

```
                     seed phrase
                          │
                          │  one-way
                          ▼
                     512-bit seed
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
      key #0          key #1          key #2        … unlimited
          │               │               │
          ▼               ▼               ▼
      address 0       address 1       address 2
```

The words are stretched into a single large number — the **seed** — and that seed can produce an endless supply of private keys. Each key then yields one address, exactly as the cryptography section described.

So "many addresses from one thing" is true of a **seed** and false of a **private key**.

??? abstract "The procedure that turns one seed into many keys"

    Worth seeing, because "a repeatable procedure" is doing a lot of work in
    that sentence.

    Every point in the tree holds **two** things: a private key, and a
    separate 32-byte value called a **chain code**. The seed gives you the
    first of each.

    To produce child number *i* from any point in the tree:

    ```
    1.  combine  the chain code, the parent's key material, and i
    2.  hash it  with HMAC-SHA512, giving 64 bytes
    3.  the first 32 bytes, added to the parent key, = the child's key
    4.  the last  32 bytes                          = the child's chain code
    ```

    Three properties follow, and they're the useful part:

    - **Deterministic.** The same seed and the same *i* always give the same
      key, on any machine, forever. That's what makes a written phrase a
      complete backup.
    - **One-way.** A child key reveals nothing about its parent, so exposing
      one account doesn't expose the others.
    - **Unlimited.** *i* can be any of about four billion values at every
      level, and the levels nest. You will not run out.

    This is BIP-32 [(Wuille, 2012)](#ref-bip32), and the tool below runs it.

<svg viewBox="0 0 470 232" role="img" aria-label="A tree. One seed leads to an account node at path m slash 44 slash 60 slash 0 slash 0, which branches from a single horizontal line into numbered children, each giving exactly one private key and one address. An ellipsis at the right shows the branching continues indefinitely." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="175" y="8" width="120" height="34" rx="4"/><path d="M235 42 L235 70"/><rect x="140" y="70" width="190" height="34" rx="4"/><path d="M235 104 L235 128"/><path d="M60 128 L436 128"/><rect x="24" y="152" width="72" height="46" rx="4"/><rect x="122" y="152" width="72" height="46" rx="4"/><rect x="220" y="152" width="72" height="46" rx="4"/><rect x="318" y="152" width="72" height="46" rx="4"/><path d="M60 128 L60 152"/><path d="M158 128 L158 152"/><path d="M256 128 L256 152"/><path d="M354 128 L354 152"/><path d="M424 128 L424 150" stroke-dasharray="3 3"/></g><g fill="currentColor" stroke="none"><text x="235" y="29" font-size="12" text-anchor="middle">the seed, 64 bytes</text><text x="235" y="92" font-size="12" text-anchor="middle" font-family="monospace">m/44'/60'/0'/0</text><text x="60" y="169" font-size="11" text-anchor="middle" font-weight="700">/0</text><text x="60" y="185" font-size="9" text-anchor="middle" opacity="0.75">one address</text><text x="158" y="169" font-size="11" text-anchor="middle" font-weight="700">/1</text><text x="158" y="185" font-size="9" text-anchor="middle" opacity="0.75">one address</text><text x="256" y="169" font-size="11" text-anchor="middle" font-weight="700">/2</text><text x="256" y="185" font-size="9" text-anchor="middle" opacity="0.75">one address</text><text x="354" y="169" font-size="11" text-anchor="middle" font-weight="700">/3</text><text x="354" y="185" font-size="9" text-anchor="middle" opacity="0.75">one address</text><text x="424" y="176" font-size="16" text-anchor="middle" opacity="0.7">&#8230;</text><text x="424" y="196" font-size="9" text-anchor="middle" opacity="0.7">and on,</text><text x="424" y="207" font-size="9" text-anchor="middle" opacity="0.7">without limit</text><text x="24" y="226" font-size="10" opacity="0.75">Same seed, same path, same addresses &#8212; in the same order, on any wallet.</text></g></svg>

Because that procedure is deterministic, the same phrase always produces the same keys, in the same order, on any wallet that walks the same route through the tree. **That** is what makes a written-down phrase a backup rather than merely a hint.

??? example "Try it: a phrase, and the addresses it produces"

    <div class="tool" markdown="0">
      <label for="hd-phrase">Seed phrase</label>
      <input id="hd-phrase" type="text" autocomplete="off" spellcheck="false" value="abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about">
      <label for="hd-pass">Passphrase (optional)</label>
      <input id="hd-pass" type="text" autocomplete="off" spellcheck="false" placeholder="usually empty">
      <p class="tool__out" id="hd-out"></p>
    </div>

    This is the real derivation, run in your browser — the same procedure your
    wallet performs.

    **Step 1 — look at the five addresses.** One phrase, five unrelated
    addresses, and it would go on indefinitely. This is what your wallet is
    doing when it shows you a list.

    Each address is shown with **the private key it was derived from**, in
    full. Those are real keys, and the only reason it is safe to print them
    here is that the phrase above is public. Compare any two: nothing in one
    hints at the other, and nothing in either hints at the phrase they both
    came from.

    **Step 2 — change one word.** Every address changes completely. There's a
    hash at the heart of this, so the [avalanche
    property](../crypto/keccak256.md) applies here too.

    **Step 3 — type something in the passphrase field.** Every address changes
    again, and you now have a *different wallet* from the same twelve words.
    More on that below.

    **Step 4 — type something that isn't a phrase at all.** `banana banana
    banana`, or your own name. It derives addresses from that too, perfectly
    happily.

    That is not a shortcoming of the tool; it is what the derivation does.
    Turning a phrase into a seed is one fixed calculation over the characters
    you typed, and it has no opinion about whether those characters were words.
    The wordlist and the checksum are checks a **wallet** runs *before* this
    point — which is why your wallet rejects a mistyped phrase and this tool
    accepts it. Worth noticing, because it's the same division as the `60` in
    the path: real rules, enforced entirely by software, nowhere in the
    protocol.

    The phrase shown is the standard test vector from the specification. It is
    famous, publicly known, and holds nothing — a good thing to experiment
    with, and the worst conceivable thing to use.

## Why words

A seed could perfectly well be written as hex. The reason it isn't:

- **You can copy words by hand without error.** Sixty-four hex characters transcribed onto paper is a mistake waiting to happen; `abandon` is not.
- **You can read them aloud**, and spell them if needed.
- **Most typos become detectable**, because the words come from a fixed list of 2048. Write `abandonn` and it simply isn't in the list, so a wallet can refuse it before deriving anything.
- **And part of the phrase is a checksum**, so a phrase with one word swapped for another valid word usually still fails.

### Where the numbers come from

The list holds exactly **2048 words**, and 2048 is 2<sup>11</sup>. That number was chosen for precisely that reason: picking one word out of 2<sup>11</sup> carries exactly **11 bits**, with nothing left over.

That makes the arithmetic tidy:

| Words | Bits total | Of which random | Of which checksum |
| --- | --- | --- | --- |
| 12 | 132 | **128** | 4 |
| 18 | 198 | 192 | 6 |
| 24 | 264 | **256** | 8 |

Which is where the twelve and the twenty-four come from. They aren't arbitrary, and they aren't the only lengths the standard allows — they're the two that land on round numbers of random bits. Twelve words is exactly 128 bits of randomness; twenty-four is exactly 256. Those were the two security levels anyone wanted, so those are the two counts you meet in practice.

??? warning "12 words is not half as strong as 24"

    It's 2<sup>128</sup> against 2<sup>256</sup> — and 2<sup>128</sup> is
    already far beyond reach, by the same argument as on the
    [private keys](../crypto/private-keys.md) page. Both are unguessable. The
    difference matters only against attacks that don't exist yet.

## The path, and why two wallets can disagree

The seed can produce unlimited keys, so something has to say **which** ones. That's the **derivation path** — the route taken down the tree. Wallets handling Ethereum keys have settled on this one:

```
m / 44' / 60' / 0' / 0 / 0
```

Read left to right, each segment picks a branch:

| Segment | What it selects |
| --- | --- |
| `m` | the seed itself — the root of the tree |
| `44'` | a standard structured layout, rather than an ad-hoc one |
| `60'` | **Ethereum.** 60 is the number registered for it in the wallet standard |
| `0'` | which account, if the wallet offers more than one |
| `0` | ordinary receiving addresses |
| `0` | the address index — 0, 1, 2, … the list your wallet shows you |

Note what that `60` is and isn't. It's an entry in a registry **wallet software keeps**, so that two wallets don't derive different keys for the same chain. Ethereum doesn't publish it, doesn't read it, and doesn't know it exists. The path is a convention among wallets about where to look — not something the protocol specifies.

Walk a different path and you get entirely different keys from the same seed. Which is exactly why **the same phrase can show different addresses in two different wallets** — not a bug, and not a lost wallet. The phrase was fine; the wallet was looking somewhere else in the tree.

??? abstract "The standards underneath, and what each one does"

    Three separate specifications stack up here, all of them originally
    Bitcoin's:

    | | Does what |
    | --- | --- |
    | **BIP-39** [(Palatinus et al., 2013)](#ref-bip39) | words ⇄ seed. Defines the 2048-word list, the checksum, and the function that stretches a phrase into a 512-bit seed |
    | **BIP-32** [(Wuille, 2012)](#ref-bip32) | seed → a tree of keys. Defines how a parent key and an index produce a child key |
    | **BIP-44** [(Palatinus & Rusnak, 2014)](#ref-bip44) | which branches to use. Defines the `m/44'/coin'/account'/change/index` layout and the registered coin numbers |

    The apostrophes mark **hardened** derivation — a variant that uses the
    parent *private* key rather than the public one, so a leaked child key and
    chain code can't be walked back up the tree.

    Stretching the phrase into a seed is deliberately slow: 2048 rounds of
    PBKDF2-HMAC-SHA512. That's not for elegance, it's to make guessing
    phrases expensive, which matters because human-chosen phrases would
    otherwise be weak.

??? question "Then what is the optional passphrase?"

    A thirteenth secret, mixed in when the phrase is stretched into a seed.
    Change it and you get a completely different tree — different keys,
    different addresses, everything.

    Which has an unusual consequence. **Any passphrase is valid**, so one
    phrase plus one passphrase is one wallet, one phrase plus a *different*
    passphrase is a different wallet, and there is no way to tell from the
    phrase alone which passphrase, if any, was meant. There's no "wrong
    passphrase" error, because there's nothing to check against — you simply
    land on an empty wallet.

    That's deliberate: it means a phrase found in a drawer doesn't
    necessarily unlock anything. It also means a forgotten passphrase is
    indistinguishable from a lost phrase. Try it in the tool above.

## Ethereum knows about keys. It has no idea how you got them.

That sentence is the whole boundary, and it's worth being exact about, because the claim gets both over- and under-stated.

**Keys are protocol.** Three things on the previous pages are written into the specification and enforced by every node: that an [address](../crypto/addresses.md) is derived from a public key in one particular way, that a public key comes from a private key on one particular curve, and that a [signature](../crypto/signatures.md) from that key is the only thing which can authorise a change to that address. Those rules are Ethereum.

**Where your key came from is not.** Nothing on *this* page — not seed phrases, not the key tree, not derivation paths — appears anywhere in Ethereum. The protocol cares that you hold a key. It has no interest in how you came by it.

### What a node actually sees

When you send a transaction, a node receives the fields plus `v`, `r` and `s`. It [recovers an address](../crypto/signatures.md), checks that account's nonce and balance, and executes.

Nothing in that sequence mentions a seed, a phrase, a path or a wallet. The node **cannot tell** whether your key came from twelve words, a hardware device, or a number you made up — and it has no way to ask.

### The dice test

Here's the version that settles it.

Roll a die 256 times. Write the results down as bits. Treat that number as a private key, derive the public key, derive the address, and send ether to it.

**Ethereum accepts that key exactly as readily as one from any wallet.** There's no registration step, no scheme to declare, nothing to opt into. There is no field anywhere that says *"this key was generated properly"*, because there would be nothing to put in it.

If the protocol cared where keys came from, that wouldn't work. It does work. So it doesn't care.

!!! danger "Don't actually do that"

    The dice test is sound as an argument and a poor idea in practice. Real
    dice are slightly biased, counting 256 results by hand goes wrong, and
    you'd have no checksum to catch the error — so you could lose everything
    to a miscount you never notice.

    It demonstrates what the protocol will accept. It is not a method.

### Then what is a seed phrase for?

It solves a **human** problem, not a protocol one.

A 64-character hex key is miserable to write on paper and verify, and you would need a fresh one for every account you wanted. So BIP-39 turns one number into words you can transcribe by hand, and BIP-32 turns one secret into a whole tree of keys so you never need to back up more than once.

Both are conveniences. Neither makes anything possible that wasn't possible before — you could always have written down raw keys, one per account, and Ethereum would have been equally content.

### Three things this explains

Each of them looks like a defect until you see where the line falls.

**Two wallets can show different addresses for the same phrase.**

Each wallet picks a path down the tree, and nothing *forces* two wallets to pick the same one. If Ethereum defined paths, they would all have to agree, because disagreeing would mean breaking the rules. Ethereum doesn't define them, so a wallet is free to look somewhere else — and some older ones did. Your keys weren't lost. The second wallet was reading a different branch of the same tree, and the addresses it showed you were real, just unused.

**A hardware wallet and a browser extension can share one phrase.**

Not because Ethereum coordinates them — it has no idea either exists. Because both vendors independently chose to implement the same three published standards. That's co-operation between competitors, which can be relied on in practice and could in principle stop at any time.

**Anyone could invent a different scheme tomorrow.**

A new way of turning a backup into keys would need no permission, no proposal, and no change to Ethereum — because Ethereum only ever sees the finished keys. It would need other wallets to adopt it to be *useful*, but nothing about the protocol would resist it.

That last point is the test for whether something is protocol or convention: **could you replace it unilaterally?** Seed phrases, yes. The curve that turns a private key into an address, no.

### What it does *not* mean

Not that wallets are unimportant. They're the only reason any of this is usable, and a flaw in one costs you everything. The point is narrower: the protocol doesn't **define** them — so they vary, compete, and improve without anyone needing to change Ethereum.

??? info "History: the boundary is starting to move"

    The clean story above is becoming less clean, and it's worth knowing which
    direction it's going.

    **Account abstraction** is, in part, about pulling wallet logic *into*
    contract code — so that "what authorises a transaction" can be a rule
    rather than a single key: several signers required, spending limits, a
    recovery procedure, fees paid by somebody else.

    That is the protocol beginning to care about something it had left
    entirely to software. The layer this page describes doesn't go away — a
    contract still ultimately checks signatures made by keys — but "one key,
    one account" stops being the only arrangement available.

    Everything in the [cryptography](../crypto/private-keys.md) section stays
    exactly as described. What changes is how much gets built on top of it.

---

## Recap

- A wallet holds **keys, not money.** Your ether is in the state; the wallet can only sign.
- A **seed** can produce unlimited private keys; a private key still gives exactly one address.
- Because the procedure is **repeatable**, the phrase is a complete backup.
- The word list is **2048 = 2<sup>11</sup>**, chosen so each word carries exactly 11 bits. That's why 12 words comes to 128 bits of randomness and 24 comes to 256, plus a checksum in each case.
- The **derivation path** decides which keys. Two wallets disagreeing about your addresses are walking different paths, not losing your money.
- The optional **passphrase** makes a different wallet from the same words, with no way to detect a wrong one.
- **None of it is part of Ethereum.** It's convention on top, and the protocol would not notice if it changed.

**Next:** [What losing your keys means](losing-your-keys.md) — the other side of holding the only secret.

---

## References

<div class="sources" markdown>

- <a id="ref-bip32"></a>**Wuille, P.** (2012). *BIP-32: Hierarchical Deterministic Wallets.* Bitcoin Improvement Proposals. Defines the key tree and the hardened/normal child derivation used above. <https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki>
- <a id="ref-bip39"></a>**Palatinus, M., Rusnak, P., Voisine, A., & Bowe, S.** (2013). *BIP-39: Mnemonic code for generating deterministic keys.* Bitcoin Improvement Proposals. Defines the 2048-word list, the checksum, and the PBKDF2 stretch verified against this specification's own test vectors. <https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki>
- <a id="ref-bip44"></a>**Palatinus, M., & Rusnak, P.** (2014). *BIP-44: Multi-Account Hierarchy for Deterministic Wallets.* Bitcoin Improvement Proposals. Defines the path layout and the coin number 60 used for Ethereum. <https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki>

</div>
