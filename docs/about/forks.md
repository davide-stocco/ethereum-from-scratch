# Ethereum changes — how this site handles it

Ethereum is not finished, and it was never meant to be. It upgrades through **hard forks**: coordinated rule changes that every node on the network adopts at an agreed point. There have been roughly twenty since 2015, and more are planned.

Some were substantial. In September 2022, an upgrade called **The Merge** replaced Ethereum's entire consensus mechanism — the way the network agrees on the order of transactions — swapping mining for staking. In 2021, **EIP-1559** rebuilt how transaction fees are calculated. In 2024, **blobs** were introduced and made transactions on Layer 2 networks dramatically cheaper.

This creates an obvious problem for a site like this one. Plenty of Ethereum tutorials were accurate when written and are now quietly, confidently wrong. A reader has no way of telling which parts have gone stale.

So this site is built around a deliberate choice.

## Not everything changes

Hard forks sound like they churn everything, but they don't. The churn is concentrated, and a large part of how Ethereum works has not moved since the network launched in 2015:

- An **address** has always been the last 20 bytes of the Keccak-256 hash of a public key.
- A **private key** has always been a 256-bit number on the secp256k1 curve.
- There have always been exactly 10<sup>18</sup> **wei** in one ether.
- **RLP**, the encoding Ethereum uses to serialise data, has never been revised.
- The **nonce** has always been a simple per-account counter.
- Every **account** has always had the same four fields.

None of these can realistically change. Altering any one would break every wallet, library, block explorer and deployed contract simultaneously. They are, for practical purposes, permanent.

## What this site covers right now

**Only that permanent core.**

Everything currently published here has been true since 2015 and will almost certainly be true in twenty years. Nothing on this site depends on which fork is live as you read it.

That's a narrower site than it could be. It leaves out gas costs, the fee market, transaction types, Proof of Stake, and rollups — all genuinely important, and all things I intend to cover.

But it's the right place to start, for two reasons. The permanent material is **foundational**: you cannot understand why a storage write is expensive without first understanding what storage is, and you cannot follow a transaction's signature without knowing what a private key is. And it's **honest** — I'd rather publish a small site that stays correct than a large one that rots.

## How the rest will be added

When the fork-dependent sections arrive, they'll follow three rules.

**Numbers live in one place.** No page will ever hardcode a gas cost. Pages explain *why* an operation is expensive; a single reference table says *how much*. When a fork reprices something, one file changes.

**Volatile pages say so.** Any page whose details depend on the current fork will carry a visible note naming the upgrade it was written against, so you can judge for yourself whether it's current.

**Changes are taught as history, not patched over.** This is the useful part. EIP-1559 is confusing on its own, but obvious once you know what came before: fee bidding used to be a blind auction where you guessed what everyone else would pay, and usually overpaid or got stuck. The old design explains the new one.

So forks won't be errata buried in a changelog. Where something changed, you'll get the version before, the problem with it, and the version after — because that sequence is genuinely the clearest way to understand the thing as it stands today.

## If you find something wrong

Please tell me. This site is written in public, by someone learning the material, and corrections are the most useful thing you can offer. Open an issue on the repository.

For anything fork-dependent, the authoritative sources are always:

- <https://eips.ethereum.org> — the EIPs themselves
- <https://github.com/ethereum/execution-specs> — the executable specification
- <https://ethereum.org/en/history/> — the upgrade timeline
