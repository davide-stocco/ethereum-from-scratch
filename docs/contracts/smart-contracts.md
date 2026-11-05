---
tier: 1
description: A smart contract is a program stored at an account — and the interesting thing about it is everything it has been forbidden to do.
---

# What a smart contract is

**[Permanent](../about/forks.md).** What a contract *is* follows from [accounts](../accounts/accounts.md) and hasn't changed since 2015. What it costs to run, and which operations exist, are fork-dependent and belong to later pages.

!!! definition "Smart contract"

    A **program stored at an account**, under the `codeHash` field the
    [accounts](../accounts/accounts.md) page described.

    It runs only when something calls it, it runs identically on every
    [node](../nodes/what-a-node-is.md), and it can reach nothing outside
    Ethereum. Those three constraints are not limitations of the current
    implementation — they are what make it work at all.

## Neither smart nor a contract

The name is the first obstacle, and worth clearing before anything else, because most people meet the term years before the mechanism.

**It isn't smart.** There is no judgement in it, no interpretation, no capacity to notice that something has gone wrong. It does exactly what its code says, including when the code says something its author didn't mean. A contract cannot be reasoned with, cannot be asked what it intended, and has no way to behave sensibly in a situation nobody wrote down.

**It isn't a contract.** There are no parties, no offer and acceptance, no consideration, no court, no remedy. The word imports a set of expectations from law that are all false here: that intent matters, that ambiguity gets resolved reasonably, that breach has consequences someone will impose. None of that exists. There is a program, and it runs.

