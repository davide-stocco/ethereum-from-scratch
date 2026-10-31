# Accounts

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof, with one caveat** — see the note at the bottom.

## Questions this page should answer

- What are the two kinds of account?
    - **EOA** (externally owned account) — controlled by a private key
    - **Contract account** — controlled by its own code
- What four fields does every account have? These have been the same since genesis:
    - `nonce`
    - `balance`
    - `storageRoot`
    - `codeHash`
- How can you tell the two kinds apart, given both are just 20-byte addresses? (An EOA's `codeHash` is the hash of empty data.)
- Who can *start* a transaction? (Only an EOA. Contracts act solely in response to being called — nothing on Ethereum runs by itself, and there are no timers or cron jobs.)
- What happens to an account with a zero balance that's never been used? (Nothing is stored. It isn't in the state at all. All 2<sup>160</sup> addresses exist in principle, holding nothing.)
- Why does an account-based design need a [nonce](nonce.md), when Bitcoin's coin-based design doesn't?

## Notes to self

- This is where the Bitcoin comparison pays off: **accounts, not UTXOs.** Spell out the consequence — order matters, which is exactly why the nonce has to exist. That sets up the next page.
- "Contracts can't act on their own" is the single most clarifying fact for a beginner. Give it room.
- `storageRoot` and `codeHash` can't be fully explained yet — they need the state trie and the EVM, neither of which is published. Name the fields, say what they commit to, and promise the detail later. Don't bluff it.

!!! info "One thing here is changing"

    The four account fields are permanent. The clean split between the two
    *kinds* of account is softening: **EIP-7702**, which shipped in May 2025,
    lets an EOA point at contract code, so "EOAs have no code" is no longer
    strictly true.

    Write this page around the four fields and the "only EOAs initiate
    transactions" rule — both still hold. Mention the blurring in a note
    rather than restructuring the page around it.

    See [how this site handles forks](../about/forks.md).

**Next:** [The nonce](nonce.md)
