---
tier: 1
description: A token is not a protocol feature. It is a contract keeping a list of numbers, and owning one means a number in somebody else's storage.
---

# Tokens aren't special

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**[Permanent](../about/forks.md).** That tokens are contracts rather than a protocol feature has been true since the first one, and the standards that describe them are finalised documents that cannot be revised.

## The thesis this page exists to argue

**Ethereum has one native asset: ether.** Everything else people hold — every stablecoin, every governance token, every NFT — is not a thing the protocol knows about. It is a [contract](smart-contracts.md) keeping a mapping from address to number, and "owning" one means **there is a number recorded against your address in somebody else's storage.**

Which sounds reductive and is the literal mechanism. The consequences are not reductive at all, and they explain most of what surprises people about holding tokens.

## Questions this page should answer

- What is a token, mechanically? (A contract with a mapping of address → balance, and functions to change it. That's all. Show how small the essential idea is.)
- So what do you own? (**The central answer.** Not an object. An entry in a particular contract's storage — which means your ownership is exactly as good as that contract's code and its author's intentions.)
- Why does your wallet show tokens it doesn't hold? (It queries token contracts for your address and displays the answers. A token you have never heard of can appear in your wallet because somebody wrote your address into their contract — you did not receive anything.)
- Why do you need **ether** to move a token? (The fee is payable only in ether, as the [ether](../foundations/ether.md) page said. Hence the account with a fortune in tokens and nothing it can do — this is where that situation is finally explained rather than mentioned.)
- What is a standard, and why does it matter? (ERC-20 and ERC-721 are **agreed function names and behaviours**, not protocol rules. A contract that follows them works with every wallet; one that doesn't is still a valid contract that nothing can read. Conventions all the way down, like the ABI and the derivation path.)
- Can a token's author take yours, or stop you moving it? (**Often yes**, and this is the section that earns the page. Whatever the code allows, the author can do — freeze, mint, blacklist, upgrade. Whether any given token permits it is a question about its code, not about Ethereum.)
- What is an **approval**, and why is it the biggest practical hazard? (Permission for another contract to move your tokens, granted once and lasting until revoked. Explain the mechanism and why the risk is structural rather than a bug: the token contract has no idea whether the spender deserves it.)
- Is an NFT different in kind? (No — same shape, mapping address to a token identifier rather than a quantity. And what it points *at* is usually a URL, so "owning the artwork" is a claim about somebody's web server.)

## Notes to self

- **This is probably the highest-value page in this part**, because tokens are what most people mean by "smart contracts" and the gap between the folk model and the mechanism is enormous.
- Argue it in the [why accounts](../accounts/why-accounts.md) register: one thesis — ownership is a number in somebody else's storage — and every consequence derived from it rather than listed.
- **Do not name tokens or projects.** Mechanisms and classes only, per [FORKS.md](../about/forks.md). The mechanisms are permanent; the products are not, and naming them would also read as commentary on specific assets.
- Resist the temptation to editorialise about the asset class. State the mechanism and let the reader conclude — the same discipline the governance page needs.
- The approvals section is where a reader could be protected from real loss, so be precise and avoid advice that dates. The structural point — permission persists until revoked, and the token contract cannot judge the spender — is permanent.
- Ties to collect: ether-only fees, the account model's persistent identity, logs as the only usable record of transfers, and the "immutable" caveat from [what a smart contract is](smart-contracts.md).

**Next:** [RLP encoding](../encoding/rlp.md) — how all of this gets written down as bytes.
