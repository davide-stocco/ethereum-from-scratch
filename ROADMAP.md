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

Reading order once everything exists. **Bold** = published or Phase 1;
everything else is Phase 2+. Note how each problem page sits directly above the
mechanism that answers it.

```
Home
Foundations            What is Ethereum? · Ether/wei/gwei · Hex and bytes
Cryptography           Keccak-256 · Private keys · Public keys · Addresses
                       Signatures
Encoding               RLP
                       Merkle Patricia Trie                      [tier 2]
Accounts and state     Accounts · The nonce
                       State                                     [tier 2]
Transactions           Why metering is necessary                  <- problem
                       Transactions                              [tier 2]
                       Gas and the fee market                    [tier 3]
Blocks                 Blocks · The block header                 [tier 3]
Consensus              Why order has to be agreed                 <- problem
                       Proof of Stake · validators · finality    [tier 3]
The EVM                The EVM · opcodes · storage · the ABI
                       Gas costs per operation                   [tier 2]
Limits                 The oracle problem                         <- problem
                       Why throughput is limited                  <- problem
                       Rollups and blobs                         [tier 3]
Reference              Gas costs table · Fork history            [tier 2/3]
Glossary
About                  Ethereum changes · Who's writing this
```

Two things to notice. The **Reference** section is where every fork-dependent
*number* is centralised, so repricings touch one file. And **Limits** groups the
inherent constraints — a genuine topic, not a tier bucket: readers do look for
"what can't this do", and all three pages there are about the same thing.

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

These stubs already exist in `drafts/`. They stay unpublished until Phase 1 is written, because they need the foundations above *and* because they need the careful handling described in [FORKS.md](FORKS.md): numbers centralised, pages date-stamped, changes taught as history.

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

# Phase 3 — interactive tools

Save these for last; they need HTML and JavaScript, which is worth learning once the writing is done. They're also what makes a site like this memorable.

- Unit converter (wei ⇄ gwei ⇄ ether)
- Hex ⇄ decimal ⇄ bytes converter
- Keccak-256 hasher
- Private key → public key → address generator
- RLP encoder/decoder
- Transaction decoder
- ABI decoder

Note that every one of these operates on **fork-proof** material, so they won't go stale either.

---

## Page conventions

Every page follows the same template. The point is that a beginner and a
specialist can read the *same* page and each get what they came for — rather
than maintaining two versions that drift apart.

1. **`description:` frontmatter** — one sentence, used as the search-result
   snippet.
2. **Accessible main prose.** No unexplained jargon. This is the default
   reading path, and it must stand alone.
3. **Every extra box is collapsible — `???`, never `!!!`.** This is the
   layering mechanism: one page serves both audiences instead of two pages that
   drift apart. Common kinds:
      - `??? abstract "The formal version"` — specification notation, exact
        field widths, edge cases.
      - `??? info "History: …"` — how something used to work and why it
        changed. Often the clearest justification for the current design, and
        the fork policy's "teach changes as history" in practice.
      - `??? note "…"` — asides, terminology, caveats.

   **No mixing.** An always-open `!!!` box sitting beside collapsed ones reads
   as a mistake, and a reader can't tell what the convention is. All closed by
   default; the main prose must stand alone without any of them.

   **The only `!!!` boxes are status notices about the page itself** — the
   "Stub — not written yet" warnings and the glossary's scope note. Those are
   not content a reader may skip, so they stay open, and the difference in
   purpose justifies the difference in form.

   **A collapsed title has to be self-describing**, since it's all the reader
   sees. "Two simplifications in the table above" works; "Note" doesn't.

   Avoid double quotes inside a title — they terminate it early. Use single
   quotes: `??? note "Where does the 'world computer' phrase come from?"`
4. **In-text citations, author–date style**, linking to the reference:
   `[Wood (2014)](#ref-wood-2014)` when the author is the subject of the
   sentence, `[(Nakamoto, 2008)](#ref-nakamoto-2008)` when it's parenthetical.
   This replaced footnotes — it shows the reader where a claim comes from at
   the point they read it, rather than making them chase a number.
5. **A `## References` section** at the end, wrapped in
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
