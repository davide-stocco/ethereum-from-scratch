---
tier: 1
description: Why there is no password reset, no customer service, and no way back — and what that actually implies.
---

# What losing your keys means

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** A direct consequence of how [addresses](../crypto/addresses.md) are derived. It cannot be changed.

## Questions this page should answer

- Why is there no recovery? (Nobody issued your account. There's no record connecting it to you, and no authority with the power to reassign it.)
- What would a "reset" even require? (Someone able to move funds without the key — which is precisely what an attacker needs. The two are indistinguishable to the protocol.)
- What happens to the ether? (Nothing. It stays in the state forever, visible and unspendable.)
- What is the difference between losing a key and losing a **seed phrase**?
- Can a contract soften this? (Yes — this is what account abstraction and social recovery address, by putting the authority under code rather than one key. Worth naming, not explaining here.)
- Is irrecoverability a **feature**? Honestly: it's the cost of the thing being valuable. The same property that stops anyone confiscating your funds stops anyone restoring them.

## Notes to self

- Keep this page short and unsentimental. The temptation is either to lecture about backups or to be grim. Neither helps.
- The strongest framing is the symmetry: **no privileged party** means no confiscation *and* no recovery. You cannot have one without the other. That earns the page its place — it's the clearest illustration on the site of what "no one is in charge" actually costs.
- Avoid statistics about lost coins. The numbers are estimates and they age.

**Next:** [Accounts](../accounts/accounts.md)
