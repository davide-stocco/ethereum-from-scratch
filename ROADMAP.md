# Roadmap

Two organising principles:

1. **Ordering** — no page explains something that depends on a page further down.
2. **Fork stability** — publish the permanent core first. See [FORKS.md](FORKS.md) for the full classification.

---

# Two orderings, kept separate

The single most important structural decision on this site: **tiers are a
maintenance concern, not a reading concern.**

| | Ordered by | Lives in |
| --- | --- | --- |
| **Reading order** | topic — problem before mechanism | `nav` in `mkdocs.yml` |
| **Publishing order** | tier — fork-proof first | this file |

These are different orderings, and that is fine. A reader should never be able
to tell which tier a page is in; they should see a sensible path through
Ethereum. Meanwhile you need to know exactly which pages a hard fork can
invalidate. Conflating the two would mean readers browsing your maintenance
schedule.

So the tier never appears in the navigation. It's recorded three ways instead:

- **`tier:` in each page's frontmatter** — `1`, `2`, `3`, or `meta`. Invisible
  to readers, and it makes the post-fork review mechanical:
  `grep -rl "^tier: 3" docs/` lists everything to re-check.
- **A visible date stamp**, on Tier 2 and 3 pages only — "current as of
  <upgrade>" — so readers can judge whether a page has gone stale.
- **This file**, which holds the publishing order and what's written.

## Consequence: sections appear before they're full

Because the problem is Tier 1 and the mechanism is Tier 3, a section often
publishes its first page long before the rest. *Consensus* will exist in the
menu holding only "why transaction order has to be agreed", with Proof of Stake
still unwritten.

That's correct, not a defect — it tells a reader the topic is coming and where
it sits. Each such page ends with a forward pointer saying the mechanism isn't
published yet, and linking the [fork policy](docs/about/forks.md) for why.

## Target structure

Reading order once everything exists. `←` marks a fork-proof *problem* page
sitting directly above the fork-dependent mechanism that answers it.

```
Home

Foundations         What is Ethereum? · Ether, wei and gwei · Hex and bytes
Cryptography        Keccak-256 · Private keys · Public keys · Addresses
                    Signatures
Wallets             Wallets and seed phrases · What losing your keys means
Encoding            RLP · Merkle Patricia Trie [2]
Accounts and state  Accounts · The nonce · State [2]
Transactions        Why metering is necessary ← · Transactions [2]
                    Gas [2] · Fees [3]
Blocks              Blocks [2] · The block header [3] · The chain, reorgs [3]
The EVM             The EVM [2] · Opcodes [3] · Stack, memory and storage
                    Bytecode and deployment [2] · The ABI · Events and logs
Consensus           Why order must be agreed ← · Proof of Stake [3]
                    Validators · Finality · Withdrawals [3]
Scaling             Why throughput is limited ← · Rollups [3] · Blobs [3]
Standards           ERC-20 · ERC-721 · ENS [3] · Account abstraction [3]

Economics           (landing page)
  Why it costs      Security budget ← · Who pays ← · Fixed cap or flexible ←
  Pricing           Congestion pricing [2] · The fee burn [3] · MEV [3]
                    Capacity as supply [3]
  Money             Stablecoins: what holds a peg · Runs and reserve quality
                    Private money in historical perspective
  Institutions      Transaction cost economics · State growth as externality
                    Public goods funding [2]

Applications        What needs this machine? · Insurance · Exchanges and AMMs
                    Lending · NFTs · DAOs
Governance          Who changes the protocol · The EIP process [3]
Security & privacy  How things go wrong · Reentrancy · Oracle manipulation
                    The economics of audits · Everything is public

Fork-dependent      Gas costs [2] · Fork history [3]
Glossary
About               Ethereum changes · Who's writing this
Tools               Keccak hasher · key → address · converters · decoders
```

## What adding the missing topics changes

Five structural consequences, all of them real changes rather than extra rows.

**1. It's four strands now, not one spine.** Protocol mechanics, economics,
applications, practicalities. At roughly sixty pages, linear reading stops being
plausible for most visitors — so the **reading paths on the homepage are
promoted from a nicety to the primary navigation aid**, and need maintaining as
a first-class feature.

**2. Economics needs internal structure and a landing page.** Fourteen-odd
pages across four distinct questions — why it costs anything, how block space is
priced, private money, and institutions. Past roughly a dozen pages a flat
section stops being navigable, and arriving directly into the middle of an
argument needs a front door.

**3. Applications sits *after* Economics, not before.** Tempting to put it early
because it's the most approachable material, but judging whether an application
needs this machine requires the economic frame first — otherwise the honest
answer ("mostly nothing") reads as cynicism rather than conclusion.

**4. "Limits" dissolves.** It was holding the oracle problem and throughput
together, but once Applications exists the oracle problem belongs there — it's
the constraint that decides what can be built — and throughput belongs at the
head of Scaling. Grouping them was a symptom of having nowhere better.

