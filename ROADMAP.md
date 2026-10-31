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
3. **Collapsed blocks** for anything a reader can skip without losing the
   thread. This is the layering mechanism — one page serves both audiences,
   instead of two pages that drift apart. Two kinds:
      - `??? abstract "The formal version"` — specification notation, exact
        field widths, edge cases.
      - `??? info "History: …"` — how something used to work and why it
        changed. Often the clearest justification for the current design, and
        the fork policy's "teach changes as history" in practice.

   Both are closed by default and the main prose must stand alone without them.
   The homepage tells readers this explicitly, so skipping a box never feels
   like missing something.
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
6. **Verify every citation** against the original before publishing. A wrong
   reference costs more credibility than no reference.

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
7. **Unfamiliar terms get a destination.** Three mechanisms, in priority order:
      - If the term **has its own page**, link to that page. Always better than
        a one-line definition.
      - If it **doesn't have a page yet**, link to its glossary entry on first
        use — `[gas](../glossary.md#gas)`. Anchors exist for all 40 terms.
      - **Acronyms and short jargon** get a hover tooltip automatically, from
        `includes/abbreviations.md`, with no markup in the prose. Deliberately
        excludes words used dozens of times per page (state, transaction,
        account, block, ether, wei) — tooltipping those would underline half
        the text.

   Link on **first use per page** only. A page where every third word is a link
   is unreadable.

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
