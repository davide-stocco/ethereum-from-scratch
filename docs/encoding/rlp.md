# RLP encoding

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** Recursive Length Prefix has not been revised since genesis.

## Questions this page should answer

- What problem does RLP solve? (Turning structured data — a list of items, possibly containing lists — into a single flat string of bytes, reversibly.)
- Why does Ethereum need its own encoding rather than using JSON or Protobuf? Two reasons, and the second is the important one:
    1. It's minimal and cheap to implement.
    2. It's **canonical** — one piece of data has exactly one valid encoding. Without that, two nodes could hash the same data and get different answers, and consensus would collapse.
- What are the only two things RLP can encode? (A **byte string**, and a **list** of items. That's it. No integers, no booleans, no maps — those get converted to byte strings first.)
- What are the four encoding rules?
    - A single byte below `0x80` encodes as itself
    - A short string (0–55 bytes) gets a `0x80 + length` prefix
    - A long string gets a prefix encoding the *length of the length*
    - Lists work identically, starting at `0xc0`
- Where is RLP used? (Transaction encoding, block headers, and every node in the state trie.)
- Why are integers encoded with no leading zeros? (Canonicality again — `0x01` and `0x0001` must not both be valid.)

## Notes to self

- This page lives or dies on worked examples. Encode `"dog"`, then `["cat", "dog"]`, then an empty list, byte by byte.
- The canonicality point is the one that makes RLP make *sense*. Lead with it — most explanations bury it and leave readers wondering why Ethereum didn't just use JSON.
- Don't cover the Merkle Patricia Trie here, even though it's built on RLP. Separate page, and it's not fork-proof (Verkle trees are planned).
- Excellent candidate for an interactive encoder/decoder widget later.

**Next:** [Accounts](../accounts/accounts.md)