**5. Wallets moves early.** It was filed under practicalities, late.
Wrong: "what happens if I lose my keys" is among the first questions anyone
asks, and it needs only the Cryptography section. Immediately after it is the
right home.

## A fourth kind of staleness: ecosystem

Pages now go stale in four distinct ways, and conflating them is how a reference
site rots:

| Kind | Example | Marker |
| --- | --- | --- |
| **Fork** | gas costs, opcodes | `tier:` plus a visible upgrade stamp |
| **Data** | "the burn exceeds issuance" | period and source, never a bare value |
| **Ecosystem** | which stablecoins exist, which protocols are used | describe mechanism classes, never products |
| **Never** | keccak, RLP, addresses, the security budget | nothing needed |

The **ecosystem** category is new, and it governs the whole Applications section
plus the money pages in Economics. The rule that follows is the same one already
written for the oracle page, generalised:

> **Name the mechanism class, not the product.** "Over-collateralised lending"
> outlives any particular lender. "Fully-reserved versus algorithmic
> stablecoins" outlives any particular issuer. Products are the one thing on
> this site guaranteed to be wrong within a year.

Where a specific case genuinely teaches something — Terra/UST as reflexive
collapse — write it as **history**, in a `??? info "History: …"` box, with dates.
Past tense ages gracefully; present tense doesn't.

---

# Versions

~79 pages at full scope, which is a multi-year project. So the goal is a site
that's **useful at every stage**, not only at the end.

| | Contents | Pages | Why it stands alone |
| --- | --- | --- | --- |
| **v1 — launch** | Foundations, Cryptography, Wallets, Encoding, Accounts and state, Economics "why it costs", Glossary, About | ~20 | *"The permanent core, and why it costs anything."* Almost all Tier 1 — nothing can go stale. Contains the differentiator. |
| **v2** | Transactions, Blocks, Fork-dependent details, first Tools | ~32 | The working machine. Where most readers' questions actually live. |
| **v3** | The EVM, Consensus, Scaling, Standards | ~50 | Technically complete. |
| **v4** | Applications, Governance, Security and privacy, rest of Economics | ~79 | The judgement layer — needs everything before it. |

**Launch at v1**, and don't wait for v2. Twenty permanent pages is a complete,
defensible site; waiting for v3 means two years of nothing public.

**v1 and v2 are scaffolded in `nav` now.** v3 and v4 stay out of the site until
v1 is published — a sidebar listing seventy unwritten pages is worse than no
sidebar.

**At launch, trim `nav` to written pages only.** The stubs are there for the
author's benefit; publishing them gets near-empty pages indexed as thin content
and drags down the good ones.

---

# Phase 1 — the fork-proof core *(published)*

Everything here has been true since 2015 and cannot realistically change. Write these once; they never need revisiting.

## Foundations

| Page | Status |
| --- | --- |
| What is Ethereum? | ✅ written |
| Ether, wei and gwei | stub |
| Hex and bytes | stub |

## Cryptography

| Page | Status |
| --- | --- |
| Keccak-256 | stub |
| Private keys | stub |
| Public keys | stub |
| Addresses | stub |

## Encoding

| Page | Status |
| --- | --- |
| RLP encoding | stub |

## Accounts

| Page | Status |
| --- | --- |
| Accounts | stub — carries one EIP-7702 caveat |
| The nonce | stub |

## About

| Page | Status |
| --- | --- |
| Ethereum changes (fork policy) | ✅ written |

**Still to add to Phase 1** once the above are done — all fork-proof, but each needs groundwork that isn't published yet:

- Signatures (ECDSA signing and recovery) — secp256k1, unchanged since genesis
- The ABI — a convention, not a consensus rule
- Events and logs — mechanism unchanged
- ERC-20 and ERC-721 — finalised standards, immutable
- Stack, memory and storage — the EVM's 256-bit word and 1024-item stack
- **The oracle problem** — why a deterministic machine cannot read the outside
  world. See the splitting rule below.
- **Why transaction order has to be agreed** — the double-spend problem and why
  a shared state needs a single ordering. Also per the splitting rule.

### Economics — the section that differentiates this site

Davide is an economics researcher, which makes this the one area where the
author is the expert rather than the student. A learner-written Ethereum primer
is one of hundreds; an economist's account of Ethereum's monetary policy and
fee mechanism is rare. **Treat this as the site's distinguishing section, not a
side interest.**

#### The conceptual spine

Not a list of topics — one argument, each step resting on the one before, the
same discipline as the rest of the site.

1. **Why anything must be paid at all.** Ordering transactions has to be
   expensive to attack, which means it has to be rewarded. Somebody must be
   paid, continuously, or the chain is cheap to capture. This is the root of
   everything else and it needs no Ethereum specifics — only the state machine.
