---
tier: 2
description: A node runs two cooperating programs, and several independent implementations of each exist on purpose — because one implementation means one bug can take the network with it.
---

# Clients and the two layers

!!! info "Current as of Fusaka (December 2025)"

    The two-program split and the argument for many implementations are
    durable. **Which implementations exist, who maintains them and what share
    each has are not** — teams start and stop, and shares move. This page
    names roles and reasons rather than products, and any figure that does
    appear carries its date.

**Mostly [permanent](../about/forks.md).** That a node runs two cooperating programs, and why having several independent implementations of each matters, are structural. Which programs exist is not.

!!! definition "Client"

    A program that implements Ethereum's rules. **Not** an app, not a wallet —
    the software that *is* a [node](what-a-node-is.md), or half of one.

    Several independent clients exist for each half of the job. They are
    written by different teams in different programming languages, and they
    must agree exactly, because a disagreement about the rules is a
    disagreement about what happened.

## One node, two programs

A node is not a single piece of software. It is **two programs running side by side**, each doing a job the other can't, talking over a defined interface.

<svg viewBox="0 0 470 236" role="img" aria-label="One node drawn as a dashed box containing two programs side by side: an execution client holding the accounts and running the code, and a consensus client deciding the order of transactions. An arrow runs between them, and the consensus client also connects outward to other nodes." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="8" y="30" width="454" height="134" rx="8" stroke-dasharray="5 4" opacity="0.5"/><rect x="26" y="56" width="186" height="90" rx="5"/><rect x="258" y="56" width="186" height="90" rx="5"/><path d="M212 90 L258 90"/><path d="M212 112 L258 112"/><path d="M351 164 L351 196"/></g><g fill="currentColor" stroke="none"><path d="M254 85 L264 90 L254 95 Z"/><path d="M216 107 L206 112 L216 117 Z"/><path d="M346 196 L351 206 L356 196 Z"/><text x="20" y="22" font-size="10" opacity="0.75">ONE NODE &#183; one machine</text><text x="38" y="78" font-size="11" font-weight="700">execution client</text><text x="38" y="98" font-size="10" opacity="0.85">holds the accounts</text><text x="38" y="114" font-size="10" opacity="0.85">runs the code</text><text x="38" y="130" font-size="10" opacity="0.85">keeps the state</text><text x="270" y="78" font-size="11" font-weight="700">consensus client</text><text x="270" y="98" font-size="10" opacity="0.85">decides the order</text><text x="270" y="114" font-size="10" opacity="0.85">of transactions</text><text x="270" y="130" font-size="10" opacity="0.85">votes on blocks</text><text x="351" y="222" font-size="10" text-anchor="middle" opacity="0.8">other nodes&#8217; consensus clients</text><text x="8" y="186" font-size="9" opacity="0.7">Neither half is a node on its own.</text></g></svg>

**The execution client** is the [state machine](../foundations/what-is-ethereum.md) this site has been describing. It holds the accounts, runs contract code, keeps the [state](../accounts/state.md), and checks that transactions follow the rules.

**The consensus client** decides *which* block comes next and in what order — the problem that [has to be solved by somebody](../blocks/why-somebody-chosen.md) because the rules don't settle it. It talks to other nodes' consensus clients, and tells its own execution client which block to apply.

Neither is a node by itself. The execution client can check whether a block is valid but has no opinion about which block is the real one. The consensus client can tell you which block the network has agreed on but cannot check whether its contents make sense. **A node is the pair.**

