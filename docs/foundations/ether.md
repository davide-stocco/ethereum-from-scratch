---
tier: 1
description: Ether, wei and gwei — what the units are, why Ethereum counts in whole numbers of wei, and why decimals would break consensus.
---

# Ether, wei and gwei

**Fork-proof.** 10<sup>18</sup> wei per ether, fixed since genesis.

!!! definition "Ether · wei"

    **Ether** is Ethereum's native currency, ticker ETH. You need it to pay
    for anything the network does on your behalf.

    **Wei** is the unit it is counted in — 10<sup>18</sup> wei to one ether.
    Every amount on Ethereum is a whole number of wei. The protocol has no
    decimals anywhere.

## Ethereum is the network. Ether is the currency.

**Ethereum** is the network — the [state machine](what-is-ethereum.md), the computers running it, the rules they follow. **Ether** is what moves across it.

So "I sent you 2 Ethereum" is wrong in the same way "I paid you 50 Visa" is wrong. You send *ether*; Ethereum is the thing that moves it.

One consequence worth having early: ether isn't only money for buying things. **You need ether to do anything at all**, because every transaction costs a fee and fees are payable only in ether.

This has a consequence people meet in practice. Suppose an account holds a large amount of some token — a stablecoin, say — and no ether. It can still *receive* things, since receiving requires no transaction from you. But it cannot **send** anything, including the tokens it holds, because sending means submitting a transaction and there's no ether to pay the fee with. The tokens are visible, owned, and stuck until somebody sends a little ether to the account.

??? note "What is an ether worth?"

    Whatever people are currently willing to pay for it. The price is set by
    markets, it moves constantly, and it has ranged over several orders of
    magnitude across Ethereum's life.

    **There's deliberately no number on this page.** Any figure written here
    would be wrong within hours, and a reference page that quietly goes stale
    is worse than one that declines to answer. For a current price, any
    exchange or market tracker will tell you.

    The more useful thing to understand is what the price *means*. Because you
    pay for computation in ether, the price of ether is also **the cost of
    using Ethereum**. When ether gets more valuable, every transaction gets
    more expensive in real terms — which is why fees are discussed so
    obsessively, and why the network's capacity matters so much.

    Two structural points, which don't change with the price:

    - There is **no fixed supply cap**. Bitcoin has one; Ethereum does not.
      New ether is issued to reward validators, and some is destroyed when
      fees are paid, so the total can rise or fall over time.
    - Ether is **not backed by anything** and makes no promise of value. It's
      useful because the network is useful, and valuable because people want
      it. Nothing more solid than that.

## Wei is the smallest unit