2. **Who pays, and how.** There are exactly two sources: **new issuance**,
   which dilutes existing holders, and **fees**, which charge users. Every
   chain picks a mix. This is a tax-incidence question, and framing it that way
   is the single most clarifying move available.
3. **The fixed-cap trade-off.** Bitcoin capped supply, so issuance tends to
   zero and the security budget must eventually come from fees alone — an
   open question, not a solved one. Ethereum left supply uncapped, so it can
   always pay for security, at the cost of any scarcity guarantee. **Neither
   choice is obviously right, and saying so is the honest position.** This is
   the inflation question, and it belongs here.
4. **Pricing block space.** Capacity is scarce and lumpy. A first-price
   auction made users guess each other's bids; EIP-1559 replaced it with a
   posted price that adjusts algorithmically. Mechanism design, with a real
   literature.
5. **Why the base fee is burned.** Paying it to validators would reward them
   for manufacturing congestion. Burning it instead redistributes to all
   holders proportionally. An incentive-compatibility argument with a
   distributional side effect — worth separating those two things.
6. **The value of ordering: MEV.** Whoever controls sequence extracts rent.
   That rent drives the builder and relay markets, and with them
   centralisation pressure.
7. **Capacity as supply.** Rollups and blobs raise effective supply, which is
   why fees fall. The demand side has had far more attention than the supply
   side.

Steps **1–3 need nothing but the state machine** and are Tier 1 — publishable
now, alongside Foundations. Steps **4–7 depend on fees, consensus and
scaling**, and are Tier 2–3.

That's the same **problem then mechanism** split used everywhere else: 1–3 are
questions *any* chain faces, 4–7 are Ethereum's particular answers. The tier
correlation is a consequence, not the organising principle.

#### The wider topic set

The seven-step spine is the backbone. Beyond it, these are the candidates,
grouped by the question they answer. Tier in brackets.

**Monetary policy and supply**

- Staking yield as a native interest rate [3]. A currency that pays a yield for
  being locked up is an unusual object; what does that do to holding behaviour?
- Reflexivity between price and security [1]. The security budget is paid in
  ether but attacks are priced in dollars, so the same issuance rate buys more
  or less security as the price moves. Structural, so Tier 1.
- Liquid staking and concentration [3]. Principal–agent, and a market-structure
  question about why a few providers dominate.

**Public economics — the strongest untapped seam**

- **Congestion pricing** [2]. EIP-1559 is, almost exactly, textbook congestion
  pricing with an algorithmically adjusting Pigouvian charge. The connection to
  Vickrey is direct and essentially nobody makes it.
- **State growth as an externality** [1 for the problem]. Storage is paid for
  once and imposes a cost on every node forever — an uninternalised externality
  and a commons problem. State-rent and statelessness proposals are Pigouvian
  responses. The problem is permanent; the proposals are not.
- Public goods funding [2]. Quadratic funding came out of this ecosystem and has
  a real paper behind it (Buterin, Hitzig & Weyl).

**Market microstructure**

- MEV and ordering rents [3] — already in the spine.
- Proposer–builder separation as vertical disintegration [3]. An industrial
  organisation question: why did block production unbundle, and what does that
  imply about concentration?
- Automated market makers as a pricing mechanism [3]. "Impermanent loss" is
  adverse selection against better-informed traders, which is a far more useful
  framing than the folk term.

**Private money — where stablecoins go**

- **Stablecoins: what makes a peg hold** [1–2]. Fully-reserved, over-collateralised
  and algorithmic designs, and why the failure modes differ. The mechanisms are
  stable concepts even though issuers churn.
- **Runs and reserve quality** [1 for the theory]. Diamond–Dybvig applies almost
  unchanged: a redeemable claim against illiquid reserves is a run waiting for a
  trigger. Terra/UST is a case study in reflexive collapse, not a special
  crypto phenomenon.
- Private money issuance in historical perspective [1]. Free banking, wildcat
  notes, clearing-house certificates. Gorton & Zhang's work makes this comparison
  explicitly. **This is the page that would be hardest for anyone else to write
  and easiest for an economist** — and it needs no protocol machinery at all.

**Transaction cost economics — the most original angle available**

- **What smart contracts actually economise on** [1]. Coase and Williamson,
  applied directly. Contracts reduce the costs of enforcement and custody while
  *raising* the costs of rigidity and of depending on an oracle. That trade-off
  explains both why some applications work and why most would be better as a
  database — which the site already asserts on *What is Ethereum?* without
  having earned it. This page would earn it.

**Layer 2**

- Rollups as firms buying data availability wholesale [3].
- Sequencer revenue and centralisation [3].

#### Where that leaves the technical side

Stablecoins and smart contracts are both wanted by the Economics section, but
the protocol prerequisites are modest:

- **Stablecoins** need only ERC-20 (Tier 1, already queued for Phase 1). The
  *technical* page would be thin — a token with an issuer — so most of the
  substance belongs in Economics.
