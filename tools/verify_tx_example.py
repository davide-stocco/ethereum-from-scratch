"""Verify the worked example on the transactions page.

Not a CI gate — a record of how the example was checked, so the check can be
repeated rather than believed. Implements Keccak-256 from the specification
(there is no keccak in the standard library: hashlib's sha3_256 uses the
other padding byte), self-tests it against two published digests, then:

  - hashes EIP-155's signing bytes and compares against the signing hash the
    EIP publishes, which validates the implementation and the example at once
  - RLP-decodes the signed transaction and checks all nine fields against the
    EIP's stated values, including r and s as decimal integers
  - computes the transaction hash the page quotes
"""

# Keccak-256 from the specification, so the worked example can be verified
# here rather than taken on trust.
RC = [0x0000000000000001,0x0000000000008082,0x800000000000808A,0x8000000080008000,
      0x000000000000808B,0x0000000080000001,0x8000000080008081,0x8000000000008009,
      0x000000000000008A,0x0000000000000088,0x0000000080008009,0x000000008000000A,
      0x000000008000808B,0x800000000000008B,0x8000000000008089,0x8000000000008003,
      0x8000000000008002,0x8000000000000080,0x000000000000800A,0x800000008000000A,
      0x8000000080008081,0x8000000000008080,0x0000000080000001,0x8000000080008008]
R = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
M = (1 << 64) - 1
def rol(x, n): return ((x << n) | (x >> (64 - n))) & M

def keccak_f(A):
    for rnd in range(24):
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x-1) % 5] ^ rol(C[(x+1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                A[x][y] ^= D[x]
        B = [[0]*5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2*x + 3*y) % 5] = rol(A[x][y], R[x][y])
        for x in range(5):
            for y in range(5):
                A[x][y] = B[x][y] ^ ((~B[(x+1) % 5][y] & M) & B[(x+2) % 5][y])
        A[0][0] ^= RC[rnd]
    return A

def keccak256(data: bytes) -> bytes:
    rate = 136
    p = bytearray(data) + b"\x01"
    while len(p) % rate != 0: p.append(0)
    p[-1] ^= 0x80
    A = [[0]*5 for _ in range(5)]
    for off in range(0, len(p), rate):
        blk = p[off:off+rate]
        for i in range(rate // 8):
            lane = int.from_bytes(blk[i*8:(i+1)*8], "little")
            A[i % 5][i // 5] ^= lane
        A = keccak_f(A)
    out = b""
    while len(out) < 32:
        for i in range(rate // 8):
            out += A[i % 5][i // 5].to_bytes(8, "little")
            if len(out) >= 32: break
    return out[:32]

# --- self-test against published Keccak-256 values -------------------------
assert keccak256(b"").hex() == "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
assert keccak256(b"abc").hex() == "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"
print("keccak self-test: PASS (empty string and 'abc' match published values)")

# --- minimal RLP decoder ---------------------------------------------------
def dec(b, i=0):
    p = b[i]
    if p < 0x80: return b[i:i+1], i+1
    if p < 0xb8:
        n = p - 0x80; return b[i+1:i+1+n], i+1+n
    if p < 0xc0:
        l = p - 0xb7; n = int.from_bytes(b[i+1:i+1+l], "big"); return b[i+1+l:i+1+l+n], i+1+l+n
    if p < 0xf8:
        n = p - 0xc0; j = i+1; end = j+n; out=[]
        while j < end:
            v, j = dec(b, j); out.append(v)
        return out, end
    l = p - 0xf7; n = int.from_bytes(b[i+1:i+1+l], "big"); j = i+1+l; end = j+n; out=[]
    while j < end:
        v, j = dec(b, j); out.append(v)
    return out, end

SIGNING = bytes.fromhex("ec098504a817c800825208943535353535353535353535353535353535353535880de0b6b3a764000080018080")
SIGNED  = bytes.fromhex("f86c098504a817c800825208943535353535353535353535353535353535353535880de0b6b3a76400008025a028ef61340bd939bc2195fe537567866003e1a15d3c71ff63e1590620aa636276a067cbe9d8997f761aecb703304b3800ccf555c9f3dc64214b297fb1966a3b6d83")

print("\nEIP-155 signing hash published: daf5a779ae972f972197303d7b574746c7ef83eadac0f2791ad23db92e4c8e53")
print("                      computed: " + keccak256(SIGNING).hex())
print("                         match:", keccak256(SIGNING).hex() == "daf5a779ae972f972197303d7b574746c7ef83eadac0f2791ad23db92e4c8e53")

f, _ = dec(SIGNED)
names = ["nonce","gasPrice","gasLimit","to","value","data","v","r","s"]
print("\nfields of the signed transaction (%d):" % len(f))
for n, v in zip(names, f):
    as_int = int.from_bytes(v, "big") if v else 0
    print(f"  {n:9} {len(v):>2} bytes  0x{v.hex() or '(empty)'}   = {as_int}")

print("\nchecks against the EIP's stated values:")
print("  nonce == 9                 :", int.from_bytes(f[0],'big') == 9)
print("  gasPrice == 20 gwei        :", int.from_bytes(f[1],'big') == 20 * 10**9)
print("  gasLimit == 21000          :", int.from_bytes(f[2],'big') == 21000)
print("  to == 0x3535...35          :", f[3].hex() == "35"*20)
print("  value == 1 ether           :", int.from_bytes(f[4],'big') == 10**18)
print("  data empty                 :", f[5] == b"")
print("  v == 37                    :", int.from_bytes(f[6],'big') == 37)
print("  r matches published decimal:", int.from_bytes(f[7],'big') == 18515461264373351373200002665853028612451056578545711640558177340181847433846)
print("  s matches published decimal:", int.from_bytes(f[8],'big') == 46948507304638947509940763649030358759909902576025900602547168820602576006531)
print("\n  transaction hash = keccak256(the signed bytes) = 0x" + keccak256(SIGNED).hex())
print("  total size on the wire:", len(SIGNED), "bytes")
