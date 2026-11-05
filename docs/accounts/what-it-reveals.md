---
tier: 1
description: Everything on Ethereum is public by default — which is what makes checking possible, and what it costs the people being checked.
---

# What it reveals

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**[Permanent](../about/forks.md).** That the state and every transaction are public is not a parameter anybody can change — it is the condition that makes independent verification possible. What people *do* about it changes constantly and belongs in classes, not products.

## The thesis this page exists to argue

**Verifiability and privacy are the same dial.** Every node can check every rule because every node can see everything. You cannot have the first property without paying the second, and no upgrade removes the trade — it only moves who sees what.

The previous pages have been assuming this without examining it. [Why accounts](why-accounts.md) lists privacy as one cost among several; here it gets the page it deserves.

## Questions this page should answer

- What exactly is public? (Every balance, every transaction, every contract's code and storage, forever, to anyone — and *addresses are not names*, which is the distinction everything else turns on.)
- So is Ethereum anonymous or not? (Neither. **Pseudonymous**: you have a persistent identifier that isn't your name, which is a much weaker property than it sounds and the source of most confusion.)
- How does a pseudonym become a name? (One link to the real world — an exchange deposit, a published address, a donation, an ENS name — and the whole history behind it resolves at once. Meiklejohn et al., already cited on [why accounts](why-accounts.md), did this to Bitcoin with public data alone.)
- Why can't this be fixed by just hiding the amounts? (Because somebody has to check the rules. A node that can't read a balance can't verify a transfer doesn't overdraw it — so hiding data means replacing verification with *proof*, which is a different and much harder design.)
- What does the transparency buy, concretely? (Anyone can audit the supply, prove a balance, spot a bug, or check whether a contract holds what it claims. None of that needs permission. That's a real and unusual property worth stating before the costs.)
- Who is actually harmed, and how? (Paying a salary in public. A business revealing its counterparties. Anyone whose address becomes known and whose entire financial history becomes readable — permanently and retroactively, which no other payments system does.)
- What are the mitigations, as classes? (Fresh addresses, which the account model fights; pooling; moving activity off the main chain; and proving statements without revealing their inputs. Name the classes and the trade each makes. **No products, no protocol names** — this is the fastest-moving material on the site.)
- And the retroactive problem: why is privacy here uniquely unfixable after the fact? (Published data cannot be unpublished. A privacy tool adopted tomorrow does nothing about the record already written, which is the sharpest difference from ordinary data protection.)

## Notes to self

- **Argue, don't describe** — this is the page type Davide responded to on [why accounts](why-accounts.md). One thesis, costs and benefits as the same property seen twice, and a frame from outside Ethereum.
- The outside frame here is strong and worth getting right: this is a **transparency-versus-confidentiality** trade of the kind regulated markets have argued about for a century. Disclosure rules exist because verification needs information, and privacy law exists because disclosure harms people. Ethereum resolved the trade at one extreme by construction rather than by policy, and lives with the consequences.
- **Refuse the lazy question.** "Is Ethereum private?" is badly formed. "What can be inferred about whom, by whom, and for how long?" is answerable.
- Do not write a how-to-stay-private guide. It would date instantly, and advice that goes stale on this subject gets people hurt.
- Resist naming specific tools or mixers. Beyond staleness, several carry legal context this site has no business summarising.
- The honest closing note: most readers' instinct is that this is a solvable engineering problem. It is partly that and mostly a **choice about who gets to check** — and the page should leave them able to see the trade rather than reassured.

**Next:** [What a smart contract is](../contracts/smart-contracts.md) — the second kind of account, and what it can see.