- **Smart contracts** need the EVM for mechanics [2–3], but the economics page
  above needs only the concept, which *What is Ethereum?* already supplies.

So the Economics section is less blocked on the technical side than it looks.
Three of the strongest candidates — private money in historical perspective,
transaction cost economics, and the state-growth externality — need essentially
no protocol pages that don't already exist.

**Literature for these** (verify each):

- Coase, R. (1937). *The Nature of the Firm.* Economica, 4(16).
- Diamond, D. & Dybvig, P. (1983). *Bank Runs, Deposit Insurance, and Liquidity.*
  Journal of Political Economy, 91(3).
- Gorton, G. & Zhang, J. (2021). *Taming Wildcat Stablecoins.*
- Buterin, V., Hitzig, Z. & Weyl, E. G. (2019). *A Flexible Design for Funding
  Public Goods.* Management Science.
- Vickrey, W. (1969). *Congestion Theory and Transport Investment.* American
  Economic Review, 59(2).

#### Managing it on the site

**A top-level `Economics` section, which owns the arguments and never
re-explains mechanism.** The division:

- **Protocol pages answer "how does this work?"** They may state a mechanism
  and give its rationale in a sentence.
- **Economics pages answer "why this design, what's the trade-off, and what do
  we actually know about the effects?"** Anything needing an *argument* rather
  than a sentence belongs here.

Without that rule the economics gets scattered across a dozen protocol pages,
the argument becomes impossible to follow, and the differentiator evaporates.
With it, both stay readable and neither duplicates the other.

**Late in the reading order**, except the Tier 1 pages, which can sit early
because they need no machinery.

#### A third kind of staleness

Protocol pages go stale by **fork**. Economics pages also go stale by **data**.

"The burn exceeds issuance" is not a fork-dependent claim — it depends on how
busy the network is, and it can reverse without any rule changing. The existing
fork stamp doesn't catch this.

So empirical claims need their own convention, now in the page conventions
above: **state the period, state the source, never state a bare current value.**

#### The real risk here isn't organisation, it's credibility

This is the most narrative-contaminated part of the whole subject. "Sound
money", "ultrasound money", deflation-as-virtue — advocacy repeated so often it
reads as analysis. Four safeguards:

- **Separate positive from normative.** What the mechanism does is one claim;
  whether that's desirable is another. Never let the second ride along inside
  the first.
- **Say what is unknown.** Whether fee-only revenue can secure a chain in the
  long run is genuinely open. Writing "open question" where it's open is worth
  more than any confident answer.
- **Cite the literature, not blog posts**, for anything contested.
- **Refuse the vocabulary.** The loaded terms carry conclusions inside them.
  Describe the mechanism and let the reader judge.

**Literature to build on** (verify each before citing):

- Budish, E. (2018). *The Economic Limits of Bitcoin and the Blockchain.*
  NBER working paper 24717. Formalises the relationship between what a chain
  pays for security per unit time and the value it can safely secure.
- Roughgarden, T. (2020). *Transaction Fee Mechanism Design for the Ethereum
  Blockchain: An Economic Analysis of EIP-1559.* arXiv:2012.00854.
- Daian, P., et al. (2019). *Flash Boys 2.0.* arXiv:1904.05234. Already cited
  on What is Ethereum?; load-bearing for step 6.

### The problem/solution splitting rule

A useful pattern turned up while scoping Proof of Stake and oracles, and it
applies more widely:

> **The problem a mechanism solves is usually fork-proof. The mechanism isn't.**

Ethereum has always needed transactions put in an agreed order, and a
deterministic machine has always been unable to query the internet. Those facts
follow from the design and cannot change. *How* Ethereum orders transactions was
replaced wholesale at The Merge, and oracle designs are commercial products that
change constantly.

So split the page. The **problem** belongs in Phase 1 and never needs
maintaining; the **mechanism** belongs in Phase 2 with a date stamp. This also
reads better — a reader who understands why ordering is hard is far better
prepared for Proof of Stake than one who meets validators and epochs cold.

Applies to: consensus, oracles, scaling (why throughput is limited vs. how
rollups work), and fees (why metering is necessary vs. the current fee market).

**Scope warning for the oracle page:** cover the problem and why it's
unavoidable. Do *not* survey oracle providers — that's fast-moving commercial
ecosystem content with a permanent maintenance cost, and it would be the only
page on the site that rots.

---

# Phase 2 — fork-dependent *(in `/drafts`, not published)*

These stubs are now scaffolded in `docs/` and visible in the menu, but unwritten. They need the foundations above *and* the careful handling described in [FORKS.md](FORKS.md): numbers centralised, pages date-stamped, changes taught as history. They come out of `nav` at launch, with everything else unwritten.

| Draft | Why it waits |
| --- | --- |
| `transactions.md` | Core fields are stable; the *type* list keeps growing |
| `gas.md` | Concept is permanent; every specific cost has been repriced |
| `fees.md` | EIP-1559 rebuilt this in 2021 |
| `state.md` | Verkle trees would replace the trie structure |
| `gas-costs.md` | The single source of truth for all numbers |
| `fork-history.md` | The upgrade timeline |

