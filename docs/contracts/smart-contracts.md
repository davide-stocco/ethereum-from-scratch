---
tier: 1
description: What a smart contract actually is — code stored at an account, run by every node, unable to act on its own.
---

# What a smart contract is

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** What a contract *is* follows from [accounts](../accounts/accounts.md) and hasn't changed since genesis. What it *costs* to run, and which operations exist, are fork-dependent and belong to later pages.

## Questions this page should answer

- What is a contract, precisely? (Code stored at an account, under `codeHash`. Not a legal agreement, and "contract" is a misleading name — it's a program.)
- Who runs it? (Every node, independently, on the same inputs, reaching the same result. That's [determinism](../foundations/what-is-ethereum.md) again.)
- How does it get there? (A transaction that deploys code. The address is computed from the creator's address and [nonce](../accounts/nonce.md).)
- How does it run? (Only when called — by an EOA's transaction, or by another contract. Never on its own. The [accounts](../accounts/accounts.md) page establishes this; here it needs the detail.)
- What can it do? (Read and write its own storage, read some chain context, send ether, call other contracts, create contracts. Narrow list, deliberately.)
- What can it **not** do? (No clock of its own, no network access, no randomness, no file system. Everything it knows must be passed in or already on the chain — which is why [oracles](../glossary.md#oracle) exist.)
- Can a contract be changed after deployment? (Not the code at an address. The appearance of upgrades comes from one contract delegating to another whose address it stores — worth explaining, since "immutable" is widely overstated.)
- What is an ABI, and why is one needed? (Code sees bytes. The ABI is the convention for which bytes mean which function and arguments. A convention, not a protocol rule.)

## Already written: moved here from the accounts page

This box sat under the "only an EOA can start anything" rule on
[accounts](../accounts/accounts.md). The rule is a fact about kinds of account
and stays there; **this** is about what contracts can't do and how people work
around it, which is this page's subject. Build the surrounding section around
it rather than rewriting it.

??? question "Then how do things that look automatic work?"

    Somebody is sending transactions. The useful question is why they bother,
    and the answer is that they're paid to.

    Take a lending contract that must sell somebody's collateral when its value
    falls too far. The contract can't watch the price — per the rule above, it
    cannot do anything at all unless called. So it's built the other way round:
    it exposes a function **anybody may call**, which checks the price and
    performs the sale only if the condition genuinely holds. Until called, it
    sits inert.

    But the contract still *needs* that sale to happen, and promptly, or it
    takes a loss. So it offers a cut of the proceeds to whoever makes the call
    at the right moment. **That converts "something must watch the price" into
    a paid job, open to anyone** — which is the only way to get it done, since
    the contract cannot employ anybody and cannot act alone.

    Hence the racing. The reward goes to the caller whose transaction lands
    **first**, and only the first: every later call re-checks the condition,
    finds it no longer true, and does nothing. So the people doing this run
    software watching for the condition and compete to get their transaction
    in ahead of the others, because second place pays nothing.

    The pattern has a name — **keepers**, or bots. The automation is economic,
    not technical. Which makes "it executes automatically" a claim worth
    examining: the honest version is usually *somebody is paid to make it
    execute, and so far somebody has.* Let the reward stop covering the fee and
    the automation quietly stops.

## Notes to self

- The name is the first obstacle. Say plainly that it is neither smart nor a contract, then move on — people have met the term long before the mechanism, and the wrong mental model is the thing to dislodge.
- The strongest framing is **constraint, not capability**: a contract is a program with almost everything taken away — no clock, no network, no randomness, no way to start itself. Everything interesting about Ethereum follows from that list of absences, because each absence is what makes the result reproducible by every node.
- Resist explaining the EVM here. This page is *what a contract is*; the machine that executes it, its opcodes and their costs are later and are not fork-proof.
- Keep the upgradeability section short but do include it. It's the most common place where a reader's belief ("contracts can't change") and reality diverge.
- Likely place for an interactive tool: show a contract address being computed from creator address and nonce, since it's the one thing on the page that's a pure calculation.

**Next:** [RLP encoding](../encoding/rlp.md) — how Ethereum writes structured data down.

The machine that executes contract code, its operations and their costs come later, with [gas](../transactions/gas.md).
