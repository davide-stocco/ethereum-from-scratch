---
tier: 1
description: Everything on Ethereum is public by default — which is what makes independent checking possible, and what it costs the people being checked.
---

# What it reveals

**[Permanent](../about/forks.md).** That the state and every transaction are readable by anyone is not a parameter somebody chose and could unchoose. It is the condition that makes independent verification possible at all. What people *do* about it changes constantly, and this page describes those efforts as classes rather than products.

!!! definition "Pseudonymous"

    Identified by a persistent name that isn't your legal one.

    Ethereum is not anonymous and not identified — it is **pseudonymous**.
    Your [address](../crypto/addresses.md) is a stable label that follows you
    across everything you do, and it is not attached to your name **until it
    is**, at which point everything it ever did becomes attached too.

    That "until" is the whole subject of this page.

## The thesis

Every page so far has relied on something without examining it: **anyone can check.** Nodes recompute balances, verify signatures, and reject invalid blocks, which is why nobody has to be trusted.

Checking requires seeing. A node cannot verify that a transfer doesn't overdraw an account without reading the balance; it cannot confirm a signature without the message. So the property the whole site rests on has a precondition, and the precondition is that **everything is readable by everybody.**

> **Verifiability and privacy are the same dial.** You do not get the first without paying the second.

That isn't a flaw anyone introduced, and it isn't fixable by being more careful. It is the trade the design makes, and the useful thing is to understand which way it was set and what that costs.

## What's actually public

More than people expect, and permanently.

**Every balance**, for every address that has ever held anything.

**Every transaction** — sender, recipient, amount, the data it carried, what it cost, whether it succeeded. Including the ones that failed, which still happened and still appear.

**Every contract's code**, and **every value in its storage.** This is the one that surprises developers: marking a variable `private` in a contract's source controls which *other contracts* may read it through the language. It does nothing whatsoever about people. The storage slot is a 32-byte value in the [state](state.md), and anybody with a node can read it.

**And intentions, briefly, before they happen.** A transaction sits in the [mempool](../nodes/what-a-node-is.md) before inclusion, visible to anybody watching. So what you are *about to do* is public for a few seconds before it is done — which is the window most front-running lives in.

What's **not** public is the one thing that matters: your [private key](../crypto/private-keys.md), which never leaves your device. The protocol hides the thing that grants control and publishes everything else.

## Why pseudonymity is weaker than it sounds

"My address isn't my name" feels like adequate protection. It is much thinner than that, for a reason that has nothing to do with cryptography.

**A pseudonym accumulates.** Every transaction you make from an address joins a permanent, public, unforgeable record attached to that one label. Nobody can forge entries and nobody can remove them. Over time that record becomes a detailed account of behaviour — amounts, timing, counterparties, what you interacted with and when.

**And it collapses all at once.** The record isn't linked to you until **one** link exists: an exchange that knows your identity and your withdrawal address, a published donation address, a name registered to your address, a payment to someone who knows you. The moment any single link is made, it doesn't reveal one transaction. **It reveals the whole history, backwards.**