To publish a draft: move it into the right `docs/` folder and add it to `nav` in `mkdocs.yml`.

## Phase 2 sections not yet drafted

- **Blocks** — blocks, the block header, the chain, reorgs
- **Merkle Patricia Trie** — needs RLP first
- **The EVM** — opcodes, bytecode, deployment, `CALL`/`DELEGATECALL`/`STATICCALL`
- **Consensus** — Proof of Stake, validators, slots and epochs, attestations, finality, withdrawals
- **Scaling** — why rollups, optimistic, ZK, blobs
- **Account abstraction** — ERC-4337, EIP-7702

---

# What the site is missing

An audit, because it's easy to mistake "queued" for "covered". Three dimensions
are **genuinely absent** rather than merely unwritten.

## Absent: applications — what has actually been built

The site explains the machine and will explain its economics, but says nothing
about what anyone has done with it. That's a real hole, and *What is Ethereum?*
currently asserts that "plenty of things built on Ethereum would be better as
an ordinary database" without ever earning the claim.

**The organising question, which makes this a section rather than a catalogue:**

> What does this application need that *only* a trustless ledger provides?

For most of them the honest answer is "nothing" — and saying so, case by case,
is far more useful than another survey of the ecosystem.

| Application | Does it need this machine? |
| --- | --- |
| **Stablecoins** | The clearest real use. Dollar access without a bank, censorship-resistant transfer. Mostly Economics, not protocol. |
| **Exchanges / AMMs** | Genuinely novel pricing mechanism; works because every input is on-chain. No oracle needed. |
| **Over-collateralised lending** | Works, and notably *replaces credit assessment with collateral* — an information-economics story. |
| **Insurance** | The interesting case. See below. |
| **NFTs** | The market largely collapsed; the underlying idea survives in niches. Worth honesty about both. |
| **DAOs / governance tokens** | Collective choice with very low turnout and concentrated holdings. Results are mixed at best. |
| **Supply-chain tracking** | The canonical example of something that should be a database. |
| **Prediction markets** | Constrained far more by regulation and liquidity than by technology. |

### Insurance deserves its own page

Davide raised it, and it's the richest case study available because it fails and
succeeds for *economic* reasons rather than technical ones:

- **The oracle problem binds hardest here.** Payouts depend on real-world events,
  so a trusted data feed is required and the trust you removed comes straight
  back. Parametric products work — flight delay, weather-station rainfall —
  because the trigger is objectively published. Indemnity insurance doesn't,
  because assessing an actual loss needs judgement.
- **Full collateralisation destroys capital efficiency.** This is the strongest
  point and it's pure economics. Traditional insurers are efficient *because*
  they pool weakly-correlated risks, hold fractional reserves and reinsure.
  An on-chain pool must post the full potential payout. That is a large,
  structural cost disadvantage, and no amount of smart contract design removes
  it.
- **Adverse selection and moral hazard are untouched.** Putting the pool
  on-chain does nothing about underwriting.
- **But one real trust cost does go away:** the insurer's discretion to deny a
  valid claim. In markets where that discretion is the actual problem, the
  trade may be worth it.
- Insuring **on-chain** risks (contract failure) is the special case where no
  oracle is needed, since the trigger is visible to the chain.

Which makes insurance the best available illustration of the general rule:
smart contracts economise on enforcement and custody, and pay for it in
rigidity, oracle dependence and capital efficiency.

## Absent: how Ethereum decides to change

Nothing on the site explains *who* changes the protocol or how. EIPs, client
teams, All Core Devs, the absence of on-chain governance for the base layer.
This is partly a collective-choice question, so it borders Economics. Tier 1 for
the structure, Tier 3 for current process.

## Absent: privacy, and things going wrong

Two smaller holes:

- **Everything is public.** Balances, transaction history, contract state. The
  implications barely feature, and they matter to anyone deciding to use it.
  Tier 1.
- **Failure modes.** Reentrancy, oracle manipulation, the economics of audits
  and bug bounties. A site that only explains how things work reads as
  promotional by omission. Tier 1 for the categories.

Also missing and more practical: **wallets and key management** — seed phrases,
what "losing your keys" means, why there's no recovery. A reader-facing gap, and
mostly Tier 1.

## Merely queued, not missing

For contrast, these are already planned above: blocks, transactions, state, gas
and fees, the Merkle Patricia Trie, the EVM and smart contract mechanics,
consensus, rollups and blobs, ERC-20 and ERC-721, signatures, the ABI, events
and logs, fork history, and the interactive tools.

---

# Phase 3 — interactive tools

**Started early, deliberately.** The plan was to leave these until the writing
was done, but the hex page made the case for moving sooner: a converter there
teaches place values better than any amount of prose. So tools now get built
where a page genuinely needs one, rather than all at the end.

