# Schnorr-Fiat-Shamir 

## Core Concept
The method for creating the lattice-based signatures is actually based on the Schnorr signature method for proof of identity (a Zero Knowledge Proof) and then applies the Fiat-Shamir method to make it non-interactive. It’s a NI-ZKP (Non-interactive Zero Knowledge Proof) of a secret (a person’s private key).

**No trapdoors needed!** Modern lattice-based signatures (like ML-DSA) use **Zero Knowledge Proofs** to prove you know a secret without revealing it.

## How It Works - The Interactive Version

### Setup
- **Private Key**: A secret vector `x`
- **Public Key**: `u = A·x` (where `A` is a public matrix)

### The "Proof of Identity" Dance
1. **Bob's Commitment**: 
   - Creates random vector `y`
   - Sends `v = A·y` to Alice

2. **Alice's Challenge**:
   - Sends random number `c` to Bob

3. **Bob's Response**:
   - Computes `z = c·x + y`
   - Sends `z` to Alice

4. **Alice Verifies**:
   - Checks if `A·z = c·u + v`
   - If equal → Bob proves he knows `x` without revealing it!

## Making It Non-Interactive (Fiat-Shamir)

Instead of waiting for Alice's challenge:
- **Bob generates his own challenge**: `c = H(v || Message)`
- **Signature** = `(v, z)`

### Verification
Anyone can:
1. Recompute `c = H(v || Message)`
2. Check `A·z = c·u + v`

## Why This Matters
- **Quantum-resistant**: Based on hard lattice problems
- **Efficient**: Small signatures, fast verification
- **Secure**: Proves knowledge without revealing the secret

**Bottom line**: You prove you know a secret by answering a challenge that only someone with the secret could answer correctly.


# Interactive vs Non-Interactive Zero-Knowledge Proofs

## Interactive Proof (The "Conversation")
**Like a teacher-student dialogue:**
1. **Commitment**: Prover sends `t = g^v mod P` (hides secret `x`)
2. **Challenge**: Verifier sends random `c` 
3. **Response**: Prover sends `r = v - c·x`
4. **Verification**: Check if `t = g^r · y^c mod P`

**Requires back-and-forth interaction between prover and verifier.**

## Non-Interactive Proof (The "Self-Solved Puzzle")  
**Like submitting a completed exam:**
1. **Setup**: Same secret `x`, public `y = g^x`
2. **Commitment**: Prover computes `t = g^v`
3. **Self-Challenge**: Prover calculates `c = Hash(g + y + t)` (creates own challenge)
4. **Self-Response**: Prover computes `r = v - c·x`
5. **Proof**: Sends `[t, r]` as complete proof

**Verifier can independently:**
- Recompute `c = Hash(g + y + t)`
- Verify `t = g^r · y^c`

## Key Difference
- **Interactive**: Requires live challenge-response (like an oral exam)
- **Non-Interactive**: Prover generates everything at once (like a written exam)
- **Fiat-Shamir**: Converts interactive → non-interactive using cryptographic hash as "virtual verifier"

# Interactive vs Non-Interactive Zero-Knowledge Proofs

## Interactive Proof (The "Conversation")
**Like a teacher-student dialogue:**
1. **Commitment**: Prover sends `t = g^v mod P` (hides secret `x`)
2. **Challenge**: Verifier sends random `c` 
3. **Response**: Prover sends `r = v - c·x`
4. **Verification**: Check if `t = g^r · y^c mod P`

**Requires back-and-forth interaction between prover and verifier.**

## Non-Interactive Proof (The "Self-Solved Puzzle")  
**Like submitting a completed exam:**
1. **Setup**: Same secret `x`, public `y = g^x`
2. **Commitment**: Prover computes `t = g^v`
3. **Self-Challenge**: Prover calculates `c = Hash(g + y + t)` (creates own challenge)
4. **Self-Response**: Prover computes `r = v - c·x`
5. **Proof**: Sends `[t, r]` as complete proof

**Verifier can independently:**
- Recompute `c = Hash(g + y + t)`
- Verify `t = g^r · y^c`

## Key Difference
- **Interactive**: Requires live challenge-response (like an oral exam)
- **Non-Interactive**: Prover generates everything at once (like a written exam)
- **Fiat-Shamir**: Converts interactive → non-interactive using cryptographic hash as "virtual verifier"

![fiat-shamir](fiat-shamir.png)
