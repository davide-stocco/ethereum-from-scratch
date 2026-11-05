---
tier: 1
description: The chain holds machine code, not the source you read on an explorer — and "verified" is somebody's claim that the two match.
---

# What the code actually is

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**[Permanent](../about/forks.md).** That a contract's code on-chain is bytecode, and that source is something kept elsewhere by people, has been true since 2015 and follows from the design rather than from any current practice.

## The thesis this page exists to argue

A reader finishing [what a smart contract is](smart-contracts.md) knows a contract is code at an address. They will almost certainly picture **Solidity** — the language they have seen in tutorials and on block explorers.

That isn't what's there. The chain holds **bytecode**: a sequence of operations for a machine, with no variable names, no comments, no function names and no types. Everything that makes source readable was discarded by the compiler and was never on-chain at all.

Which makes the thing people call "verified source code" a **claim**, not a fact: somebody uploaded source, somebody compiled it, and the result matched the bytecode at that address. Checkable, usually true, and not the same as the chain telling you anything.

## Questions this page should answer

- What is actually stored at a contract's address? (Bytecode. Show a short stretch of it so the reader sees what "the code" literally is.)
- Where did the source go? (Nowhere — it was never sent. Compilation is one-way in the practical sense: you can always read the bytecode and cannot recover the names and intent that produced it.)
- So what does "verified" mean on an explorer? (**The key section.** Somebody supplied source and compiler settings; the explorer compiled it and compared. It's a reproducible claim — and it depends on matching the exact compiler version and options, which is why verification sometimes fails for honest code.)
- Who is trusting whom, in that arrangement? (You trust the explorer to have compared honestly, or you do it yourself. Neither is the protocol telling you anything — the protocol knows only bytecode.)
- What if a contract is *not* verified? (It still works, it is still readable as bytecode, and you simply have less help. Unverified is not suspicious by itself — though it is a reason for care.)
- Can you tell what unverified bytecode does? (Partly. Decompilers exist and recover structure rather than meaning. Worth being honest: reading bytecode tells you what it *does*, never what it was *for*.)
- Does the compiler matter to the protocol? (Not at all. Ethereum has no notion of Solidity, or of any language. Worth saying plainly, since it's easy to assume the chain knows.)

## Notes to self

- **This sharpens the immutability section on the previous page.** "Code at an address is fixed" plus "you can always read it" sounds like full transparency. It isn't: you can read what a contract *does* and still not know what it was meant to do. That gap is this page's real payload.
- Do **not** teach Solidity, or any language. The point is the *relationship* between source and bytecode, which is language-independent and permanent.
- Keep compiler-version specifics out. That source and bytecode must be matched by exact version is durable; which versions exist is not.
- Likely diagram: source → compiler → bytecode, with the arrow one-way, and a dashed box showing which of the three the chain actually holds.
- Good place to note that the same reasoning applies to **any** published binary, and that Ethereum's unusual property is not that the code is readable but that **everybody is reading the same copy** — nobody can serve you different code from the code everybody else runs.

**Next:** [Events and logs](events-and-logs.md) — the one thing a contract can write and cannot read.