Conventions established by the first one:

- **One file, `docs/javascripts/converters.js`**, loaded site-wide via
  `extra_javascript`. Each tool looks for its own element ids and does nothing
  if they're absent, so there's no per-page wiring.
- **Plain JavaScript, no dependencies.** Nothing to keep updated, nothing to
  break, and the whole file stays readable.
- **BigInt throughout, never Number.** A JavaScript Number holds 53 bits
  exactly; an address is 160 and a hash is 256. Using Number would silently
  corrupt real Ethereum values, which is the one bug a tool like this must not
  have.
- **Guard against double-binding.** Material swaps pages without reloading and
  re-runs the file, so each tool marks its root element once.
- **Markup in the page, logic in the file.** The page holds a
  `<div class="tool">` of labelled inputs; the JavaScript holds the behaviour.

- Unit converter (wei ⇄ gwei ⇄ ether)
- Hex ⇄ decimal ⇄ bytes converter
- Keccak-256 hasher
- Private key → public key → address generator
- RLP encoder/decoder
- Transaction decoder
- ABI decoder

Note that every one of these operates on **fork-proof** material, so they won't go stale either.

---

## Two page types, and which one to reach for

The site writes in two registers, and the distinction is worth keeping explicit
because the second one is what a reader with outside expertise actually values.

**Mechanism pages** describe how something works. *Accounts*, *The nonce*,
*State*, *Keccak-256*. They're the majority, and they're what makes the other
kind possible — you can't argue about what persistence costs until the reader
knows what an account holds.

**Argument pages** take a design decision and argue it. *Why accounts, and what
they cost* is the model. What makes them work:

- **One thesis in a sentence**, with everything serving it.
- **Costs and benefits as the same property seen twice**, never a pros-and-cons
  list. Privacy and persistent identity are one fact, not two.
- **A frame borrowed from outside Ethereum** — the mispriced-commons reading of
  state growth, cited to Hardin — so a reader has somewhere to stand.
- **Refusing the lazy evaluative question.** "Was it the right call" is badly
  formed; "which of its bills are still outstanding" is answerable.

Already planned in this register: *Why metering is necessary*, all four
economics pages, *What it reveals*, and the client-diversity argument on
*Clients and the two layers*.

Both gaps from the missing-topics audit are now stubbed as argument pages:
**privacy** (*What it reveals*, closing Part 4) and **governance** (*Who
decides, when nobody is in charge*, closing Part 7). Neither can be written
yet — privacy needs transactions, governance needs the fork material — but both
are in the menu so the plan is visible rather than remembered.

## Page conventions

Every page follows the same template. The point is that a beginner and a
specialist can read the *same* page and each get what they came for — rather
than maintaining two versions that drift apart.

1. **`description:` frontmatter** — one sentence, used as the search-result
   snippet.
2. **Accessible main prose.** No unexplained jargon. This is the default
   reading path, and it must stand alone.
3. **Every extra box is collapsible — `???`, never `!!!`.** This is the
   layering mechanism: one page serves both audiences instead of two pages
   that drift apart.

   **Choose the type by what the box contains**, not for visual variety.
   Material gives each type its own colour, so getting the meaning right
   gets the colour right as a side effect:

   | Type | Colour | Holds |
   | --- | --- | --- |
   | `abstract` | light blue | specification-level precision — notation, exact widths, derivations, quantitative margins |
   | `info` | cyan | **history and change over time** — how it used to work, what is changing |
   | `note` | blue | a plain aside: terminology, a clarification, a caveat |
   | `question` | light green | a question a reader arrives with, or a distinction they routinely get wrong |
   | `warning` | orange | a trap that costs you something |
   | `failure` | red | the conditions under which something is rejected |
   | `example` | purple | an **interactive tool**, always titled `Try it: …` |

   **No mixing, and all closed by default.** The main prose must stand alone
   without any of them — a reader who opens nothing should lose nothing, and
   nothing load-bearing may live only inside a box.

   **Check what's adjacent.** Two consecutive boxes of the same type read as
   one undifferentiated block, which hides that they make separate points. If
   two neighbours genuinely want the same type, move one rather than
   mislabelling it.

   **One deliberate exception:** tools are always `example`, even consecutively.
   A reader should recognise a tool instantly, and that consistency is worth
   more than the adjacency rule.

   **Titles must be distinct within a page.** Two boxes both called "The formal
   version" are indistinguishable in a table of contents — name what each one
   is formal *about*.

   `!!! definition "Term"` — **the one content box that stays open.** Teal,
   with a bookmark icon, defined in `extra.css` because Material has no such
   type. Holds the page's central term stated plainly, so a reader scanning
   the page can spot it. Hiding a definition behind a click would be
   perverse — it isn't supplementary reading.

   **Every content page has exactly one**, near the top, naming the term in
   the page title. The pattern that avoids redundancy: let the prose keep the
   memorable framing and give the box the *precise* statement. *Private keys*
   still opens "a private key is a number, that's the whole of it" — the box
   then supplies the 256 bits, the 32 bytes, and what the key is actually
   for. Complementary, not duplicated.

   Where a definition was already sitting in the prose, it moved into the box
   and the surrounding sentences were rewritten so nothing is said twice.

   **So four kinds stay open**, none of them skippable reading *about the
   subject*: the `Stub — not written yet` notice, the `Current as of …`
   staleness stamps, `danger` boxes, and `definition` boxes.

   `danger` is reserved for **where ignoring it costs money**, and always
   open — a caution behind a click is a caution nobody reads. Three so far:
   never funding a key from the generator on *Private keys*, not generating a
   key by hand with dice on *Seed phrases*, and recovery services being
   categorically fraudulent on *Losing your keys*. Each one earns it by
   following from the page's own argument rather than being appended as
   general prudence. That reservation is
   what keeps it meaningful; anything merely surprising or easy to get wrong
   is a `warning`, and may be collapsed.

