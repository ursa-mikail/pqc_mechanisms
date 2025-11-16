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

import numpy as np
from numpy.polynomial import polynomial as p

class SimpleRingLWE:
    def __init__(self, n=8, q_bits=8):  # Smaller for demo
        self.n = n
        self.q = 2**q_bits - 1
        self.poly_mod = [1] + [0] * (n-1) + [1]  # x^n + 1
    
    def random_poly(self):
        """Generate random polynomial"""
        poly = np.random.normal(0, 1, self.n).astype(int)
        return np.floor(p.polydiv(poly, self.poly_mod)[1] % self.q).astype(int)
    
    def compute_public_key(self, A, secret, error):
        """Compute public key: b = A*secret + error"""
        b = p.polymul(A, secret) % self.q
        b = np.floor(p.polydiv(b, self.poly_mod)[1])
        return (b + error) % self.q
    
    def compute_shared(self, secret, public_key):
        """Compute shared secret"""
        shared = p.polymul(secret, public_key) % self.q
        return np.floor(p.polydiv(shared, self.poly_mod)[1] % self.q).astype(int)
    
    def reconciliation(self, shared, public_key):
        """Error correction to get final shared bits with region info"""
        bits = np.zeros(self.n, dtype=int)
        regions = []
        
        for i in range(min(len(shared), len(bits))):
            # Determine region from public key value
            val = public_key[i]
            
            if val < self.q/4:
                region = 0  # Region 0: [0, q/4)
            elif val < self.q/2:
                region = 1  # Region 1: [q/4, q/2)
            elif val < 3*self.q/4:
                region = 0  # Region 0: [q/2, 3q/4)
            else:
                region = 1  # Region 1: [3q/4, q)
            
            regions.append(region)
            
            # Convert to bit based on region and shared value
            if region == 0:
                # Region 0: bit=1 if shared in [q/8, 5q/8)
                bits[i] = 1 if (self.q/8 <= shared[i] < 5*self.q/8) else 0
            else:  # region == 1
                # Region 1: bit=1 if shared in [0, 3q/8) OR [7q/8, q)
                bits[i] = 1 if (shared[i] < 3*self.q/8 or shared[i] >= 7*self.q/8) else 0
                
        return bits, regions

# Initialize with small parameters
rlwe = SimpleRingLWE(n=8, q_bits=8)

print("=== Simplified Ring-LWE Key Exchange ===\n")
print(f"Modulus q = {rlwe.q}")
print(f"Regions: 0=[0,{rlwe.q/4}) U [{rlwe.q/2},{3*rlwe.q/4})")
print(f"         1=[{rlwe.q/4},{rlwe.q/2}) U [{3*rlwe.q/4},{rlwe.q})")
print()

# Generate public parameter
A = np.floor(np.random.random(rlwe.n) * rlwe.q) % rlwe.q
A = np.floor(p.polydiv(A, rlwe.poly_mod)[1]).astype(int)

print(f"Public A: {A}\n")

# Alice generates keys
sA = rlwe.random_poly()
eA = rlwe.random_poly() 
bA = rlwe.compute_public_key(A, sA, eA)

print("Alice:")
print(f"  Secret: {sA}")
print(f"  Public: {bA}\n")

# Bob generates keys
sB = rlwe.random_poly()
eB = rlwe.random_poly()
bB = rlwe.compute_public_key(A, sB, eB)

print("Bob:")
print(f"  Secret: {sB}")
print(f"  Public: {bB}\n")

# Compute shared secrets
shared_A = rlwe.compute_shared(sA, bB)
shared_B = rlwe.compute_shared(sB, bA)

print(f"Raw Shared (Alice): {shared_A}")
print(f"Raw Shared (Bob):   {shared_B}\n")

# Apply reconciliation with region info
final_A, regions_A = rlwe.reconciliation(shared_A, bB)
final_B, regions_B = rlwe.reconciliation(shared_B, bA)

print("Reconciliation Details:")
print(f"Bob's public values: {bB}")
print(f"Regions for Alice:   {regions_A}")
print(f"Regions for Bob:     {regions_B}")
print()

print(f"Final Key (Alice): {final_A}")
print(f"Final Key (Bob):   {final_B}\n")

# Verify
if np.array_equal(final_A, final_B):
    print("✅ SUCCESS: Keys match!")
    print(f"Shared Key: {final_A}")
else:
    mismatches = np.sum(final_A != final_B)
    print(f"❌ Keys differ at {mismatches} positions")

"""
=== Simplified Ring-LWE Key Exchange ===

Modulus q = 255
Regions: 0=[0,63.75) U [127.5,191.25)
         1=[63.75,127.5) U [191.25,255)

Public A: [250  76  77  95  87  33  29  90]

Alice:
  Secret: [0 0 0 0 0 1 0 1]
  Public: [ 84.  91. 127. 138. 132. 221. 241.  73.]

Bob:
  Secret: [  0   0   1   0 254   0   0   1]
  Public: [235. 119. 182.  77.  47. 243. 173. 186.]

Raw Shared (Alice): [ 59  26 190  35  81  62 188 162]
Raw Shared (Bob):   [ 55  21 187  32  77  61 187 167]

Reconciliation Details:
Bob's public values: [235. 119. 182.  77.  47. 243. 173. 186.]
Regions for Alice:   [1, 1, 0, 1, 0, 1, 0, 0]
Regions for Bob:     [1, 1, 1, 0, 0, 1, 1, 1]

Final Key (Alice): [1 1 0 1 1 1 0 0]
Final Key (Bob):   [1 1 0 1 1 1 0 0]

✅ SUCCESS: Keys match!
Shared Key: [1 1 0 1 1 1 0 0]


"""
