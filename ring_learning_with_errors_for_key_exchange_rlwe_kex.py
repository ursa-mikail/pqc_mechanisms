import numpy as np
from numpy.polynomial import polynomial as p

class RingLWE:
    def __init__(self, n=1024, q_bits=32):
        self.n = n
        self.q = 2**q_bits - 1
        self.poly_modulus = [1] + [0] * (n-1) + [1]  # x^n + 1
        
    def generate_polynomial(self):
        """Generate a random polynomial with normal distribution"""
        poly = np.floor(np.random.normal(0, size=self.n))
        poly = np.floor(p.polydiv(poly, self.poly_modulus)[1] % self.q)
        return poly.astype(int)
    
    def generate_public_polynomial(self):
        """Generate public polynomial A"""
        A = np.floor(np.random.random(size=self.n) * self.q) % self.q
        A = np.floor(p.polydiv(A, self.poly_modulus)[1])
        return A.astype(int)
    
    def compute_public_key(self, A, secret, error):
        """Compute public key: b = A * secret + error"""
        b = p.polymul(A, secret) % self.q
        b = np.floor(p.polydiv(b, self.poly_modulus)[1])
        b = p.polyadd(b, error) % self.q
        return b.astype(int)
    
    def compute_shared_secret(self, secret, public_key):
        """Compute shared secret: shared = secret * public_key"""
        shared = np.floor(p.polymul(secret, public_key) % self.q)
        shared = np.floor(p.polydiv(shared, self.poly_modulus)[1]) % self.q
        return shared.astype(int)
    
    def compute_rounding_helper(self, public_key):
        """Compute rounding helper u based on public key values"""
        u = np.zeros(self.n, dtype=int)
        
        for i in range(min(len(public_key), len(u))):
            val = public_key[i]
            if int(val / (self.q/4)) == 0:
                u[i] = 0
            elif int(val / (self.q/2)) == 0:
                u[i] = 1
            elif int(val / (3*self.q/4)) == 0:
                u[i] = 0
            elif int(val / self.q) == 0:
                u[i] = 1
            else:
                print(f"Warning: Unexpected value at index {i}")
                
        return u
    
    def error_correction(self, shared_secret, u):
        """Apply error correction using rounding helper u"""
        corrected = np.zeros(self.n, dtype=int)
        
        for i in range(len(shared_secret)):
            if u[i] == 0:  # Region 0
                if shared_secret[i] >= self.q * 0.125 and shared_secret[i] < self.q * 0.625:
                    corrected[i] = 1
                else:
                    corrected[i] = 0
            elif u[i] == 1:  # Region 1
                if shared_secret[i] >= self.q * 0.875 or shared_secret[i] < self.q * 0.375:
                    corrected[i] = 1
                else:
                    corrected[i] = 0
            else:
                print(f"Warning: Invalid u value at index {i}")
                
        return corrected

def main():
    # Initialize Ring-LWE with smaller parameters for demonstration
    rlwe = RingLWE(n=8, q_bits=8)
    
    print("=== Ring-LWE Key Exchange ===")
    print("=" * 50)
    
    # Generate public polynomial
    A = rlwe.generate_public_polynomial()
    print(f"Public polynomial A (length {len(A)}):")
    print(A)
    print()
    
    # Alice's keys
    print("--- Alice ---")
    sA = rlwe.generate_polynomial()
    eA = rlwe.generate_polynomial()
    bA = rlwe.compute_public_key(A, sA, eA)
    
    print(f"Secret sA: {sA}")
    print(f"Error eA:  {eA}")
    print(f"Public bA: {bA}")
    print()
    
    # Bob's keys
    print("--- Bob ---")
    sB = rlwe.generate_polynomial()
    eB = rlwe.generate_polynomial()
    bB = rlwe.compute_public_key(A, sB, eB)
    
    print(f"Secret sB: {sB}")
    print(f"Error eB:  {eB}")
    print(f"Public bB: {bB}")
    print()
    
    # Compute shared secrets
    print("--- Shared Secret Computation ---")
    shared_alice_raw = rlwe.compute_shared_secret(sA, bB)
    shared_bob_raw = rlwe.compute_shared_secret(sB, bA)
    
    print(f"Raw shared secret (Alice): {shared_alice_raw}")
    print(f"Raw shared secret (Bob):   {shared_bob_raw}")
    print()
    
    # Error correction
    print("--- Error Correction ---")
    u = rlwe.compute_rounding_helper(bB)
    print(f"Rounding helper u: {u}")
    
    shared_alice_final = rlwe.error_correction(shared_alice_raw, u)
    shared_bob_final = rlwe.error_correction(shared_bob_raw, u)
    
    print(f"Final shared (Alice): {shared_alice_final}")
    print(f"Final shared (Bob):   {shared_bob_final}")
    print()
    
    # Verification
    print("--- Verification ---")
    if np.array_equal(shared_alice_final, shared_bob_final):
        print("✓ SUCCESS: Shared secrets match!")
        print(f"Shared key: {shared_alice_final}")
    else:
        print("✗ FAILURE: Shared secrets don't match!")
        differences = np.where(shared_alice_final != shared_bob_final)[0]
        print(f"Differing indices: {differences}")

if __name__ == "__main__":
    main()

"""
=== Ring-LWE Key Exchange ===
==================================================
Public polynomial A (length 8):
[ 15 222  13 179  98 138 158  94]

--- Alice ---
Secret sA: [254   1 254   0   1 254 254 254]
Error eA:  [  0   1 253 253 253 253 254 254]
Public bA: [110  40 194 165 216 238   6 109]

--- Bob ---
Secret sB: [253 254   1   2 254 253 253 253]
Error eB:  [253 253 254 254   0   0 254 253]
Public bB: [ 44 102  56 252  82  83 212  72]

--- Shared Secret Computation ---
Raw shared secret (Alice): [169  66 207   7  15  89  26 107]
Raw shared secret (Bob):   [166  57 198   0  18  86  20 103]

--- Error Correction ---
Rounding helper u: [0 1 0 1 1 1 1 1]
Final shared (Alice): [0 1 0 1 1 1 1 0]
Final shared (Bob):   [0 1 0 1 1 1 1 0]

--- Verification ---
✓ SUCCESS: Shared secrets match!
Shared key: [0 1 0 1 1 1 1 0]

"""    