4. **The sidebar is six questions, not ten topics.** Part labels are
   *What it is · Who can act · What it holds · How it changes · When it's
   settled · Why anyone bothers*, which in order read as a sentence
   summarising the whole site.

   Three decisions inside that, each of which started as a mistake:

   **Keccak-256 sits in part one, not with the keys.** It's a primitive that
   addresses, the state root, transaction hashes and function selectors all
   depend on — nothing to do with identity. It was under *Cryptography* only
   because it precedes private keys in reading order, which is placement by
   accident.

   **"What it holds", never "Where".** Ethereum has no location; every node
   holds the same state. A part called *Where* primes a reader to look for a
   place — a server, a cloud — which is exactly the model the state page
   opens by demolishing. A part name must not ask the question its pages have
   to argue against.

   **A page belongs to the part its own content serves, not the part its
   topic belongs to in general.** *Contracts* sounds like execution, so it
   went under *How it changes*; but that page is about what a contract **is**
   — an account with code — and defers the EVM entirely. It belongs with
   accounts. The EVM page, when written, belongs under *How*.

   The *Fork-dependent details* section was folded away for a related reason:
   once every page carried a durability label in its first line, a whole menu
   section signalling staleness duplicated it, while introducing a second
   organising principle — maintenance risk — competing with the questions.
   Gas costs moved under *How it changes*, fork history under *About*.
   The searchable words — Keccak, nonce, gas — are the page titles directly
   beneath, which is where a reader arriving from a search engine lands
   anyway.

   **Both levels are kept.** The parts sit above the original topic sections
   rather than replacing them: *Who you are* contains *Cryptography* and
   *Wallets*, *What it knows* contains *Accounts and state*, *Contracts* and
   *Encoding*. The first attempt flattened the topics away and lost the words
   a reader scans for — "Cryptography" and "Blocks" stopped appearing in the
   menu at all. Keeping both means the question orients you and the topic name
   is still findable.

   Parts holding a single topic (*What it is*, *Why anyone bothers*) list their
   pages directly, since a one-child subsection is a level of nesting earning
   nothing. Directory names were left alone throughout, so no URL moved — the
   same trick as *Fork-dependent details* pointing at `reference/`.

   Three ranks therefore need distinguishing in `extra.css`, and the rule
   order matters: the part selector is the least specific, so the topic and
   page rules must come after it or all three render identically. **Size
   carries the rank, not capitals** — parts are set larger with a little space
   above, topics are bold at body size, pages are plain. Small caps were tried
   first and shout too much for a label read far more often than it is
   clicked.
   The expand animation also needs **two** max-height ceilings now — a part
   holding three expanded topics is far taller than a topic holding four
   pages, and a ceiling sized for the larger makes the smaller snap open.

   Rejected first: a coloured left-edge accent per part. The hues had to be
   low-saturation to avoid colliding with the palette that already means
   something (teal = definition, red = danger, amber = warning), and at that
   saturation five 2px lines are indistinguishable. **The idea didn't survive
   being made tasteful enough not to clash** — which is the argument that
   colour was the wrong instrument, not merely the wrong palette.

5. **An opening durability label**, the first line of every content page,
   bolded and linking to `about/forks.md`:

   - `**[Permanent](../about/forks.md).**` — nothing here can go stale.
   - `**[Permanent, except one part](../about/forks.md).**` — then the
     sentence after it names *which* part. Never "mostly": a hedge tells the
     reader something is unreliable without telling them what.
   - `**[Permanent in practice](../about/forks.md).**` — used once, on *seed
     phrases*, where the material is convention rather than protocol. Nothing
     binds anyone to BIP-39, so the stronger claim would be false.

   This replaced `**Fork-proof.**`, which was internal vocabulary appearing on
   the site's second content page and explained nowhere — not on the homepage,
   not in the glossary. **The standing lesson: terminology invented for
   maintenance must not reach the reader.** `Tier 2`, `Tier 3` and
   `fork-proof` all leaked before anyone noticed, so grep for them before
   publishing.

