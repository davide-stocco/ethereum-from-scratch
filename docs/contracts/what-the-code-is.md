---
tier: 1
description: The chain holds machine code, not the source you read on an explorer — and "verified" is somebody's claim that the two match.
---

# What the code actually is

**[Permanent](../about/forks.md).** That a contract's code on-chain is bytecode, and that source is something kept elsewhere by people, has been true since 2015 and follows from the design rather than from any current practice.

!!! definition "Bytecode"

    The actual contents of a contract's code: **a sequence of bytes, each one
    an instruction** for the machine that runs contracts, with constants mixed
    in between them.

    No variable names, no function names, no comments, no types. Those exist
    in **source code**, which is a separate file kept by people somewhere else
    and has never been on the chain at all.

When somebody writes a contract, they write it in a programming language — text with names, comments and structure, meant for people to read. The most widely used one is **[Solidity](../glossary.md#solidity "The language most Ethereum contracts are written in")**, though several others exist.

**That text never reaches the chain.** It goes through a *compiler*, a program that translates it into instructions a machine can execute, and only that output is sent.

So two different things get called "the code", and almost everything confusing here comes from running them together:

- **Source** — what a person wrote and can read. Kept on somebody's computer.
- **Bytecode** — what the compiler produced. The only one Ethereum has ever seen.

## What is actually at the address

Ask a node for the code at a contract's address and you get something like this:

```
6080604052348015600f57600080fd5b50...
```

That is the code. Not a description of it — the thing itself.

And it *is* readable, in a narrow sense. Each byte is an instruction, so the beginning of that run says:

```
60 80     PUSH1 0x80      put the value 0x80 on the stack
60 40     PUSH1 0x40      put the value 0x40 on the stack
52        MSTORE          write one to memory at the other
```

Three instructions, entirely unambiguous — and they tell you **nothing about what the contract is for.** They are the opening move of almost every Solidity contract: housekeeping, done before any of its actual business starts.

That gap — between what the code *does* and what it is *for* — is this page's subject.

## Where the bytecode is kept

The [accounts](../accounts/accounts.md) page said an account holds four fields, one of which is `codeHash` — **a 32-byte hash, not the code itself.** So where is the code?

**On every node.** All of it, on each of them.

Code is part of the [state](../accounts/state.md), and the state is the thing every node holds a complete copy of. So every node that can check a block holds the bytecode of every contract that exists — exactly as it holds every balance and every storage slot. Nothing is kept on one special machine, nothing has to be fetched from anybody, and there is no question of *which* node has it. They all do.

That is worth being emphatic about, because the word "hash" invites the wrong picture. `codeHash` is **not** a reference to somewhere else on the network. It is a key into the node's **own** storage, on its own disk, a few millimetres from the account entry that mentions it.

??? abstract "Then why keep the code out of the account entry at all?"

    Three reasons, all about size.

    **The entry stays small.** An account is four fields and must be a fixed,
    tidy size whether its code is fifty bytes or fifty thousand. Holding a
    32-byte hash achieves that; holding the code would not.

    **Identical contracts share one copy.** Two deployments of the same
    bytecode have the same `codeHash`, so there is nothing to store twice.
    The account entries differ; the code they point at is one object.

    **And code never changes.** Once deployed it is fixed, so unlike a balance
    it never needs rewriting — which makes it exactly the sort of thing to
    keep to one side and refer to, rather than carry around.

### How a node knows it has the right code

By hashing it.

Hand a node some bytes claiming to be a contract's code and it hashes them, compares the result with the `codeHash` in that contract's account, and rejects them if they differ. Nothing is taken on trust, which is the same move as everywhere else on this site.

And `codeHash` is itself covered by the [state root](../accounts/state.md), which the block header commits to. So the commitment runs all the way down:

```
block header → state root → the account entry → codeHash → the code
```

Alter one byte of a contract's code and its hash changes, so the account entry changes, so the state root changes, so the block header is wrong. **A contract's code is committed to exactly as firmly as anybody's balance** [(Wood, 2014)](#ref-wood-2014).

??? note "And how does it get called?"

    Mechanically: a transaction naming the contract's address as its
    recipient, carrying some bytes as input. The node looks up the account,
    fetches the code by its `codeHash`, and runs it with those input bytes
    available to it.

    Which bytes mean which function is the **ABI** convention from the
    [previous page](smart-contracts.md) — the protocol just hands the code
    whatever was sent. The anatomy of the transaction that does this belongs
    with [transactions](../transactions/transactions.md).

## Where the source went

Nowhere. It was never sent.

<svg viewBox="0 0 470 240" role="img" aria-label="Source code passes through a compiler and becomes bytecode. Only the bytecode is inside a dashed box marked as what the chain holds. A crossed-out arrow pointing back from bytecode to source shows there is no way to recover the names, comments and types the compiler discarded." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="10" y="40" width="124" height="76" rx="5"/><rect x="166" y="60" width="86" height="36" rx="5"/><rect x="278" y="22" width="180" height="112" rx="8" stroke-dasharray="5 4" opacity="0.5"/><rect x="292" y="40" width="152" height="76" rx="5"/><path d="M134 78 L160 78"/><path d="M252 78 L286 78"/><path d="M292 162 L140 162" stroke-dasharray="4 3" opacity="0.55"/><path d="M209 154 L223 170"/><path d="M223 154 L209 170"/></g><g fill="currentColor" stroke="none"><path d="M160 73 L170 78 L160 83 Z"/><path d="M286 73 L296 78 L286 83 Z"/><path d="M150 157 L140 162 L150 167 Z"/><text x="22" y="34" font-size="10" opacity="0.75">what you read</text><text x="22" y="60" font-size="11" font-weight="700">source</text><text x="22" y="78" font-size="9" opacity="0.85">names, comments,</text><text x="22" y="91" font-size="9" opacity="0.85">types, structure,</text><text x="22" y="104" font-size="9" opacity="0.85">intent</text><text x="178" y="82" font-size="11">compiler</text><text x="292" y="16" font-size="10" opacity="0.75">what the chain holds</text><text x="304" y="60" font-size="11" font-weight="700">bytecode</text><text x="304" y="78" font-size="9" opacity="0.85">one byte per</text><text x="304" y="91" font-size="9" opacity="0.85">instruction, and</text><text x="304" y="104" font-size="9" opacity="0.85">nothing else</text><text x="238" y="186" font-size="9" text-anchor="middle" opacity="0.8">no way back</text><text x="14" y="214" font-size="10" opacity="0.85">The compiler throws away everything that made the source readable. Nothing</text><text x="14" y="228" font-size="10" opacity="0.85">on the chain ever held it, so nothing on the chain can give it back.</text></g></svg>

A compiler's job is to produce something a machine can execute, and everything that made the source comprehensible to *you* is surplus to that: the names you chose, the comments you wrote, the types you declared, the structure you imposed. All of it is used during compilation and then discarded.

So the relationship is **one-way in the practical sense.** Given the source you can always produce the bytecode. Given the bytecode you cannot produce the source, because the information isn't missing from the chain — it was never in the bytecode to begin with.

## So what does "verified" mean?

Open a contract on a block explorer and you may well see readable Solidity, with names and comments, laid out in files. Given everything above, where did that come from?

**Somebody uploaded it.** The author, usually, or anyone who had it. They supplied the source and the exact compiler settings; the explorer compiled it itself and checked whether the result matched the bytecode already at that address. If it matched, the source is displayed and the contract is marked **verified**.

So "verified" is a precise and limited claim:

> **Somebody produced source that compiles to exactly these bytes.**

That is genuinely useful — it is very strong evidence that the source you are reading is the source that produced the contract, because producing different source that compiles to identical bytes is not something you can do by accident or easily on purpose.

But notice what it is not. It is not the protocol telling you anything. **The chain holds bytecode and has no opinion about source**, so verification happens entirely off to one side, performed by a party who chose to do it.

??? abstract "Why verification can fail for honest code"

    Two details that explain most confusion around this.

    **An exact match means exact.** Compiling the same source with a different
    compiler version, or different optimiser settings, produces different
    bytes — so verification needs the *settings*, not just the source. This is
    why a contract whose source is genuinely correct can fail to verify: the
    submitter mis-remembered which version they used. Failure to verify is
    evidence of a mismatch, not of dishonesty.

    **And the bytecode usually carries a pointer to its own description.** By
    default the Solidity compiler appends, to the end of the runtime bytecode,
    a small structure containing **the compiler version and a hash of a
    metadata file** describing the source [(Solidity documentation,
    v0.8.26)](#ref-solidity-metadata).

    Which is a neat twist on this whole page. The chain does not hold the
    source — but it very often holds a **fingerprint of a description of the
    source**, which is enough to tell you whether a file somebody hands you is
    the right one. The source still lives elsewhere; the chain just carries a
    receipt for it.

## Who is trusting whom

Worth being exact, because the arrangement is easy to misread in both directions.

**If you read the verified source on an explorer**, you are trusting that explorer to have done the comparison honestly and correctly. Not a wild trust — it is checkable, and a false claim would be caught by anyone who repeated the exercise — but it is trust, and it is not the protocol's guarantee.

**If you want no trust at all**, do what the explorer did: take the source, compile it with the stated settings, and compare the result against the bytecode you fetched from a node yourself. This is reproducible by anybody, which is what makes the whole arrangement work.

**And if you read nothing at all**, which is the usual case, you are trusting that somebody else has looked.

## Unverified is not the same as suspicious

A contract with no verified source **works exactly as well** as one with it. Verification is a convenience for humans and has no bearing on execution.

What you lose is help. The bytecode is still there, still public, still identical for everybody — you simply have to read machine code instead of Solidity. Plenty of perfectly ordinary contracts are unverified because nobody got round to it.

It *is* a reason for care, though, and the reason is narrow: the easiest way to check what a contract does has been removed, so the effort required to find out has gone up. Treat it as a cost, not as a confession.

## What bytecode can and cannot tell you

Tools exist that read bytecode and reconstruct something source-like — decompilers. They work, within limits worth understanding.

**What comes back is structure.** The control flow, the arithmetic, which storage slots are read and written, which other contracts are called. All of that is in the bytecode and can be recovered.

**What does not come back is meaning.** A decompiler can tell you that storage slot 3 is compared against the caller's address and the function stops if they differ. It cannot tell you that slot 3 is *the owner*, that the check is *an access control*, or that the author intended it to protect a withdrawal. Names are precisely the part that was thrown away.

So the honest statement, and the one that sharpens the previous page's section on immutability:

> You can always read what a contract **does**. You can never read what it was **for**.

The [smart contracts](smart-contracts.md) page said *code at an address is fixed* and *the code is public*, which together sound like total transparency. They aren't. Both are true, and the thing you most want to know — is this contract doing what its authors said it does — is not settled by either.

## The protocol has never heard of Solidity

Last and bluntly, because it is easy to assume otherwise.

Ethereum has no notion of Solidity, or of any programming language. It does not know a compiler exists. The rules describe bytes and what the machine does with them, and nothing in the specification mentions a language, a type, or a function name [(Wood, 2014)](#ref-wood-2014).

Every language that targets Ethereum is an arrangement among people outside the protocol — the same position as the [ABI](smart-contracts.md), the derivation path on [seed phrases](../wallets/seed-phrases.md), and the wordlist on that same page. Conventions sitting on top of something that knows nothing about them.

??? note "This is true of any published program, with one difference"

    Nothing above is special to Ethereum. Any compiled binary you download is
    machine code whose source you are trusting somebody about, and "reproducible
    builds" is a whole field devoted to exactly the comparison an explorer
    performs.

    The difference is not that Ethereum's code is readable. It is that
    **everybody is reading the same copy.** Nobody can serve you a different
    binary from the one other people run, because the bytes are at an address
    in a state that thousands of machines hold identically — and you can fetch
    them yourself and check their hash.

    Which is a smaller claim than "contracts are transparent" and a much more
    useful one.

---

## Recap

- Two things get called "the code": the **source** a person wrote, and the **bytecode** a compiler produced. Only the second has ever been on the chain.
- A contract's code on-chain is **bytecode**: one byte per instruction, with constants between them. No names, no comments, no types.
- **Every node holds every contract's code**, because code is part of the state. The account entry holds only a `codeHash`, which is a key into that node's own storage rather than a reference to anywhere else.
- A node checks it has the right code by **hashing it** and comparing. `codeHash` is covered by the state root, so **a contract's code is committed to as firmly as anybody's balance** — and identical contracts share one stored copy.
- **Source was never on the chain.** The compiler uses it and discards everything that made it readable, so the relationship is one-way: source gives bytecode, bytecode cannot give source.
- Bytecode *is* readable as instructions and tells you nothing about purpose. The opening bytes of nearly every Solidity contract are memory bookkeeping.
- **"Verified" means somebody produced source that compiles to exactly these bytes.** Strong evidence, performed off-chain by a party who chose to, and not a statement by the protocol.
- It needs the exact compiler version and settings, which is why **honest code sometimes fails to verify.**
- The bytecode usually ends with **the compiler version and a hash of a metadata file** describing the source — so the chain holds a receipt for the source even though it never held the source.
- Reading verified source means trusting the explorer's comparison; you can repeat it yourself, which is what makes it trustworthy.
- **Unverified is a cost, not a confession.** The contract works identically; you just have to read machine code.
- Decompilers recover **structure, never meaning**. So: you can always read what a contract **does**, and never what it was **for**.
- The protocol has **no notion of any language.** Solidity is a convention among people, like the ABI.

**Next:** [Events and logs](events-and-logs.md) — the one thing a contract can write and cannot read.

---

## References

<div class="sources" markdown>

- <a id="ref-solidity-metadata"></a>**Solidity documentation**, v0.8.26. *Contract metadata.* States that the compiler appends the IPFS hash of the canonical metadata file and the compiler version to the end of the runtime bytecode, encoded in CBOR with its length in the final two bytes. Version-pinned deliberately: the `latest` URL moves, and the default behaviour has changed between versions. <https://docs.soliditylang.org/en/v0.8.26/metadata.html>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Specifies code as a byte array and the machine's behaviour over it, with no reference to any source language — Appendix H lists the instruction set that gives each byte its meaning. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
