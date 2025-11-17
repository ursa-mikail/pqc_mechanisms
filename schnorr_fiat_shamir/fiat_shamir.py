import sys
import random
import hashlib

# Cryptographic parameters
n = 2**255 - 19  # Large prime modulus
g = 3            # Generator

def interactive_proof():
    """Interactive Zero-Knowledge Proof (The Conversation)"""
    print("=== INTERACTIVE PROOF ===")
    print("Alice proves she knows x to Bob through dialogue\n")
    
    # Alice's secret
    x = random.randint(1, 2**80)
    y = pow(g, x, n)  # Public key: y = g^x mod n
    
    # Step 1: Alice commits
    v = random.randint(1, 2**80)
    t = pow(g, v, n)  # Commitment: t = g^v mod n
    print(f"Alice → Bob: t = {t}")
    
    # Step 2: Bob challenges  
    c = random.randint(1, 2**80)  # Bob's random challenge
    print(f"Bob → Alice: c = {c}")
    
    # Step 3: Alice responds
    r = v - c * x  # Response using her secret
    print(f"Alice → Bob: r = {r}")
    
    # Step 4: Bob verifies
    verification = (pow(g, r, n) * pow(y, c, n)) % n
    print(f"\nBob verifies: g^r * y^c = {verification}")
    print(f"Original t   = {t}")
    
    if t == verification:
        print("✅ Alice proved she knows x!")
    else:
        print("❌ Proof failed!")
    
    return t == verification

def non_interactive_proof():
    """Non-Interactive Proof (The Self-Solved Puzzle)"""
    print("\n=== NON-INTERACTIVE PROOF ===")
    print("Alice creates proof without talking to Bob\n")
    
    # Alice's secret
    x = random.randint(1, 2**80)
    y = pow(g, x, n)  # Public key: y = g^x mod n
    
    # Step 1: Alice commits
    v = random.randint(1, 2**80)
    t = pow(g, v, n)  # Commitment: t = g^v mod n
    
    # Step 2: Alice creates her own challenge using hash
    challenge_input = f"{g},{y},{t}".encode()
    c = int(hashlib.sha256(challenge_input).hexdigest(), 16) % 2**80
    print(f"Alice computes: c = Hash(g, y, t) = {c}")
    
    # Step 3: Alice computes response
    r = v - c * x
    
    # The proof is complete! Send [t, r] to anyone
    print(f"Alice's proof: t = {t}, r = {r}")
    
    # Anyone can verify
    verification = (pow(g, r, n) * pow(y, c, n)) % n
    print(f"\nVerifier checks: g^r * y^c = {verification}")
    print(f"Original t     = {t}")
    
    if t == verification:
        print("✅ Proof valid! Alice knows x.")
    else:
        print("❌ Proof invalid!")
    
    return t == verification

if __name__ == "__main__":
    print("INTERACTIVE VERSION")
    print("(Requires Bob to send challenge 'c')\n")
    
    # Run both versions
    interactive_proof()
    non_interactive_proof()

"""
Key Differences:
[INTERACTIVE Version]

Bob sends random challenge c

Requires back-and-forth communication

Like a live conversation

[NON-INTERACTIVE Version]

Alice generates her own challenge using cryptographic hash

No communication needed during proof generation

Like writing a solution that anyone can verify later

INTERACTIVE VERSION
(Requires Bob to send challenge 'c')

=== INTERACTIVE PROOF ===
Alice proves she knows x to Bob through dialogue

Alice → Bob: t = 57692946612241147306790196061577132776749507377262778243029737098129158042833
Bob → Alice: c = 368235625807185490778724
Alice → Bob: r = -294910310569125327433684829414129850276787599823

Bob verifies: g^r * y^c = 57692946612241147306790196061577132776749507377262778243029737098129158042833
Original t   = 57692946612241147306790196061577132776749507377262778243029737098129158042833
✅ Alice proved she knows x!

=== NON-INTERACTIVE PROOF ===
Alice creates proof without talking to Bob

Alice computes: c = Hash(g, y, t) = 791306850740259432635277
Alice's proof: t = 36058813526721644318083766015034227727389480741987983366077392477817482128749, r = -631090928142419267017638801426070423781491802102

Verifier checks: g^r * y^c = 36058813526721644318083766015034227727389480741987983366077392477817482128749
Original t     = 36058813526721644318083766015034227727389480741987983366077392477817482128749
✅ Proof valid! Alice knows x.
"""