6. **In-text citations, author–date style**, linking to the reference:
   `[Wood (2014)](#ref-wood-2014)` when the author is the subject of the
   sentence, `[(Nakamoto, 2008)](#ref-nakamoto-2008)` when it's parenthetical.
   This replaced footnotes — it shows the reader where a claim comes from at
   the point they read it, rather than making them chase a number.
7. **A `## References` section** at the end, wrapped in
   `<div class="sources" markdown>`, **alphabetical by author surname**.
   Each entry carries an explicit anchor so citations can link to it:
   `- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Title.* Venue. URL`

   Anchors are written as inline HTML rather than `attr_list` because
   `def_list` and list items don't reliably take generated ids.

   EIPs are cited by number rather than author — `EIP-3675 (2021)` — because
   that's how everyone refers to them. They sort under E.

   **Never write "n.d."** for a living online source. It claims there's no date
   when the truth is that the date is "always now", and it tells the reader
   nothing useful. Use whichever of these the source supports:

      - **A pinned version**, where one exists. Software documentation is the
        common case: cite `(Solidity documentation, v0.8.26)` and link the
        versioned URL, not `/latest/`. More rigorous than any date — the
        reader sees exactly the text you read, and `latest` would silently
        move under them. The Solidity entry notes that `szabo` and `finney`
        were removed in earlier versions, which is precisely why pinning
        matters.
      - **An access date in the entry**, where there's no version: *"continuously
        updated; accessed November 2026."* In the prose, cite it by title
        rather than year — *Edgington's "Upgrading Ethereum"* — so no empty
        year slot appears at all.
6. **Verify every citation** against the original before publishing. A wrong
   reference costs more credibility than no reference.

   **Empirical claims carry a period and a source, never a bare value.** This
   is a different kind of staleness from forks: "the burn exceeds issuance"
   depends on how busy the network is and can reverse with no rule changing, so
   a fork stamp won't catch it. Write *"over 2024, X exceeded Y (source)"*, not
   *"X exceeds Y"*. Mostly matters in the Economics section.

   Two further rules on citations, both learned the hard way:

      - **Cite what the page claims, not what the page is about.** Every
        reference must be cited somewhere in the prose. If you can't find a
        sentence to attach it to, it's padding — and a reader who follows it up
        and finds nothing relevant trusts the rest of the page less. Author–date
        citations make this self-enforcing: an uncited entry is visibly orphaned.
      - **Say so when the fit is partial.** If a source is the best available
        evidence but not a direct one, say so in the sentence that cites it.
        Costs a clause, buys the reader's trust.

   Keep References as one flat alphabetical list. Only group under subheadings
   past roughly a dozen entries — the `.sources h3` style exists for that, but
   a heading over four items is heavier than it's worth.
7. **Unfamiliar terms: one mechanism only — a link carrying a title.**

   ```markdown
   [gas](../glossary.md#gas "The unit computational work is measured in")
   ```

   With `content.tooltips` enabled, this hovers *and* clicks: the title shows
   as a styled tooltip in place, and the link goes to the full entry. The
   reader never has to leave the page to look something up, but can go deeper
   when they want to.

   Rules:
      - **Link to the term's own page if it has one**, otherwise its glossary
        anchor. A real page always beats a one-line entry.
      - **First use per page only.** A page where every third word is a link is
        unreadable.
      - **Keep the title short** — a phrase, not the glossary's full definition.
        It stays readable, and there's less to drift out of step.
      - **Don't link terms the page defines in place.** Sending someone to a
        one-line entry for something just explained at length is worse than no
        link. UTXO, Beacon Chain and the account fields are unlinked for this
        reason.
      - **Nothing is hover-only.** If a term is marked up at all, it is
        clickable. Plain text means no affordance and no confusion.

   The `abbr` extension was used for this and **removed deliberately**. It
   produced hover-only terms, dotted-underlined so they looked clickable,
   sitting beside real links — two mechanisms a reader could not tell apart,
   with native browser tooltips that truncated long definitions.

`docs/foundations/what-is-ethereum.md` is the reference implementation of all
six.

---

## Known ordering tensions

Worth staying conscious of these:

- **Addresses need Keccak-256** — resolved by putting Keccak first in the cryptography section.
- **Accounts mention `storageRoot` and `codeHash`**, which need the state trie and the EVM. Name the fields, say what they commit to, promise detail later. Don't bluff it.
- **The nonce needs the idea of a transaction**, but not its anatomy. "What is Ethereum?" supplies the one sentence required.
- **RLP underpins the Patricia trie**, but the trie is Phase 2 while RLP is Phase 1. Fine — RLP stands alone.
- **Gas costs only make sense alongside opcodes.** Both are Phase 2; keep them adjacent when you get there.
