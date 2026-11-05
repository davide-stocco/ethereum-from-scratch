---
tier: 3
description: What running a node actually costs, in shape rather than specification — and why that cost is an argument about Ethereum rather than a note about your hardware.
---

# Running one yourself

**Expect this page to age.** It is about cost, and cost is the thing a growing [state](../accounts/state.md) changes. The argument is built to survive its own figures going stale, which is why there are almost none.

!!! info "Why this page gives shapes, not specifications"

    A page that prints "2 TB" is wrong within a year and confidently wrong,
    which is worse than vague. So this one describes the **shape** of the
    requirement — which resource binds first, what order of magnitude, and
    which way it moves — and sends you to a maintained source for today's
    numbers [(ethereum.org, 2026)](#ref-eth-org).

    If a figure here contradicts that source, trust the source.

!!! definition "Syncing"

    Getting a new node from nothing to **current**: holding the state as it is
    now, and able to check the next block against it.

    It is not downloading the chain. The state is the *result* of applying
    every transaction ever sent, so a node arriving late must either redo that
    work or obtain the state and verify it. **How much of the past you
    re-derive is the choice being made**, and it decides how long this takes.

## What it takes, in shape

Four requirements, and they are not equally binding.

**Disk is the one that rules machines out.** The other three requirements are rarely what stops somebody; this is. And the useful facts about it aren't the quantity — they're the kind and the direction. You need **terabytes rather than gigabytes**, on a solid-state drive rather than a spinning one, because the work is constant small random writes rather than bulk reading. And the requirement **only ever rises**, because nothing removes an account from the state.

**Memory and processor are ordinary.** A small desktop machine of recent vintage is enough. This is the reassuring part and the part people get wrong in both directions — you don't need a server, and a ten-year-old laptop won't do.

**Bandwidth is continuous rather than large.** A node is always talking: receiving blocks, forwarding them, answering peers. The monthly total is unremarkable; the requirement is that it never stops.

**And the real cost is that last word.** A node that runs for eight hours a day is a node that spends every morning catching up. The expense isn't the hardware, it's **a machine that stays on** — electricity, a corner of a room, and the fact that you now own something that breaks.

So the honest summary: **the cost of a node is not a purchase, it's a standing commitment.** A few hundred euros of disk is the easy part.

## Why catching up is the slow part

The chain is large, but downloading it is not what takes the time.

Having every block is not the same as having the state. To know what an account holds, you either apply every transaction that ever touched it — redoing a decade of arithmetic — or you obtain the current state from somebody and **verify it against the state root**, which is exactly the trick the [state](../accounts/state.md) page sets up. The second is far faster and gives up nothing, because a state you can check against the root is a state you don't have to trust.

So "how long does syncing take" has no single answer. It depends on how much of the past you choose to re-derive, which is the same decision as how much history you keep — described on the [previous page](what-a-node-is.md). **Hours if you verify a state you were handed; far longer if you insist on recomputing it; longest of all if you want every intermediate state ever.**

## What you get

Three things, and only the first is the point.

**You stop trusting anybody's answer.** Your balance is a number you computed, not a number you were told. Nobody can serve you a stale state, misreport a transaction, or quietly answer a different question from the one you asked.

**You stop revealing what you care about.** Querying somebody else's node tells them which addresses interest you and when. Running your own removes that audience — a privacy property most people don't realise they're giving away, and the one the [privacy](../accounts/what-it-reveals.md) page treats properly.

**You can't be rate-limited or cut off.** No API key, no terms of service, no provider deciding you've asked too often.

## What you don't get

**Any money.** This needs saying plainly, because it's the single most common expectation people arrive with.

Running a node pays **nothing**. There is no reward, no registration, nothing in the protocol that knows you exist. The paid role is being a **validator**, which is a node *plus* staking ether *plus* additional duties, and which the [node](what-a-node-is.md) page distinguishes and [proof of stake](../blocks/proof-of-stake.md) will describe. The hardware requirements for staking are higher, and the money comes from the stake and the duties — never from running the node underneath.

So if you are weighing this up as an investment, the answer is that it isn't one. It's an expense that buys you a property.

## Why the cost is an argument, not a footnote

Here is why this page exists at all, and it has nothing to do with your hardware.

Every page on this site has leaned on the same claim: **nobody has to trust anybody, because anyone can check.** The [node](what-a-node-is.md) page was blunt about what that rests on — not on people being honest, but on particular computers in particular rooms being able to redo the work.

**That claim has a price, and this page is it.**

While a node costs a few hundred euros and a spare corner, the claim is true: checking is available to anybody who wants it badly enough, and the people who most need certainty — exchanges, builders, the suspicious — can have it. **If the requirement reached the point of needing a datacentre, nothing in the rules would change, and the claim would quietly become false.** Verification would still be *possible*, in the way that auditing a central bank is possible. It would no longer be *available*.

That is why node counts get watched, and why "what does a node cost" is a question about Ethereum rather than about computers.

## What keeps it affordable?

**Nothing automatic**, and this is the uncomfortable part.

The state only grows, because nothing removes an account from it. So every operator's disk requirement rises for as long as the network runs.

And notice where the money sits. **Writing something into the state is paid for once**, by whoever writes it, at a price set by how congested the network is that day. **Keeping it is paid for indefinitely**, by every operator, including everyone who starts a node years later. Those are not the same people, and the second group was never asked.

That mismatch is a question about **pricing**, not about hardware — which is why no amount of cheaper disk resolves it. Cheaper hardware changes how fast the requirement bites. It does not change which way it moves.

It's also not this page's argument to make: it needs the account model, and so it's taken apart properly in [why accounts, and what they cost](../accounts/why-accounts.md), two parts ahead. What's worth carrying there from here is the concrete end of it — **the cost is real, it's denominated in disk, and it only goes one way.**

**EIP-4444** [(Kadianakis et al., 2021)](#ref-eip4444) addresses the other half: making old *history* somebody's deliberate job rather than everybody's default, so a node need not carry a decade of blocks it will never read.

## If you're not going to run one

Most readers won't, and that's a reasonable decision rather than a failure of duty. The useful thing isn't guilt — it's knowing **what is being assumed on your behalf.**

When your wallet shows a balance, somebody's node computed it and your wallet is repeating the answer. That somebody is almost certainly honest and almost certainly competent, and you have no way to know. The protocol's guarantee — *you need not trust anyone* — is a guarantee you have declined to exercise.

Which is fine, and worth being conscious of. It also means you have a stake in other people being able to run one cheaply, even if you never do. **The cost of a node is a question about your position whether or not you ever buy a disk.**

---

## Recap

- **Disk is the binding constraint**: terabytes not gigabytes, solid-state not spinning, and rising every block because nothing leaves the state.
- Memory and processor are **ordinary**. The real cost is a machine that **stays on**, not the hardware in it.
- **Syncing is slow because of arithmetic, not download.** How long depends on how much of the past you re-derive — and a state verified against the state root needs no trust, so there's no need to recompute it.
- What you get: **your own answers**, no audience for your queries, and nobody able to cut you off.
- What you don't get: **money.** Nodes earn nothing; the paid role is a validator, which is a node plus stake plus duties.
- The cost matters because **the site's central claim depends on it.** While a node is affordable, "anyone can check" is true. If it needed a datacentre, the rules wouldn't change and the claim would quietly stop being true.
- **Nothing keeps it affordable automatically.** Writing to the state is paid for once; keeping it is paid for indefinitely, by different people. That's a pricing mismatch rather than a hardware problem, and [why accounts](../accounts/why-accounts.md) takes it apart two parts ahead.
- If you don't run one, the useful thing is knowing **what you're assuming on somebody else's behalf** — and that you benefit from nodes staying cheap regardless.

**Next:** [Accounts](../accounts/accounts.md) — what all these machines are actually storing.

---

## References

<div class="sources" markdown>

- <a id="ref-eth-org"></a>**ethereum.org** (2026). *Run a node.* The maintained statement of current hardware requirements, including the distinction between a plain node and one used for staking. Checked November 2026; treat it rather than this page as authoritative on figures. <https://ethereum.org/en/run-a-node/>
- <a id="ref-eip4444"></a>**Kadianakis, G., lightclient, & Stokes, A.** (2021). *EIP-4444: Bound Historical Data in Execution Clients.* Ethereum Improvement Proposals. Proposes that clients stop serving and may prune block bodies and receipts past a cutoff, which bears directly on what a node operator must store. <https://eips.ethereum.org/EIPS/eip-4444>

</div>
