# Ethereum from Scratch

Ethereum is usually explained badly. Most introductions either hand you a metaphor that falls apart the moment you look closely ("it's a world computer!") or drop you straight into Solidity code without saying what the machine underneath is actually doing.

This site tries something different, with two rules.

**Nothing is explained before its prerequisites.** Start at [What is Ethereum?](foundations/what-is-ethereum.md), work down the menu, and each page assumes you've read the ones above it and nothing more.

**Everything here is permanent.** Ethereum upgrades through hard forks, and plenty of tutorials that were accurate when written are now quietly wrong. So this site begins with the part of Ethereum that has **not changed since 2015** — and realistically cannot, because altering any of it would break every wallet, library and deployed contract at once.

That makes for a narrower site than it could be. It's also the part worth learning first.

---

## Where to start

<div class="grid cards" markdown>

- **[Foundations](foundations/what-is-ethereum.md)**

    What Ethereum actually is — a state machine — plus the units and the number formats you'll meet on every page after this.

- **[Cryptography](crypto/keccak256.md)**

    Hashing, private keys, public keys, and how an address is derived from them. One worked example, carried all the way through.

- **[Encoding](encoding/rlp.md)**

    RLP: how Ethereum turns structured data into bytes, and why it needed its own format rather than using JSON.

- **[Accounts](accounts/accounts.md)**

    The four fields every account has, and why an account-based design needs a nonce when Bitcoin's coin-based design doesn't.

</div>

---

## What's missing, and why

Gas costs, the fee market, transaction types, the EVM, Proof of Stake and rollups aren't here yet. They're all important, and they're all coming.

They're also the parts that **change at hard forks** — so they need a different treatment: numbers kept in one place, pages stamped with the upgrade they were written against, and changes taught as history rather than patched over.

[How this site handles forks](about/forks.md) explains the approach in full.

!!! note "Written in public"

    I'm building this while learning Ethereum myself. Pages marked *stub* are
    outlines I haven't filled in yet.

    If you spot a mistake, I'd genuinely like to know — corrections are the most
    useful thing you can offer. Open an issue on the repository.
