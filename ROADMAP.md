# Roadmap

Two organising principles:

1. **Ordering** — no page explains something that depends on a page further down.
2. **Fork stability** — publish the permanent core first. See [FORKS.md](FORKS.md) for the full classification.

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
3. **`??? abstract "The formal version"`** — a *collapsed* block wherever there
   is a precise definition worth stating: specification notation, exact field
   widths, edge cases. Collapsed by default, so a beginner skips it and a
   specialist opens it. This is the layering mechanism.
4. **Footnotes** for citations attached to specific claims (`[^key]`).
5. **A `## Sources` section** at the end, wrapped in
   `<div class="sources" markdown>`. Papers, specifications and EIPs —
   author, year, title, venue, link, and a line on what it supports.
6. **Verify every citation** against the original before publishing. A wrong
   reference costs more credibility than no reference.

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
