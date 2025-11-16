# Lattice-Based Digital Signature Scheme

A Python implementation of a lattice-based digital signature scheme inspired by Schnorr signatures and using the Fiat-Shamir transform. This implementation demonstrates both idealized (error-free) and realistic (Learning With Errors) versions.

## Overview

This project implements a post-quantum secure digital signature scheme based on lattice cryptography. Unlike traditional schemes (RSA, ECDSA) that are vulnerable to quantum computers, lattice-based signatures rely on the hardness of lattice problems like Learning With Errors (LWE), which are believed to be quantum-resistant.

## Features

- ✅ **Dual Implementation**: Both error-free and LWE-based versions
- ✅ **Post-Quantum Security**: Based on hard lattice problems
- ✅ **Schnorr-Style Protocol**: Uses commitment-challenge-response structure
- ✅ **Fiat-Shamir Transform**: Non-interactive via hash-based challenges
- ✅ **Rejection Sampling**: Prevents information leakage about secret key
- ✅ **Educational Focus**: Clear demonstrations and explanations

## Mathematical Foundation

### Without Errors (Idealized)

**Key Generation:**
- Generate random matrix **A** ∈ ℤ_q^(m×n)
- Sample secret vector **x** ∈ ℤ^n with small coefficients
- Compute public key **u** = **A**·**x** mod q

**Signing:**
1. **Commitment**: Sample random **y**, compute **v** = **A**·**y** mod q
2. **Challenge**: c = H(**v** || message) ∈ {-1, 1}
3. **Response**: **z** = c·**x** + **y**
4. **Output**: (**z**, **v**, c)

**Verification:**
- Check: **A**·**z** ≡ c·**u** + **v** (mod q)

### With Errors (Realistic/LWE-Based)

**Key Generation:**
- Generate random matrix **A** ∈ ℤ_q^(m×n)
- Sample secret vector **x** and error **e₁** with small coefficients
- Compute public key **u** = **A**·**x** + **e₁** mod q

**Signing:**
1. **Commitment**: Sample **y** and error **e₂**, compute **v** = **A**·**y** + **e₂** mod q
2. **Challenge**: c = H(**v** || message) ∈ {-1, 1}
3. **Response**: **z** = c·**x** + **y**
4. **Output**: (**z**, **v**, c)

**Verification:**
- Check: ||**A**·**z** - (c·**u** + **v**)|| ≤ threshold
- The difference equals -c·**e₁** - **e₂**, which is small

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd lattice-signature

# Install dependencies
pip install numpy
```

**Requirements:**
- Python 3.7+
- NumPy

## Usage

### Basic Example

```python
from lattice_signature import LatticeSignature

# Initialize signature scheme
sig_scheme = LatticeSignature(n=256, m=512, q=12289, sigma=8.0)

# Generate keys (with errors for real security)
A, u, x = sig_scheme.key_generation(use_errors=True)

# Sign a message
message = "Hello, Lattice Cryptography!"
signature = sig_scheme.sign(message)  # Returns (z, v, c)

# Verify signature
is_valid = sig_scheme.verify(message, signature, A, u)
print(f"Signature valid: {is_valid}")
```

### Running Demonstrations

```bash
python lattice_signature.py
```

This runs three demonstrations:
1. **Version 1**: Signature without errors (exact verification)
2. **Version 2**: Signature with errors (approximate verification)
3. **Explanation**: Detailed analysis of error impact and algebraic correctness

### Parameter Selection

```python
LatticeSignature(
    n=256,      # Dimension of secret vectors (security parameter)
    m=512,      # Number of equations (typically m ≈ 2n)
    q=12289,    # Modulus (prime, should be large enough)
    sigma=8.0   # Standard deviation for Gaussian sampling
)
```

**Security considerations:**
- Larger `n` → higher security but slower operations
- `m ≥ 2n` recommended for hardness
- `q` should be prime and sufficiently large
- `sigma` controls error size (trade-off between security and correctness)

## How It Works

### The Role of Errors

**Without Errors:**
- Pure algebraic verification: **A**·**z** = c·**u** + **v**
- Not secure against quantum computers
- Educational purposes only

**With Errors (LWE):**
- Approximate verification: **A**·**z** ≈ c·**u** + **v**
- Based on Learning With Errors problem
- Quantum-resistant security
- Requires tolerance threshold in verification

### Why Rejection Sampling?

When computing **z** = c·**x** + **y**, we must ensure **z** doesn't leak information about the secret key **x**. Rejection sampling ensures the distribution of **z** is independent of **x** by:

1. Sampling **y** from a wider distribution
2. Computing **z** = c·**x** + **y**
3. Only accepting if ||**z**|| ≤ bound
4. Repeating if rejected

### Verification with Errors

The verification difference is:
```
δ = A·z - (c·u + v)
  = A·(c·x + y) - (c·(A·x + e₁) + (A·y + e₂))
  = -c·e₁ - e₂
```

Since c ∈ {-1, 1} and e₁, e₂ are small, ||δ|| is bounded and verification succeeds with high probability.

## Security Properties

### Correctness
- **Perfect** (without errors): Verification always succeeds for valid signatures
- **Statistical** (with errors): Verification succeeds with probability ≈ 1 - 2^(-λ)

### Unforgeability
- Based on hardness of LWE problem
- Computationally infeasible to forge signatures without secret key
- Security reduction to worst-case lattice problems (GapSVP)

### Quantum Resistance
- LWE problem believed hard for quantum computers
- No known quantum algorithm provides exponential speedup
- Part of NIST post-quantum cryptography standardization

## Limitations & Future Work

### Current Limitations
1. **Simplified Parameters**: Uses smaller dimensions than production systems
2. **Binary Challenges**: c ∈ {-1, 1} instead of larger challenge space
3. **No Optimization**: Basic implementation without advanced optimizations
4. **Educational Focus**: Not audited for production use

### Potential Improvements
- Implement full BLISS, Dilithium, or Falcon signature schemes
- Add number-theoretic transforms (NTT) for faster polynomial multiplication
- Support larger challenge spaces for tighter security
- Implement advanced sampling techniques (discrete Gaussian)
- Add parameter sets for different security levels (128, 192, 256-bit)

## Related Standards

This implementation is inspired by:
- **BLISS**: Bimodal Lattice Signature Schemes
- **Dilithium**: NIST PQC finalist (selected for standardization)
- **Falcon**: NIST PQC finalist (selected for standardization)

For production use, consider NIST's standardized schemes.

## References

1. Lyubashevsky, V. (2012). "Lattice Signatures without Trapdoors"
2. Ducas, L. et al. (2018). "CRYSTALS-Dilithium: A Lattice-Based Digital Signature Scheme"
3. Fouque, P.A. et al. (2017). "Falcon: Fast-Fourier Lattice-based Compact Signatures over NTRU"
4. Regev, O. (2005). "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography"

