import numpy as np
import hashlib
import random

class LatticeSchnorr:
    """Simplified Lattice-based Schnorr Signature (ML-DSA concept)"""
    
    def __init__(self, dimension=128, modulus=2**15):
        self.n = dimension  # Vector dimension
        self.q = modulus    # Modulus
        self.A = self._generate_matrix()  # Public matrix
        
    def _generate_matrix(self):
        """Generate random public matrix A"""
        return np.random.randint(0, self.q, (self.n, self.n))
    
    def _hash_to_challenge(self, v, message):
        """Fiat-Shamir: Hash to create challenge"""
        data = v.tobytes() + message.encode()
        hash_bytes = hashlib.sha256(data).digest()
        # Convert to integer in range [0, q-1]
        return int.from_bytes(hash_bytes, 'little') % self.q
    
    def _small_random_vector(self):
        """Generate small random vector (for secrets and errors)"""
        return np.random.randint(-10, 11, self.n)  # Small coefficients
    
    def key_generation(self):
        """Generate lattice key pair"""
        # Private key: small secret vector
        self.x = self._small_random_vector()
        # Small error term - THIS WILL BE REMOVED FOR DEMO
        self.e1 = self._small_random_vector()
        print(f"🔐 ERROR TERM e1 (will be removed for demo): {self.e1[:5]}...")  # Show first 5 elements
        
        # Public key: u = A*x + e
        self.u_with_error = (self.A @ self.x + self.e1) % self.q
        # For demo: remove error to ensure equality
        self.u_no_error = (self.A @ self.x) % self.q
        return self.x, self.u_no_error
    
    def sign(self, message):
        """Create lattice-based signature using Fiat-Shamir"""
        # Step 1: Commit with randomness
        y = self._small_random_vector()
        # Small error term - THIS WILL BE REMOVED FOR DEMO
        self.e2 = self._small_random_vector()
        print(f"🔐 ERROR TERM e2 (will be removed for demo): {self.e2[:5]}...")  # Show first 5 elements
        
        v_with_error = (self.A @ y + self.e2) % self.q
        # For demo: remove error to ensure equality
        v_no_error = (self.A @ y) % self.q
        
        # Step 2: Fiat-Shamir challenge (non-interactive)
        c = self._hash_to_challenge(v_no_error, message)
        
        # Step 3: Response using secret
        z = (c * self.x + y) % self.q
        
        return (v_no_error, z), c
    
    def verify(self, message, signature, u):
        """Verify lattice-based signature"""
        v, z = signature
        
        # Recompute challenge
        c = self._hash_to_challenge(v, message)
        
        # Verify: A*z should equal c*u + v
        left_side = (self.A @ z) % self.q
        right_side = (c * u + v) % self.q
        
        print(f"🔍 VERIFICATION DETAILS:")
        print(f"   A·z = {left_side[:3]}...")  # Show first 3 elements
        print(f"   c·u + v = {right_side[:3]}...")
        print(f"   Vectors equal: {np.array_equal(left_side, right_side)}")
        
        return np.array_equal(left_side, right_side)

class TraditionalSchnorr:
    """Traditional Schnorr Signature (for comparison)"""
    
    def __init__(self):
        self.p = 2**255 - 19  # Large prime
        self.g = 3            # Generator
    
    def key_generation(self):
        """Generate traditional key pair"""
        self.x = random.randint(1, 2**32)  # Private key
        y = pow(self.g, self.x, self.p)    # Public key
        return self.x, y
    
    def sign(self, message):
        """Create traditional Schnorr signature"""
        # Step 1: Commit with randomness
        v = random.randint(1, 2**32)
        t = pow(self.g, v, self.p)
        
        # Step 2: Fiat-Shamir challenge
        challenge_input = f"{self.g},{t},{message}".encode()
        c = int(hashlib.sha256(challenge_input).hexdigest(), 16) % 2**32
        
        # Step 3: Response using secret
        r = (v - c * self.x) % (self.p - 1)
        
        return (t, r), c
    
    def verify(self, message, signature, y):
        """Verify traditional Schnorr signature"""
        t, r = signature
        
        # Recompute challenge
        challenge_input = f"{self.g},{t},{message}".encode()
        c = int(hashlib.sha256(challenge_input).hexdigest(), 16) % 2**32
        
        # Verify: g^r * y^c should equal t
        left_side = (pow(self.g, r, self.p) * pow(y, c, self.p)) % self.p
        
        print(f"🔍 VERIFICATION DETAILS:")
        print(f"   g^r · y^c = {left_side}")
        print(f"   t = {t}")
        
        return left_side == t