This is not hypothetical, and it has been demonstrated against a system that tries *harder* than Ethereum does. [Meiklejohn et al. (2013)](#ref-meiklejohn-2013) clustered Bitcoin activity into real-world identities using public data and a handful of heuristics — against users who were already generating a fresh address per payment, which is the practice the account model discourages.

Ethereum hands over by design what that research had to reconstruct.

??? abstract "Why the account model makes this worse, specifically"

    The [previous page](why-accounts.md) listed privacy as one cost of
    choosing accounts. Here is the mechanism.

    Bitcoin wallets generate a new address for each payment, so one user's
    activity is scattered across many unlinked labels, and linking them is
    the work those researchers had to do.

    Ethereum pushes the other way. An address is a **persistent place** —
    where your token balances live, where a name points, where a contract
    expects to find you, where a lending position is recorded. Reusing it
    isn't carelessness, it's what the model is for.

    So the same property that makes undercollateralised lending and
    reputation *conceivable* makes surveillance *straightforward*. **They are
    one fact seen from two sides**, which is why this page sits where it does
    rather than in a section of its own.

## Why you can't simply hide the amounts

The obvious fix is to encrypt the sensitive parts and leave the rest. It fails immediately, and the reason is worth following.

A node validating a transfer must establish that the sender's balance covers it. If the balance is hidden, the node cannot do that — so it would have to **take somebody's word**, which is precisely the thing the design exists to avoid. Hiding data from the verifier doesn't make the system private; it makes it trusted.

So confidentiality here can't be a matter of withholding information. The node still has to end up convinced. What it needs is a way to be convinced **without being shown** — and that is a real technique, usually called a **zero-knowledge proof**.

The everyday version: proving you are over eighteen without disclosing your date of birth. The bouncer needs certainty, not your birthday, and the two are separable. Or a bank's letter saying *this customer can cover £5,000* — the recipient learns what they need and not the balance. The difference with a zero-knowledge proof is that nobody has to trust the bank: the argument itself is checkable, and checking it reveals nothing beyond the fact it was valid.

Applied here, a transaction would carry a proof that *the sender's balance covered this amount and the arithmetic was done correctly*, which a node could verify without learning any balance at all. The verification still happens. What's removed is the node's need to see.

That is an active field rather than a finished one, and it's a different design from the one this site describes. The point for now is just this: **"hide the amounts" is not a small change.** It changes what checking means.

## What the transparency buys

Worth stating plainly before the costs, because it is easy to forget that this side exists.

**You can audit the whole thing yourself.** Total supply, who holds what, whether a contract actually has the reserves it claims — all checkable by anybody with a node, without asking permission and without anyone's cooperation. There is no equivalent for a bank, a payment network, or a company's internal ledger.

**You can prove a specific fact compactly.** "This address held this much at this block" is a short proof against the [state root](state.md), as the state page described. Verifiable without handing over the rest.

**And bugs are findable by outsiders.** A contract holding money with a flaw in it can be examined by anyone, which is why serious problems are often found by people with no relationship to the project.

That combination — **universal auditability with no gatekeeper** — is genuinely unusual, and it is what the privacy cost is buying.

## Who it costs, and how

The costs are specific, and they fall unevenly.

**Anyone paid on-chain.** A salary paid to an address publishes that salary — to colleagues, to counterparties, to anyone who learns the address. Most employment arrangements assume this information is private, and most legal systems treat it as such.

**Any business.** Counterparties, volumes, margins and timing are visible to competitors. Ordinary commercial confidentiality simply isn't available.

**Anyone whose address becomes known**, which is most people eventually. And the exposure is **retroactive**: it isn't "from now on, my transactions are public", it's "everything I have ever done is now public, including from before I had any reason to be careful".

That retroactivity is what makes this different from ordinary data protection, and it deserves its own statement:

> **Published data cannot be unpublished.** A privacy technique adopted tomorrow does nothing about the record already written.

Every other privacy regime assumes some ability to delete, restrict or expire. Here there is none, by construction — the data's permanence is the same property that makes the chain's history trustworthy.

## The mitigations, as classes

Four approaches exist. Naming them as classes rather than products is deliberate: specific tools on this subject date quickly, and some carry legal context this site is not the place to summarise.

**Use a fresh address per purpose.** Effective and cheap, and the account model fights it — you lose the accumulated balances, names and positions that made the address useful. Works for receiving, poorly for anything persistent.

**Pool with others**, so that which participant did what is no longer determinable from the chain alone. The classic approach, and the one whose legal treatment varies most by jurisdiction.

**Move the activity off the main chain**, so only summaries are published. Reduces what is visible without changing what the main chain does with what it does see.

**Prove rather than reveal.** Attach a zero-knowledge proof instead of the data, so a node can confirm the rules were followed without learning the amounts — the over-eighteen trick above, applied to balances. The most promising of the four and the least finished.

Each is a different point on the same dial, and **none of them moves the dial for the record you have already written.**

## So is Ethereum private?

The question is badly formed, and that's worth saying rather than answering it.

"Private" suggests a property the system either has or lacks. What actually exists is a set of specific answerable questions: **what can be inferred, about whom, by whom, and for how long?** On Ethereum the answers are roughly *everything financial*, *about anybody whose address is known*, *by anyone at all*, *for ever*.

Which is a defensible arrangement and an extreme one. Economic treatments of privacy describe disclosure as a **trade rather than a good**: it creates value by letting people verify and enforce things, and destroys value by exposing people to anyone who would use the information against them [(Acquisti et al., 2016)](#ref-acquisti-2016).

So there is no amount of disclosure that is simply correct. **It depends who ends up holding the information, and what they want it for** — your salary disclosed to a tax authority and your salary disclosed to a burglar are the same fact with opposite consequences. Which is why the question is never "how private is this?" but "visible to whom, and what can they do with it?". Regulated markets spend enormous effort *tuning* that trade: what must be disclosed, to whom, in what detail, and — crucially — **after what delay.**

Ethereum has no tuning. There is no "disclose to regulators only", no "publish after ninety days", no "aggregate figures but not individual positions". The dial is welded at one end, and the weld is what makes the verification work.

So the honest summary is not that Ethereum is private, or that it isn't. It's that **Ethereum made a policy choice structurally**, where everyone else makes it adjustably — and bought something real with it.

---

## Recap

- **Verifiability and privacy are the same dial.** Nodes can check everything because they can see everything; the site's central claim has transparency as its precondition.
- Public: every balance, every transaction including failed ones, every contract's code and **every value in its storage** — `private` in source code restrains other contracts, not people. Plus your intentions briefly, while a transaction waits in the mempool.
- Not public: your **private key**. The protocol hides what grants control and publishes the rest.
- Ethereum is **pseudonymous**, which is weaker than it sounds: a pseudonym **accumulates** a permanent record, and **one** link to the real world reveals that record **backwards**.
- Clustering chain activity into identities has been demonstrated against users who *were* rotating addresses [(Meiklejohn et al., 2013)](#ref-meiklejohn-2013). Ethereum discourages rotating them.
- **"Just hide the amounts" isn't a small change.** A verifier that can't read a balance must trust someone. Confidentiality therefore needs a **zero-knowledge proof** — convincing the node without showing it, the way you can prove you're over eighteen without giving your birthday. The checking still happens; the seeing doesn't.
- What it buys: **universal auditability with no gatekeeper**, compact proofs of specific facts, and bugs findable by outsiders.
- What it costs falls on anyone paid on-chain, any business, and anyone whose address becomes known — **retroactively**, which no other privacy regime assumes.
- **Published data cannot be unpublished.** No mitigation helps the record already written.
- "Is Ethereum private?" is the wrong question. **What can be inferred, about whom, by whom, for how long** — and the answers are *everything financial, anybody known, anyone at all, for ever.*

**Next:** [What a smart contract is](../contracts/smart-contracts.md) — the second kind of account, and what its code can and cannot see.

---

## References

<div class="sources" markdown>

- <a id="ref-acquisti-2016"></a>**Acquisti, A., Taylor, C., & Wagman, L.** (2016). *The economics of privacy.* *Journal of Economic Literature*, 54(2), 442–492. Surveys privacy as a trade rather than a good — disclosure enabling verification and enforcement while exposing the disclosed — which is the frame this page applies to a system that resolved the trade structurally. <https://doi.org/10.1257/jel.54.2.442>
- <a id="ref-meiklejohn-2013"></a>**Meiklejohn, S., Pomarole, M., Jordan, G., Levchenko, K., McCoy, D., Voelker, G. M., & Savage, S.** (2013). *A fistful of bitcoins: Characterizing payments among men with no names.* *Proceedings of the 2013 Internet Measurement Conference*, 127–140. Clusters public chain activity into real-world identities using heuristics alone, against users who were already generating a fresh address per payment. <https://doi.org/10.1145/2504730.2504747>

</div>
