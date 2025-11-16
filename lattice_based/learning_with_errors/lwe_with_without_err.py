import numpy as np
import hashlib

class LatticeSignature:
    def __init__(self, n=256, m=512, q=12289, sigma=8.0):
        """
        Initialize lattice signature parameters
        
        Args:
            n: dimension of secret vectors
            m: number of equations (rows in A)
            q: modulus (prime for lattice crypto)
            sigma: standard deviation for Gaussian sampling
        """
        self.n = n
        self.m = m
        self.q = q
        self.sigma = sigma
        self.bound = int(100 * sigma)  # Bound for rejection sampling
        # Verification tolerance when using errors
        self.verify_bound = int(200 * sigma)  
        
    def key_generation(self, use_errors=True):
        """Generate public and private keys"""
        self.use_errors = use_errors
        
        # Random matrix A (public parameter)
        self.A = np.random.randint(0, self.q, (self.m, self.n))
        
        # Secret vector x (private key) - small coefficients
        self.x = self._sample_small_poly(self.n)
        
        if use_errors:
            # Error vector e1 - small coefficients
            self.e1 = self._sample_error_poly(self.m)
            # Public key u = A*x + e1 mod q
            self.u = np.mod(self.A @ self.x + self.e1, self.q)
        else:
            self.e1 = np.zeros(self.m)
            # Public key u = A*x mod q (no error)
            self.u = np.mod(self.A @ self.x, self.q)
        
        return self.A, self.u, self.x
    
    def sign(self, message):
        """
        Sign a message using lattice-based signature
        Based on Schnorr identification + Fiat-Shamir
        """
        max_attempts = 1000
        
        for attempt in range(max_attempts):
            # Step 1: Commitment
            # Sample random vector y with larger coefficients for masking
            y = self._sample_masking_poly(self.n)
            
            if self.use_errors:
                # Error vector e2 for commitment
                e2 = self._sample_error_poly(self.m)
                # Compute v = A*y + e2 mod q
                v = np.mod(self.A @ y + e2, self.q)
            else:
                e2 = np.zeros(self.m)
                # Compute v = A*y mod q (no error)
                v = np.mod(self.A @ y, self.q)
            
            # Step 2: Challenge via Fiat-Shamir
            # c = H(v || message) - small integer challenge
            c = self._hash_to_challenge(v, message)
            
            # Step 3: Response
            # z = c*x + y (NOT mod q initially)
            z = c * self.x + y
            
            # Step 4: Rejection sampling - ensure z doesn't leak x
            if self._is_within_bound(z):
                # Store e2 for verification if using errors
                if self.use_errors:
                    self.last_e2 = e2
                # Reduce z modulo q for transmission
                z_mod = np.mod(z, self.q)
                return (z_mod, v, c)
        
        raise ValueError("Failed to generate valid signature after multiple attempts")
    
    def verify(self, message, signature, A, u):
        """
        Verify a signature
        Without errors: Check A*z ≡ c*u + v (mod q) exactly
        With errors: Check ||A*z - (c*u + v)|| is small
        """
        z, v, c = signature
        
        # Recompute challenge from v and message
        c_verify = self._hash_to_challenge(v, message)
        
        # Check challenge matches
        if c != c_verify:
            return False
        
        # Compute both sides of verification equation
        left_side = np.mod(A @ z, self.q)
        right_side = np.mod(c * u + v, self.q)
        
        if self.use_errors:
            # WITH ERRORS: Check if difference is small
            # The difference should be approximately c*e1 + e2
            diff = np.mod(left_side - right_side + self.q//2, self.q) - self.q//2
            
            # Check if the difference is within expected error bounds
            # This accounts for c*e1 + e2
            is_valid = np.all(np.abs(diff) <= self.verify_bound)
            
            if not is_valid:
                max_diff = np.max(np.abs(diff))
                print(f"Verification with errors: max difference = {max_diff}, bound = {self.verify_bound}")
        else:
            # WITHOUT ERRORS: Check for exact equality
            is_valid = np.array_equal(left_side, right_side)
            
            if not is_valid:
                diff = np.mod(left_side - right_side, self.q)
                non_zero = np.count_nonzero(diff)
                if non_zero > 0:
                    print(f"Exact verification failed: {non_zero} non-zero differences")
        
        return is_valid
    
    def _sample_small_poly(self, size):
        """Sample polynomial with small coefficients for secret key"""
        # Coefficients in range [-sigma, sigma]
        return np.random.randint(-int(self.sigma), int(self.sigma)+1, size)
    
    def _sample_error_poly(self, size):
        """Sample error polynomial with very small coefficients"""
        # Errors should be smaller than secret
        error_range = max(1, int(self.sigma / 4))
        return np.random.randint(-error_range, error_range+1, size)
    
    def _sample_masking_poly(self, size):
        """Sample polynomial with larger coefficients for masking"""
        # Larger range for y to properly mask x
        masking_range = int(self.sigma * 10)
        return np.random.randint(-masking_range, masking_range+1, size)
    
    def _is_within_bound(self, vector):
        """Check if all coefficients are within rejection sampling bounds"""
        return np.all(np.abs(vector) <= self.bound)
    
    def _hash_to_challenge(self, v, message):
        """
        Hash v and message to create challenge
        Challenge must be small to keep z bounded
        """
        # Convert v to bytes for hashing
        v_bytes = v.tobytes()
        msg_bytes = message.encode() if isinstance(message, str) else message
        
        # Hash concatenation
        hash_input = v_bytes + msg_bytes
        hash_digest = hashlib.sha256(hash_input).digest()
        
        # Convert to small integer challenge (±1 for simplicity)
        challenge_bit = int.from_bytes(hash_digest[:1], 'big') % 2
        return 1 if challenge_bit == 0 else -1


def demo_both_versions():
    """Demonstrate both versions: with and without errors"""
    print("="*60)
    print("LATTICE-BASED SIGNATURES: WITH AND WITHOUT ERRORS")
    print("="*60)
    
    # Test WITHOUT errors first
    print("\n### VERSION 1: WITHOUT ERRORS (Exact Verification) ###\n")
    
    sig_scheme_no_error = LatticeSignature(n=128, m=256, q=12289, sigma=8.0)
    A, u, x = sig_scheme_no_error.key_generation(use_errors=False)
    
    message = "Hello, Lattice Cryptography!"
    print(f"Message: '{message}'")
    
    # Sign and verify
    z, v, c = sig_scheme_no_error.sign(message)
    is_valid = sig_scheme_no_error.verify(message, (z, v, c), A, u)
    print(f"Signature verification: {'✓ VALID' if is_valid else '✗ INVALID'}")
    
    # Mathematical check
    left = np.mod(A @ z, sig_scheme_no_error.q)
    right = np.mod(c * u + v, sig_scheme_no_error.q)
    print(f"A·z ≡ c·u + v (mod q): {np.array_equal(left, right)}")
    
    # Test tampering
    wrong_msg = "Tampered!"
    is_valid_tampered = sig_scheme_no_error.verify(wrong_msg, (z, v, c), A, u)
    print(f"Tampered message: {'✓ VALID' if is_valid_tampered else '✗ INVALID'}")
    
    # Test WITH errors
    print("\n### VERSION 2: WITH ERRORS (Approximate Verification) ###\n")
    
    sig_scheme_with_error = LatticeSignature(n=128, m=256, q=12289, sigma=8.0)
    A2, u2, x2 = sig_scheme_with_error.key_generation(use_errors=True)
    
    print(f"Message: '{message}'")
    print(f"Error e1 range: [{np.min(sig_scheme_with_error.e1)}, {np.max(sig_scheme_with_error.e1)}]")
    
    # Sign and verify
    z2, v2, c2 = sig_scheme_with_error.sign(message)
    print(f"Error e2 range: [{np.min(sig_scheme_with_error.last_e2)}, {np.max(sig_scheme_with_error.last_e2)}]")
    
    is_valid2 = sig_scheme_with_error.verify(message, (z2, v2, c2), A2, u2)
    print(f"Signature verification: {'✓ VALID' if is_valid2 else '✗ INVALID'}")
    
    # Show the approximation
    left2 = np.mod(A2 @ z2, sig_scheme_with_error.q)
    right2 = np.mod(c2 * u2 + v2, sig_scheme_with_error.q)
    diff = np.mod(left2 - right2 + sig_scheme_with_error.q//2, sig_scheme_with_error.q) - sig_scheme_with_error.q//2
    print(f"Verification difference stats:")
    print(f"  Max absolute difference: {np.max(np.abs(diff))}")
    print(f"  Verification bound: {sig_scheme_with_error.verify_bound}")
    print(f"  Within bound: {np.all(np.abs(diff) <= sig_scheme_with_error.verify_bound)}")
    
    # Test tampering
    is_valid_tampered2 = sig_scheme_with_error.verify(wrong_msg, (z2, v2, c2), A2, u2)
    print(f"Tampered message: {'✓ VALID' if is_valid_tampered2 else '✗ INVALID'}")


def explain_error_impact():
    """Explain the role of errors in the scheme"""
    print("\n" + "="*60)
    print("THE ROLE OF ERROR TERMS IN LATTICE SIGNATURES")
    print("="*60)
    
    print("\n### Why Include Errors? ###")
    print("1. SECURITY: Errors make the Learning With Errors (LWE) problem hard")
    print("2. QUANTUM RESISTANCE: LWE is believed quantum-resistant")
    print("3. WORST-CASE HARDNESS: LWE has worst-case to average-case reductions")
    
    print("\n### Mathematical Impact ###")
    print("WITHOUT errors:")
    print("  u = A·x (exactly)")
    print("  v = A·y (exactly)")
    print("  Verification: A·z ≡ c·u + v (mod q) [EXACT EQUALITY]")
    
    print("\nWITH errors:")
    print("  u = A·x + e1")
    print("  v = A·y + e2")
    print("  Verification: A·z ≈ c·u + v (mod q) [APPROXIMATE]")
    print("  Difference: A·z - (c·u + v) ≈ c·e1 + e2 (small)")
    
    print("\n### Verification Difference ###")
    print("The verification equation becomes:")
    print("  A·z = A·(c·x + y)")
    print("      = c·A·x + A·y")
    print("      = c·(u - e1) + (v - e2)")
    print("      = c·u + v - c·e1 - e2")
    print("\nSo: A·z - (c·u + v) = -c·e1 - e2")
    print("\nSince c ∈ {-1, 1} and e1, e2 are small,")
    print("the difference is bounded and predictable!")
    
    print("\n### Practical Considerations ###")
    print("• Errors must be small enough for verification to work")
    print("• Errors must be large enough to provide security")
    print("• Verification needs a tolerance threshold")
    print("• The threshold depends on error distributions and challenge size")


def analyze_algebraic_correctness():
    """Analyze the algebraic correctness with errors"""
    print("\n" + "="*60)
    print("ALGEBRAIC CORRECTNESS ANALYSIS")
    print("="*60)
    
    print("\n### Without Errors ###")
    print("Public: u = A·x")
    print("Commitment: v = A·y")
    print("Response: z = c·x + y")
    print("\nVerification:")
    print("  A·z = A·(c·x + y)")
    print("      = c·(A·x) + A·y")
    print("      = c·u + v ✓")
    
    print("\n### With Errors ###")
    print("Public: u = A·x + e1")
    print("Commitment: v = A·y + e2")
    print("Response: z = c·x + y")
    print("\nVerification:")
    print("  A·z = A·(c·x + y)")
    print("      = c·(A·x) + A·y")
    print("      = c·(u - e1) + (v - e2)")
    print("      = c·u + v - c·e1 - e2")
    print("\nDifference from expected:")
    print("  δ = A·z - (c·u + v) = -c·e1 - e2")
    print("\nSince |c| = 1 and e1, e2 are small:")
    print("  ||δ||∞ ≤ ||e1||∞ + ||e2||∞")


if __name__ == "__main__":
    # Run demonstrations
    demo_both_versions()
    explain_error_impact()
    analyze_algebraic_correctness()

"""
============================================================
LATTICE-BASED SIGNATURES: WITH AND WITHOUT ERRORS
============================================================

### VERSION 1: WITHOUT ERRORS (Exact Verification) ###

Message: 'Hello, Lattice Cryptography!'
Signature verification: ✓ VALID
A·z ≡ c·u + v (mod q): True
Tampered message: ✗ INVALID

### VERSION 2: WITH ERRORS (Approximate Verification) ###

Message: 'Hello, Lattice Cryptography!'
Error e1 range: [-2, 2]
Error e2 range: [-2, 2]
Signature verification: ✓ VALID
Verification difference stats:
  Max absolute difference: 4
  Verification bound: 1600
  Within bound: True
Tampered message: ✗ INVALID

============================================================
THE ROLE OF ERROR TERMS IN LATTICE SIGNATURES
============================================================

### Why Include Errors? ###
1. SECURITY: Errors make the Learning With Errors (LWE) problem hard
2. QUANTUM RESISTANCE: LWE is believed quantum-resistant
3. WORST-CASE HARDNESS: LWE has worst-case to average-case reductions

### Mathematical Impact ###
WITHOUT errors:
  u = A·x (exactly)
  v = A·y (exactly)
  Verification: A·z ≡ c·u + v (mod q) [EXACT EQUALITY]

WITH errors:
  u = A·x + e1
  v = A·y + e2
  Verification: A·z ≈ c·u + v (mod q) [APPROXIMATE]
  Difference: A·z - (c·u + v) ≈ c·e1 + e2 (small)

### Verification Difference ###
The verification equation becomes:
  A·z = A·(c·x + y)
      = c·A·x + A·y
      = c·(u - e1) + (v - e2)
      = c·u + v - c·e1 - e2

So: A·z - (c·u + v) = -c·e1 - e2

Since c ∈ {-1, 1} and e1, e2 are small,
the difference is bounded and predictable!

### Practical Considerations ###
• Errors must be small enough for verification to work
• Errors must be large enough to provide security
• Verification needs a tolerance threshold
• The threshold depends on error distributions and challenge size

============================================================
ALGEBRAIC CORRECTNESS ANALYSIS
============================================================

### Without Errors ###
Public: u = A·x
Commitment: v = A·y
Response: z = c·x + y

Verification:
  A·z = A·(c·x + y)
      = c·(A·x) + A·y
      = c·u + v ✓

### With Errors ###
Public: u = A·x + e1
Commitment: v = A·y + e2
Response: z = c·x + y

Verification:
  A·z = A·(c·x + y)
      = c·(A·x) + A·y
      = c·(u - e1) + (v - e2)
      = c·u + v - c·e1 - e2

Difference from expected:
  δ = A·z - (c·u + v) = -c·e1 - e2

Since |c| = 1 and e1, e2 are small:
  ||δ||∞ ≤ ||e1||∞ + ||e2||∞

"""