def demo():
    print("=== LATTICE-BASED SCHNORR (ML-DSA Concept) ===\n")
    
    # Lattice version
    lattice = LatticeSchnorr(dimension=128)  # Smaller for demo
    priv_lattice, pub_lattice = lattice.key_generation()
    
    message = "Hello ML-DSA!"
    print(f"\n📝 SIGNING PROCESS:")
    signature, challenge = lattice.sign(message)
    print(f"\n✅ VERIFICATION PROCESS:")
    valid = lattice.verify(message, signature, pub_lattice)
    
    print(f"\n📊 SUMMARY:")
    print(f"Message: {message}")
    print(f"Private key (x): vector of {len(priv_lattice)} small integers")
    print(f"Public key (u): vector of {len(pub_lattice)} elements")
    print(f"Signature (v,z): two vectors")
    print(f"Challenge (c): {challenge}")
    print(f"Signature valid: {valid}")
    
    print("\n" + "="*60 + "\n")
    
    print("=== TRADITIONAL SCHNORR (For Comparison) ===\n")
    
    # Traditional version
    traditional = TraditionalSchnorr()
    priv_trad, pub_trad = traditional.key_generation()
    
    print(f"📝 SIGNING PROCESS:")
    signature_trad, challenge_trad = traditional.sign(message)
    print(f"\n✅ VERIFICATION PROCESS:")
    valid_trad = traditional.verify(message, signature_trad, pub_trad)
    
    print(f"\n📊 SUMMARY:")
    print(f"Message: {message}")
    print(f"Private key (x): {priv_trad}")
    print(f"Public key (y): {pub_trad}")
    print(f"Signature (t,r): ({signature_trad[0]}, {signature_trad[1]})")
    print(f"Challenge (c): {challenge_trad}")
    print(f"Signature valid: {valid_trad}")
    
    print("\n" + "="*60 + "\n")
    print("🔬 KEY INSIGHTS:")
    print("1. Both use same 3-step pattern: Commit → Challenge → Respond")
    print("2. Both use Fiat-Shamir to make it non-interactive")
    print("3. Lattice uses matrix/vector math, Traditional uses modular exponentiation")
    print("4. Lattice is quantum-resistant, Traditional is vulnerable to quantum attacks")
    print("5. ⚠️ In real ML-DSA, small errors (e1, e2) provide security but make verification approximate")
    print("6. 🎯 For this demo, errors are REMOVED to ensure exact equality in verification")

if __name__ == "__main__":
    demo()

"""
=== LATTICE-BASED SCHNORR (ML-DSA Concept) ===

🔐 ERROR TERM e1 (will be removed for demo): [ 9 -7 -7 -4  0]...

📝 SIGNING PROCESS:
🔐 ERROR TERM e2 (will be removed for demo): [-1 -4  8  4  6]...

✅ VERIFICATION PROCESS:
🔍 VERIFICATION DETAILS:
   A·z = [13030 32089  1960]...
   c·u + v = [13030 32089  1960]...
   Vectors equal: True

📊 SUMMARY:
Message: Hello ML-DSA!
Private key (x): vector of 128 small integers
Public key (u): vector of 128 elements
Signature (v,z): two vectors
Challenge (c): 28394
Signature valid: True

============================================================

=== TRADITIONAL SCHNORR (For Comparison) ===

📝 SIGNING PROCESS:

✅ VERIFICATION PROCESS:
🔍 VERIFICATION DETAILS:
   g^r · y^c = 13645615257892856105951411280373596189198771210871131172618690299390931652762
   t = 13645615257892856105951411280373596189198771210871131172618690299390931652762

📊 SUMMARY:
Message: Hello ML-DSA!
Private key (x): 1934818262
Public key (y): 56625263960990518290225653917631768478592191425712791345321846390596332105826
Signature (t,r): (13645615257892856105951411280373596189198771210871131172618690299390931652762, 57896044618658097711785492504343953926634992332820282019724152442938694664280)
Challenge (c): 2397931170
Signature valid: True

============================================================

🔬 KEY INSIGHTS:
1. Both use same 3-step pattern: Commit → Challenge → Respond
2. Both use Fiat-Shamir to make it non-interactive
3. Lattice uses matrix/vector math, Traditional uses modular exponentiation
4. Lattice is quantum-resistant, Traditional is vulnerable to quantum attacks
5. ⚠️ In real ML-DSA, small errors (e1, e2) provide security but make verification approximate
6. 🎯 For this demo, errors are REMOVED to ensure exact equality in verification

"""    