There are **10<sup>18</sup> wei** in one ether — a billion billion. Wei is the unit the specification itself counts in: the Yellow Paper defines balances and fees in wei throughout, and treats ether as a denomination on top [(Wood, 2014)](#ref-wood-2014).

```
1 ether = 1,000,000,000,000,000,000 wei
```

It's named after **Wei Dai**, a cryptographer who in 1998 described *b-money* [(Dai, 1998)](#ref-dai-1998), one of the ideas that fed into cryptocurrencies. Several other units were defined early on with similar namesakes, and almost nobody uses them. In practice you'll meet three: **wei, gwei, ether.**

### Yes — wei is Ethereum's satoshi

The comparison is exact in role, and the difference is only in scale:

| | Bitcoin | Ethereum |
| --- | --- | --- |
| Currency | bitcoin | ether |
| Smallest unit | satoshi | wei |
| How many per unit | 10<sup>8</sup> (100 million) | 10<sup>18</sup> (a billion billion) |
| Decimal places | 8 | 18 |

Both systems do the same thing for the same reason: pick a smallest unit, count only in whole numbers of it, and let software display the friendly version.

**And wei is genuinely indivisible.** There is no sub-wei unit and no way to hold half a wei — not because nobody has defined one, but because balances are whole numbers and a fraction of the smallest unit cannot be represented. One wei is the atom.

## Ethereum never stores a decimal point

This is the part that matters, and it's not a detail.

Every balance, every transfer, every fee is a **whole number of wei**. Your wallet showing "2.5 ETH" is doing a presentation trick. What the chain actually holds is:

```
2500000000000000000
```

The decimal point is a display choice made by software. It does not exist anywhere in the protocol.

### Why integers? Because of determinism

Recall what the previous page established: thousands of computers each apply the rules independently and must arrive at an **identical** answer. That's what makes checking possible, and therefore what makes trust unnecessary.

Now try computing `0.1 + 0.2` on a computer. In most programming languages you don't get `0.3` — you get `0.30000000000000004`. Computers store fractions in binary, and plenty of ordinary decimals have no exact binary form, so there is always rounding. Worse, exactly *how* it rounds can differ between processors, compilers and languages [(Goldberg, 1991)](#ref-goldberg-1991).

For most software a rounding error in the seventeenth decimal place is harmless. For Ethereum it is fatal. If two nodes computed the same balance and got answers differing by one part in a quadrillion, **they would disagree about the state** — and there would be no single answer for the network to agree on. The whole structure depends on arithmetic that comes out the same everywhere, every time.

Integer arithmetic has no such problem. It is exact, and identical on every machine ever built. `2500000000000000000 − 1000000000000000000` is the same number in every language, on every processor, forever.

So the rule, and it's a consequence rather than a preference:

> **Count in the smallest unit. Use integers only. Let the display layer put the dot in.**

??? abstract "Why 10<sup>18</sup>, and not as fine as the machine allows?"

    A fair question: the EVM works on 256-bit unsigned integers, so it could
    represent roughly 1.16 × 10<sup>77</sup> distinct values. Why stop at
    10<sup>18</sup> subdivisions rather than using everything available?

    **Because you need arithmetic headroom.** Contracts don't just store
    balances, they compute with them — multiplying an amount by a price, by an
    interest rate, by a share. Multiplication is where it hurts: multiply two
    numbers that each use half the available bits and the result overflows.

    The numbers work out comfortably. Total ether supply is on the order of
    10<sup>26</sup> wei, which occupies about 87 of the 256 bits available. That
    leaves roughly 169 bits spare for intermediate results — enough that
    ordinary arithmetic on realistic balances cannot overflow. Had ether been
    subdivided as finely as the type allows, every balance would consume the
    whole word and any multiplication would be unsafe.

    **And more precision would be useless.** 18 decimal places already lets you
    express a quantity far smaller than any amount anyone could meaningfully
    transact. The constraint on usefulness is economic, not arithmetic.

    **18 is also simply convenient.** It's a round power of ten, so converting
    is moving a decimal point rather than doing a calculation, and "18 decimals"
    became the convention most tokens follow in turn.

## Why fees are quoted in gwei

**One gwei is 10<sup>9</sup> wei** — a billion wei. The prefix is *giga*, so written out in full the unit is *gigawei*.

It exists for one reason: readability.

An example will make that obvious far quicker than an argument would — and setting one up needs just a single piece of background.

A fee on Ethereum isn't a flat charge. It's a **price per unit of computational work**, and that unit is called **[gas](../glossary.md#gas "The unit computational work is measured in")** — which gets a page of its own later. All that matters here is that a fee comes out as a price, and prices need a unit to be quoted in.

Write one such price three ways and the choice makes itself:

| Unit | The same gas price |
| --- | --- |
| wei | `20000000000` |
| ether | `0.00000002` |
| **gwei** | **`20`** |

Gas prices land naturally in the single-to-low-hundreds range when written in gwei, so that's what wallets and fee trackers use. Nothing deeper than that: it's simply the scale at which the numbers are readable.

??? note "Gwei, gwei or gigawei?"

    All three appear in the wild, and no standard settles it. Two things can be
    said definitely.

    **Spelled out in full, it's one word: *gigawei*.** Metric prefixes never
    take a space — gigawatt, not giga watt — so "giga wei" isn't right.

    **In code it is always lowercase.** Solidity accepts `wei`, `gwei` and
    `ether` as suffixes on a numeric literal, and those keywords are
    case-sensitive [(Solidity documentation, v0.8.26)](#ref-solidity-units):

    ```solidity
    assert(1 wei == 1);
    assert(1 gwei == 1e9);
    assert(1 ether == 1e18);
    ```

    That list has itself shrunk, incidentally, which is some evidence for how
    unsettled the naming is: `szabo` and `finney` were once valid suffixes too,
    and have since been removed from the language.

    **That's the reason this site writes lowercase everywhere.** Prose and code
    then agree, and there's no sense in spelling the same unit two ways inside
    one project. Capitalised *Gwei* is perfectly defensible — block explorers
    and market sites commonly use it — but choosing it means every code example
    on the site contradicts the surrounding text, for no gain.

    Lowercase also happens to match how SI writes spelled-out units named after
    people: volt, watt, newton. That's a weaker argument though, since wei is
    not an SI unit and the analogy is just an analogy. The compiler is a rule.


## The conversion table

| Unit | Wei | In ether |
| --- | --- | --- |
| 1 wei | `1` | 0.000000000000000001 |
| 1 gwei | `1000000000` | 0.000000001 |
| 1 ether | `1000000000000000000` | 1 |

Going from ether to wei means moving the decimal point **18 places right**. From gwei to wei, **9 places right**. That's the whole arithmetic.

---

## Recap

- **Ethereum** is the network, **ether** is its currency. You need ether to use the network at all.
- **Wei** is the smallest unit: 10<sup>18</sup> per ether, and genuinely indivisible. It's Ethereum's equivalent of Bitcoin's satoshi, just far finer.
- **The protocol holds only whole numbers of wei.** The decimal point you see is added by software.
- That's required, not stylistic: **decimal fractions round differently on different machines**, nodes would disagree, and determinism would break.
- Fees are quoted in **gwei** (10<sup>9</sup> wei), the scale at which they read most easily.

**Next:** [Hex and bytes](hex-and-bytes.md) — how those numbers are actually written down.

---

## References

<div class="sources" markdown>

- <a id="ref-dai-1998"></a>**Dai, W.** (1998). *b-money.* <http://www.weidai.com/bmoney.txt>
- <a id="ref-goldberg-1991"></a>**Goldberg, D.** (1991). *What every computer scientist should know about floating-point arithmetic.* *ACM Computing Surveys*, 23(1), 5–48. <https://doi.org/10.1145/103162.103163>
- <a id="ref-solidity-units"></a>**Solidity documentation**, v0.8.26. *Units and globally available variables.* Documents `wei`, `gwei` and `ether` as case-sensitive suffixes on numeric literals. Version-pinned deliberately: the `latest` URL moves, and `szabo` and `finney` were removed from earlier versions. <https://docs.soliditylang.org/en/v0.8.26/units-and-global-variables.html>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Defines wei as the base unit of account. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