The term is older than Ethereum by about two decades. Szabo [(1997)](#ref-szabo-1997) used it for embedding contractual terms into hardware and software so that breaking them becomes impractical rather than merely actionable — a vending machine being the primitive ancestor, enforcing *payment, then goods* with no lawyer involved. Ethereum's contracts are related to that idea and narrower than it. They don't enforce agreements. They execute.

Keep the word, since everybody uses it. Just don't let it do any reasoning for you.

## What it actually is

Go back to the four fields. A contract account has the same ones as any other: nonce, balance, `storageRoot`, `codeHash`. What makes it a contract is simply that **`codeHash` isn't the empty constant** — there is code, so the account is controlled by that code rather than by any key.

A contract is therefore not a special kind of object. It's **an account with a program attached**, which is why it can hold ether, receive transactions, and be looked up exactly like a wallet account. That was the point of choosing accounts in the first place — [Buterin (2014)](#ref-buterin-2014) presents contracts as what the model is *for*, rather than as something built on top of it.

Two consequences people find surprising, both established earlier:

**Nobody holds its keys**, because there are none. Control is the code, and the code is public.

**It cannot act on its own.** The [accounts](../accounts/accounts.md) page argued this at length: no timers, no scheduled jobs, no thread of its own. A contract is inert between calls, and everything that looks automatic is somebody being paid to send a transaction.

## How it gets there

A contract is created by a transaction carrying code instead of a recipient — a deployment. Once that transaction is included, the code is written to an account and stays there.

**The address is computed, not chosen.** It comes from the creating account's address and that account's [nonce](../accounts/nonce.md), hashed together [(Wood, 2014)](#ref-wood-2014) — which is why a contract's nonce counts deployments rather than transactions, and why two deployments from one account can never collide.

A useful consequence: **you can know the address before the contract exists.** Deployment is predictable, so ether can be sent to, or code written referring to, an address that will only be occupied later. That underpins several arrangements you'll meet, and it's possible only because address derivation is arithmetic rather than allocation.

## How it runs

When a transaction calls a contract, **every node runs the code** — independently, against its own copy of the state, arriving at the same answer. That's the [determinism](../foundations/what-is-ethereum.md) the site opened with, finally doing real work: thousands of machines can agree on what a program computed because the program cannot do anything that might come out differently anywhere.

Which brings us to the part worth the page.

## What it cannot do, and why that's the point

A contract is a program with almost everything taken away. The list of absences is short and total:

| It cannot | Because |
| --- | --- |
| read a clock | two nodes would read different times |
| make a network request | the response could differ, or not arrive |
| generate a random number | the result would differ per node |
| read a file, or anything else on the machine | nothing outside the state is shared |
| start itself | nothing schedules it, and nobody would pay |

**Every one of those absences is the price of reproducibility.** A program able to fetch a web page would get different answers on different machines, and the network would stop agreeing about what happened. So each capability is missing not because nobody implemented it, but because having it would destroy the one property that makes the whole arrangement work.

That inversion is what to take from this page. **A contract is interesting because of what it is forbidden to do.** The absences are the design.

??? abstract "Two of those need qualifying, because the honest version is sharper"

    **"No clock" isn't quite right.** A contract *can* read a timestamp — but
    it's a number the block's proposer wrote down, not a reading from a clock.
    It is approximately the real time, because other nodes reject a block
    whose timestamp is implausible, and it is not trustworthy to the second,
    because the proposer chooses it. So contracts have an *approximate,
    partly adversarial* notion of time, which is a more awkward thing than
    none at all.

    **"No randomness" needs the same care.** There are values on the chain
    that look random and a contract can read them. The difficulty is
    structural: anything a contract can read, the party assembling the block
    can read first — and can often choose whether to include the transaction
    at all. So a contract's "random" number is knowable in advance by exactly
    the person with the most incentive to exploit it.

    Both have one shape. The constraint isn't that information is
    unavailable; it's that **anything available to the contract is available
    to whoever orders the transactions.** That's a recurring trap rather than
    a solved problem.

So how does a contract learn anything about the world — a price, a result, a temperature? **Somebody sends it in.** A party puts the data on-chain in an ordinary transaction, and the contract reads it from the state like anything else. Those parties are **[oracles](../glossary.md#oracle)**, and the arrangement deserves clear eyes: the contract isn't observing the world, it's trusting whoever reported it. Any claim that a contract is "trustless" stops at that boundary.

## Can a contract be changed?

**The code at an address cannot change.** That much is true, and it's the basis of everything said about immutability.

The trouble is it doesn't mean what it's usually taken to mean, because **behaviour isn't determined by one contract's code.** The common pattern: the contract you interact with holds an *address* in its storage and forwards calls to the code found there. Storage is writable. So changing one stored value changes what the whole thing does, without altering a byte of the code you were told was immutable.

That isn't a loophole or an abuse — it's a widely used, openly documented technique. But it makes "immutable" a claim to check rather than accept:

- **Is the code at this address fixed?** Almost always yes.
- **Can its behaviour change?** Only by reading it to find out.

A good instance of a pattern this site keeps hitting: a true statement about the protocol — *code at an address is fixed* — and a false impression it creates, that the thing therefore can't change.

## How a call says which function to run

A short section, because the mechanism is a convention rather than a rule and people assume the reverse.

The protocol has no concept of a function. A call arrives as **bytes**, and the contract's own code decides what to make of them. What makes `transfer(address,uint256)` mean anything is an agreement everybody follows: the first **four bytes** of a call are the leading four bytes of the Keccak-256 hash of the function's signature [(Solidity documentation, v0.8.26)](#ref-solidity-abi), with the arguments in a defined layout after it.

Two things worth noticing. **[Keccak-256](../crypto/keccak256.md) is doing this job too** — the same function behind addresses and the state root also decides what a function is called. And because four bytes is short, two different signatures can in principle produce the same selector: rare, and a real source of trouble when it happens.

The whole arrangement is the **ABI**, and nothing in the protocol enforces it. It's a shared convention, like the derivation path on the [seed phrases](../wallets/seed-phrases.md) page — universally followed, nowhere required.

## How many times has a contract been used?

A question with an instructive answer: **nothing records it.**

A contract account has only the four fields, and its nonce counts contracts it *created*, not calls it received. There is no counter anywhere. So this is a question about **history**, not state — and a node that pruned its history cannot answer it, however perfectly it validates the present.

Reconstructing it from the chain gives three different numbers, depending on what you count:

- **Transactions sent to the address.** Undercounts, often badly — it misses every call arriving from another contract, since those aren't transactions.
- **Events it emitted.** The practical method, and cheap at scale. Misses any execution that emitted nothing, which is the author's choice.
- **Re-executing everything with tracing.** Complete, expensive, and needs a node that kept the history.

The warning for anyone using chain data: **published usage figures aren't comparable unless you know which was counted**, and sources rarely say. Same family as *addresses are not people*, which [the previous page](../accounts/what-it-reveals.md) argued, and *a failed transaction still happened and still cost gas.*

---

## Recap

- A smart contract is **a program stored at an account**, identified by its `codeHash` not being the empty constant. Not a special object — an account with code.
- It is **neither smart nor a contract**: no judgement, no parties, no remedy. The word predates Ethereum by two decades and meant something broader [(Szabo, 1997)](#ref-szabo-1997).
- **Nobody holds its keys**, because there are none. Control is the code, and the code is public.
- Its **address is computed** from the creator's address and nonce, so it is predictable before the contract exists.
- **Every node runs the code and gets the same answer** — possible only because of what the code is forbidden to do.
- It cannot read a clock, reach the network, generate randomness, or start itself. **Each absence is the price of reproducibility**, not a missing feature.
- The sharper version: anything available to a contract is **also available to whoever orders the transactions** — which is why on-chain randomness and timestamps are traps rather than tools.
- Outside data arrives only because **somebody sends it in** — an oracle. The contract isn't observing the world; it's trusting a reporter.
- **Code at an address can't change; behaviour can.** The usual pattern forwards calls to an address held in storage, and storage is writable. "Immutable" is a claim to check, not accept.
- Functions are a **convention**: four bytes of a Keccak-256 hash of the signature, by agreement. The protocol knows nothing about functions.
- **Nothing counts how often a contract is used.** It's a history question, answerable three ways that disagree.

**Next:** [RLP encoding](../encoding/rlp.md) — how all of this gets written down as bytes.

---

## References

<div class="sources" markdown>

- <a id="ref-buterin-2014"></a>**Buterin, V.** (2014). *Ethereum white paper: A next-generation smart contract and decentralized application platform.* Sets out contracts as the purpose of the account model rather than an addition to it, and the deliberate narrowness of what they may do. <https://ethereum.org/en/whitepaper/>
- <a id="ref-solidity-abi"></a>**Solidity documentation**, v0.8.26. *Contract ABI specification.* States that the first four bytes of a call are the leading four bytes of the Keccak-256 hash of the function signature. Version-pinned deliberately: the `latest` URL moves. <https://docs.soliditylang.org/en/v0.8.26/abi-spec.html>
- <a id="ref-szabo-1997"></a>**Szabo, N.** (1997). *Formalizing and securing relationships on public networks.* *First Monday*, 2(9). The origin of the term, used for embedding contractual terms into hardware and software so that breach becomes impractical — a broader and different idea from a program at an address. <https://doi.org/10.5210/fm.v2i9.548>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Defines code as an account field, the deployment of code by transaction, and the derivation of a contract's address from its creator and that creator's nonce. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
