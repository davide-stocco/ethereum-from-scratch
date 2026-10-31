# Fork policy

Ethereum changes by **hard fork** — a coordinated upgrade where every node switches rules at an agreed block or slot. There have been roughly twenty since 2015.

This is a maintenance problem for a reference site. The answer isn't to document every fork; it's to **write pages that don't depend on the fork in the first place**, and isolate the parts that do.

---

## The one rule

> **Concept pages explain mechanisms. Reference pages hold numbers.**
>
> Never hardcode a gas cost, a fee parameter, a block time, or a field list into a concept page. State the *reason* the number exists, and link to the reference table.

Why this works: *"writing to storage is expensive because every node must keep it forever"* was true in 2015 and will be true in 2035. *"Writing to storage costs 20,000 gas"* was true in 2015, wrong by 2019, and wrong again by 2021.

The reason is fork-proof. The number is not. Put them in different files.

---

## Tier 1 — Fork-proof

Unchanged since genesis, and changing any of them would break every wallet, library and contract in existence. Write these once and never revisit them.

| Page | Why it's safe |
| --- | --- |
| Hex and bytes | Not a protocol rule at all |
| Ether, wei, gwei | 10<sup>18</sup> wei per ether, fixed since genesis |
| Private keys | secp256k1, 256-bit — unchanged since genesis |
| Addresses | `keccak256(pubkey)`, last 20 bytes — unchanged since genesis |
| EIP-55 checksums | Finalised 2016, never revised |
| Keccak-256 | Ethereum's hash function since genesis |
| RLP encoding | Unchanged since genesis |
| The nonce | Sequential-counter semantics never revised |
| The ABI | A convention, not a consensus rule |
| Stack, memory, storage model | 256-bit words, 1024-item stack — original design |
| Events and logs (mechanism) | Structure unchanged |
| ERC-20, ERC-721 | Finalised standards; immutable once final |
| What is Ethereum (state machine) | Conceptual |

**That's over half the site.** Start here — it's the content with the longest shelf life.

## Tier 2 — Stable concept, volatile detail

The idea is durable; specific numbers or field lists are not. Safe to write now, provided you follow the one rule above.

| Page | Durable | Volatile |
| --- | --- | --- |
| Gas | Why metering exists; why storage costs more than arithmetic | Every specific cost |
| Fees | Base fee + priority fee + burn | Parameters, and the pre-London mechanism |
| Accounts | Four fields; EOA vs contract | EIP-7702 now lets an EOA carry code — the clean split is blurring |
| State | State root commits to all accounts | Verkle trees would replace the trie structure |
| Transactions | Core fields; signature recovery | The *list* of transaction types keeps growing |
| The EVM | Stack machine, deterministic execution | Opcode set grows each fork |
| Merkle Patricia Trie | How hash-commitment works | Verkle replacement is actively planned |
| Blocks | Blocks bundle transactions and chain by hash | The exact header field list has grown repeatedly |

## Tier 3 — Fork-defined

These *are* fork output. Expect to rewrite them, and date-stamp them clearly.

| Page | Churn |
| --- | --- |
| Transaction types | Legacy → 2930 → 1559 → 4844 → 7702, still growing |
| Block header fields | Gained `baseFeePerGas`, `withdrawalsRoot`, blob fields, beacon root |
| Proof of Stake, validators | The Merge replaced consensus wholesale |
| Slots, epochs, finality | Timing and committee parameters get tuned |
| Withdrawals | Didn't exist until Shanghai (2023) |
| Blobs | New in Cancun (2024); capacity raised since |
| Opcodes added | `PUSH0`, `MCOPY`, `TLOAD`/`TSTORE`, `BLOBHASH`… |
| `SELFDESTRUCT` | Semantics changed in Cancun (EIP-6780) |
| Precompiles | Added over time |
| Account abstraction | ERC-4337, then EIP-7702 |
| Rollups and scaling | Ecosystem, not just protocol — fastest-moving section |

**Write Tier 3 last.** You'll understand it better by then, and you'll rewrite it less.

---

## How to handle it on the page

**1. Stamp volatile pages.** Put this under the title of any Tier 2 or Tier 3 page:

```markdown
!!! info "Current as of the Pectra upgrade (May 2025)"

    Gas costs and parameters change at hard forks. If you're reading this
    much later, check [the reference table](../reference/gas-costs.md).
```

**2. Keep every number in one file.** The gas-costs page is the single source of truth. When a fork changes costs, you edit one file — not the twelve pages that mention them. The stub currently lives at `drafts/gas-costs.md`; move it to `docs/reference/` when you publish Phase 2.

**3. Explain changes as history, not as corrections.** When a fork changes something, the old behaviour is often the clearest way to explain why the new one exists. EIP-1559 makes far more sense once you know fee bidding was a blind auction. Write it as *"it used to work like X, which had problem Y, so now it works like Z."* That turns your maintenance burden into your best teaching material.

**4. Don't version the whole site.** There's an MkDocs plugin (`mike`) that publishes a version selector for multiple site versions. **Don't use it here.** It suits software docs where users run old releases. Ethereum has one live network — nobody needs the London-era version of your site. One current site plus a history page is the right model.

---

## Maintenance checklist

After each hard fork, review only:

- [ ] the gas-costs reference — any repricings?
- [ ] the fork-history page — add the new entry
- [ ] Transaction types — a new type?
- [ ] Block header — new fields?
- [ ] Opcodes — additions or changed semantics?
- [ ] Consensus parameters — timing, validator rules?

Six items. Tier 1 needs no review, ever.

---

## Verify fork status yourself

My own knowledge has a cutoff, and this list ages. Check against primary sources rather than trusting any secondary summary, including this one:

- <https://ethereum.org/en/history/> — fork history, maintained
- <https://eips.ethereum.org> — the EIPs themselves, authoritative
- <https://github.com/ethereum/execution-specs> — the actual rules, per fork

Pectra (Prague/Electra) activated on mainnet in May 2025. **Confirm what has shipped since then before you write Tier 3** — treat anything I tell you about recent forks as needing a check.
