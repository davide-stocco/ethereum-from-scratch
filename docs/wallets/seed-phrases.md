---
tier: 1
description: What a wallet actually holds, and how twelve ordinary words can stand behind an unlimited number of private keys.
---

# Wallets and seed phrases

**Fork-proof.** None of this is part of Ethereum. These are conventions built on top, and they haven't changed since they were written.

The [cryptography](../crypto/private-keys.md) section ended with a loose thread. A [private key](../crypto/private-keys.md) is one number and gives [exactly one address](../crypto/addresses.md) — yet every wallet you've used shows a list of addresses, and offers to restore all of them from twelve words.

This page is how those two facts fit together.

## A wallet doesn't hold your money

Worth clearing up first, because the word is actively misleading.

Your ether isn't in your wallet. It isn't anywhere except [the state](../accounts/state.md) — a number recorded against your address on thousands of machines. Deleting your wallet app doesn't move it. Installing a different one doesn't move it either.

What a wallet holds is **keys**, and what it does is sign things with them. A better name would be a keyring.

Which explains something that otherwise seems strange: you can "import" the same seed phrase into three different wallets at once and see the same balances in all three. Nothing was copied. All three are looking at the same public state, and all three can produce the same signatures.

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

The phrase becomes a single large number — the **seed** — and that seed can generate an endless supply of private keys by a repeatable procedure. Each key then yields one address, exactly as the cryptography section described.

So "many addresses from one thing" is true of a **seed** and false of a **private key**. And because the procedure is repeatable, the same phrase always produces the same keys, in the same order, on any wallet that follows the same rules. That's what makes a written-down phrase a backup.

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

    **Step 2 — change one word.** Every address changes completely. There's a
    hash at the heart of this, so the [avalanche
    property](../crypto/keccak256.md) applies here too.

    **Step 3 — type something in the passphrase field.** Every address changes
    again, and you now have a *different wallet* from the same twelve words.
    More on that below.

    The phrase shown is the standard test vector from the specification. It is
    famous, publicly known, and holds nothing — a good thing to experiment
    with, and the worst conceivable thing to use.

## Why words

A seed could perfectly well be written as hex. The reason it isn't:

- **You can copy words by hand without error.** Sixty-four hex characters transcribed onto paper is a mistake waiting to happen; `abandon` is not.
- **You can read them aloud**, and spell them if needed.
- **Most typos become detectable**, because the words come from a fixed list of 2048. Write `abandonn` and it simply isn't a word in the list.
- **And part of the phrase is a checksum**, so a phrase with one word swapped for another valid word usually still fails.

### Where the numbers come from

The list holds exactly **2048 words**, and 2048 is 2<sup>11</sup> — so each word carries precisely **11 bits**.

That makes the arithmetic tidy:

| Words | Bits total | Of which random | Of which checksum |
| --- | --- | --- | --- |
| 12 | 132 | **128** | 4 |
| 18 | 198 | 192 | 6 |
| 24 | 264 | **256** | 8 |

Which answers a question people often ask: why 12 and 24, rather than any number of words? Because 12 words is exactly 128 bits of randomness and 24 words is exactly 256, with the remainder a checksum. Those are the two security levels anyone wanted, so those are the two counts you meet.

??? warning "12 words is not half as strong as 24"

    It's 2<sup>128</sup> against 2<sup>256</sup> — and 2<sup>128</sup> is
    already far beyond reach, by the same argument as on the
    [private keys](../crypto/private-keys.md) page. Both are unguessable. The
    difference matters only against attacks that don't exist yet.

## The path, and why two wallets can disagree

The seed can produce unlimited keys, so something has to say **which** ones. That's the **derivation path**, and for Ethereum it conventionally looks like this:

```
m / 44' / 60' / 0' / 0 / 0
│    │     │     │   │   └── address index — 0, 1, 2, … the list your wallet shows
│    │     │     │   └────── 0 for ordinary receiving addresses
│    │     │     └────────── account number, if the wallet offers separate accounts
│    │     └──────────────── 60 means Ethereum
│    └────────────────────── 44 means "this is a standard structured path"
└───────────────────────────  the seed itself
```

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

## None of this is Ethereum

Worth saying plainly, because it explains most of the confusion in this area.

**Ethereum has never heard of seed phrases.** It has no concept of a wallet, a seed, a derivation path or an account list. It sees [addresses](../crypto/addresses.md), [signatures](../crypto/signatures.md) and nothing else.

Every mechanism on this page is a convention that wallet software agreed on, invented for Bitcoin and adopted wholesale. Which is why:

- different wallets can disagree about your addresses — they're following conventions, not rules
- a hardware wallet and a browser extension can share one phrase
- none of this appears anywhere in the Yellow Paper
- and it could all be replaced tomorrow without touching Ethereum at all

That last point is already happening, incidentally. [Account abstraction](../crypto/addresses.md) moves the whole question of "what authorises a transaction" into contract code, where a single key need not be the answer. But the protocol underneath stays exactly as the cryptography section described it.

---

## Recap

- A wallet holds **keys, not money.** Your ether is in the state; the wallet can only sign.
- A **seed** can produce unlimited private keys; a private key still gives exactly one address.
- Because the procedure is **repeatable**, the phrase is a complete backup.
- The word list is **2048 = 2<sup>11</sup>**, so 12 words carries 128 bits of randomness and 24 carries 256, plus a checksum in each case.
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