??? info "History: they were separate systems first"

    The division looks like an architectural decision. It's a historical
    accident that turned out well.

    Until 2022, Ethereum did both jobs in one program: one piece of software
    held the accounts and also ordered the transactions, by mining. Meanwhile a
    second, entirely separate network — the **Beacon Chain** — had been running
    since December 2020, doing nothing but practising consensus. It held no
    accounts and processed no transactions. For about twenty-one months it ran
    alongside the real thing, agreeing on the order of nothing in particular.

    In September 2022 the two were connected: the old system stopped ordering
    transactions and started taking its order from the Beacon Chain instead.
    **EIP-3675** [(Kalinin et al., 2021)](#ref-eip3675) is the specification
    for that change, and the event is called **the Merge**.

    Which is why the split exists at all. Nobody set out to build a node from
    two programs; two systems were built separately and then joined, and the
    seam is still visible in every node today.

## Why several of each, rather than one official one?

Here is the part worth understanding, because the obvious intuition is backwards.

It would seem simpler — and safer — to have **one** correct implementation that everybody runs. One codebase to audit, one team to fund, no risk of two programs disagreeing about the rules.

That arrangement has a fatal property: **a bug in it is a bug in Ethereum.**

If every node runs the same software and that software accepts a block it shouldn't, every node accepts it. There is no one left to notice. The rules of Ethereum would no longer be the specification — they would be whatever that program happened to do, bugs included, and nobody could tell the difference.

Several independent implementations change the shape of that failure. A bug in one is **a disagreement rather than a catastrophe**: the affected nodes reject blocks the others accept, the discrepancy is visible immediately, and the remaining network carries on. The bug becomes a problem for that client's users instead of a rewriting of the rules.

So **diversity here is a safety property, not an absence of standardisation.** The duplicated effort is the point, in the same way a second opinion is not an inefficiency.

### How real is that risk?

Not hypothetical, and not rare enough to be reassuring.

Researchers at Seoul National University and Georgia Tech built a tool that feeds the same transactions to different clients and watches for disagreement — differential fuzzing. It found **two previously unknown consensus bugs** in a single widely used client, and **one of them later caused a split on the live network** [(Yang et al., 2021)](#ref-yang-2021).

That one sentence contains the whole argument. The bugs existed. They were found by comparing implementations against each other, which is only possible if more than one exists. And one of them went on to do real damage anyway.

## The sharp edge: when one client has most of the network

Diversity is only protective if it exists in practice, and it hasn't always.

On **11 November 2020**, a consensus bug in the client then running most of the network caused exactly the failure described above. A fix had been released earlier but not flagged as urgent, so many operators hadn't applied it. A single transaction triggered the bug, and nodes on the old version split away from the rest — following a different chain, reporting different balances, and in some cases serving wrong answers to the applications built on them [(De, 2020)](#ref-de-2020).

Two things about that incident are worth separating, because they're usually run together.

**It was a version split, not a client-diversity failure** in the strict sense — old and new releases of the *same* client disagreed. But the reason it mattered so much is dominance: because one implementation held most of the network, a mistake in its release process became most of the network's problem.

**And this is why client share is counted and published.** It isn't a popularity contest. Under [proof of stake](../blocks/proof-of-stake.md) the thresholds become sharper still — a client with a large enough share of validators can stall the network's ability to settle anything, or in the worst case carry an invalid chain to settlement. The exact fractions are parameters and belong on that page; the structural point is that **share is a safety variable, and a client being popular is a risk rather than an endorsement.**

## Who writes them, and who pays?

A fair question once "nobody is in charge" is taken seriously, and the answer is less tidy than people expect.

Each client is built and maintained by its **own team**, independently, in different languages, funded variously — foundation grants, company sponsorship, public goods funding, and in some cases unpaid work. No team can compel the others to do anything. The specification is the shared reference, and agreeing with it is voluntary in the sense that nothing but consequence enforces it.

Which produces a situation worth stating plainly: **the rules of Ethereum are maintained by several small groups of people who are not obliged to continue.** Who decides what those rules become is a different question again, and gets [its own page](../economics/governance.md).

## Do you ever choose a client?

**Running a node: yes, and it's the one decision an individual operator makes that affects everybody else.** You pick one implementation of each half. Choosing a less common one slightly increases your own risk — fewer users means bugs are found later — while reducing the network's. That tension is real and worth naming rather than smoothing over.

**Using Ethereum through a wallet: no.** You're relying on somebody else's node, running somebody else's client, chosen by them. The [previous page](what-a-node-is.md) made this point about nodes; it applies one level down as well. Most people have never chosen a client and never will, which is precisely why the share figures matter to people who aren't running anything.

---

## Recap

- A node is **two programs**: an **execution client** holding the accounts, state and code, and a **consensus client** deciding the order and voting on blocks. Neither is a node alone.
- The split is **historical, not architectural**. The consensus system ran as a separate chain from December 2020 and was joined to the execution system in September 2022 — the Merge.
- A **client** is an implementation of the rules. Several independent ones exist for each half, written by different teams in different languages.
- **One official implementation would be more dangerous, not safer.** If everyone runs the same software, a bug in it isn't a bug — it silently becomes the rules.
- With several, a bug is **a disagreement rather than a rewriting**: visible immediately, survivable by the rest of the network. The duplicated effort is the point.
- The risk is documented: differential fuzzing across clients found **two unknown consensus bugs in one client, and one later split the live chain.**
- **Dominance is the danger.** In November 2020 a bug in the most-used client split the network, which is why client share is treated as a safety variable rather than a popularity measure.
- Clients are maintained by **independent, variously funded teams** that nothing obliges to continue.
- Running a node means choosing clients; **using a wallet means somebody chose for you.**

**Next:** [Running one yourself](running-one.md) — what it actually takes, and why that number is an argument rather than a footnote.

---

## References

<div class="sources" markdown>

- <a id="ref-de-2020"></a>**De, N.** (2020, 11 November). *Ethereum's "unannounced hard fork" was trying to prevent the very disruption it caused.* CoinDesk. Contemporaneous account of the chain split caused by a consensus bug in the then-dominant client, and of the patch-communication failure behind it. <https://www.coindesk.com/tech/2020/11/11/ethereums-unannounced-hard-fork-was-trying-to-prevent-the-very-disruption-it-caused>
- <a id="ref-eip3675"></a>**Kalinin, M., Ryan, D., & Buterin, V.** (2021). *EIP-3675: Upgrade consensus to Proof-of-Stake.* Ethereum Improvement Proposals. The specification for connecting the two layers, and the reason a node now runs two programs. <https://eips.ethereum.org/EIPS/eip-3675>
- <a id="ref-yang-2021"></a>**Yang, Y., Kim, T., & Chun, B.-G.** (2021). *Finding consensus bugs in Ethereum via multi-transaction differential fuzzing.* *15th USENIX Symposium on Operating Systems Design and Implementation (OSDI '21)*. Feeds identical transactions to different clients and reports the disagreements; found two previously unknown consensus bugs in one client, one of which subsequently caused a mainnet fork. <https://www.usenix.org/conference/osdi21/presentation/yang>

</div>
