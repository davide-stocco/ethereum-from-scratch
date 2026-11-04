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

## Notes to self

- The name is the first obstacle. Say plainly that it is neither smart nor a contract, then move on — people have met the term long before the mechanism, and the wrong mental model is the thing to dislodge.
- The strongest framing is **constraint, not capability**: a contract is a program with almost everything taken away — no clock, no network, no randomness, no way to start itself. Everything interesting about Ethereum follows from that list of absences, because each absence is what makes the result reproducible by every node.
- Resist explaining the EVM here. This page is *what a contract is*; the machine that executes it, its opcodes and their costs are later and are not fork-proof.
- Keep the upgradeability section short but do include it. It's the most common place where a reader's belief ("contracts can't change") and reality diverge.
- Likely place for an interactive tool: show a contract address being computed from creator address and nonce, since it's the one thing on the page that's a pure calculation.

**Next:** [RLP encoding](../encoding/rlp.md) — how Ethereum writes structured data down.

The machine that executes contract code, its operations and their costs come later, with [gas](../transactions/gas.md).
