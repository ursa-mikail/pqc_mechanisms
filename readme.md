# Post-Quantum Cryptography: Main Categories

## Overview
Post-quantum cryptography (PQC) aims to develop cryptographic systems secure against quantum computer attacks. NIST has standardized several approaches across four main categories.

## 1. Lattice-Based Cryptography

### Core Principle
Security based on the hardness of lattice problems like **Learning With Errors (LWE)** and **Shortest Vector Problem (SVP)**.

### Key Algorithms

#### 🔐 Public-Key Encryption & KEMs
- **CRYSTALS-KYBER**: Uses LWE with lattice methods
  - *Status*: NIST Standard (KEM)
  - *Features*: Excellent performance, good key sizes
  - *Considerations*: Requires side-channel protection

- **NTRU**: Traditional structured lattice approach
  - *Status*: NIST Standard (KEM)
  - *Features*: Long history (≈25 years), well-studied
  - *Advantages*: Proven robustness, IP clarity

- **SABER**: Based on modular learning with rounding
  - *Status*: Alternative candidate
  - *Features*: Excellent performance, production-ready
  - *Focus*: Side-channel attack resilience

#### ✍️ Digital Signatures
- **CRYSTALS-DILITHIUM (ML-DSA)**: Lattice-based Fiat-Shamir
  - *Status*: NIST Standard (Signature)
  - *Features*: Small signatures, efficient verification
  - *Method*: Zero-knowledge proofs with Fiat-Shamir transform

- **FALCON**: Based on NTRU with GPV framework
  - *Status*: NIST Standard (Signature)
  - *Features*: Very small signatures
  - *Method*: Uses trapdoor sampling with FFT

### Security Basis
- **LWE Problem**: Solve noisy linear equations
- **SVP**: Find shortest non-zero vector in lattice
- **Quantum Resistance**: Believed secure against quantum attacks

## 2. Hash-Based Cryptography

### Core Principle
Security based solely on cryptographic hash functions.

### Key Algorithms

#### ✍️ Digital Signatures
- **SPHINCS+ (SLH-DSA)**: Stateless hash-based signatures
  - *Status*: NIST Standard (Signature)
  - *Features*: Conservative security, hash-based only
  - *Method*: Merkle trees of few-time signatures

### How It Works
1. **WOTS+ (Winternitz OTS)**: Few-time signature scheme
2. **Merkle Trees**: Combine many OTS keys into single root
3. **Hyper-tree**: Enable multiple signatures without state

### Security Basis
- **Hash Function Security**: Relies on preimage/resistance
- **Quantum Resistance**: Hash functions remain secure
- **Conservative**: Minimal cryptographic assumptions

## 3. Code-Based Cryptography

### Core Principle
Security based on error-correcting code problems.

### Key Algorithms

#### 🔐 Public-Key Encryption
- **Classic McEliece**: Based on Goppa codes
  - *Status*: NIST Standard (KEM)
  - *Features*: 40+ year history, well-studied
  - *Trade-offs*: Large public keys, small ciphertext

### Security Basis
- **Decoding Problem**: Hard to decode random linear codes
- **Quantum Resistance**: No efficient quantum algorithms known
- **Mature**: Decades of cryptanalysis

## 4. Multivariate Polynomial Cryptography

### Core Principle
Security based on solving systems of multivariate polynomial equations.

### Key Algorithms

#### ✍️ Digital Signatures
- **Rainbow**: Oil and Vinegar signature scheme
  - *Status*: Alternative candidate (Round 3, not selected)
  - *Method*: Multivariate quadratic equations
  - *Concept*: Trapdoor for solving n variables with m equations

### Security Basis
- **MQ Problem**: Solve multivariate quadratic systems
- **Trapdoor Design**: Easy with secret, hard without
- **Efficiency**: Fast verification, larger keys

## NIST Standardization Status

### 🏆 Selected Standards (2022)

#### Key Encapsulation Mechanisms (KEMs)
1. **CRYSTALS-KYBER** (Lattice-based)
2. **Classic McEliece** (Code-based)
3. **NTRU** (Lattice-based)
4. **SABER** (Lattice-based) - Alternative

#### Digital Signatures
1. **CRYSTALS-DILITHIUM** (Lattice-based)
2. **FALCON** (Lattice-based)
3. **SPHINCS+** (Hash-based)

## Comparative Analysis

| Category | Security Basis | Key Sizes | Performance | Maturity |
|----------|---------------|-----------|-------------|----------|
| **Lattice** | LWE/SVP Problems | Medium | Fast | High |
| **Hash-Based** | Hash Functions | Small | Slow | Very High |
| **Code-Based** | Decoding Problems | Large Keys | Fast | Very High |
| **Multivariate** | MQ Problems | Large | Fast Sign | Medium |

## Deployment Recommendations

### General Purpose
- **KEM**: CRYSTALS-KYBER (balance of security/performance)
- **Signatures**: CRYSTALS-DILITHIUM (efficient, well-studied)

### High Security
- **KEM**: Classic McEliece (conservative choice)
- **Signatures**: SPHINCS+ (minimal assumptions)

### Performance Critical
- **KEM**: SABER or NTRU
- **Signatures**: FALCON (smallest signatures)

## Future Directions

1. **Hybrid Approaches**: Combine classical + PQC
2. **Parameter Updates**: Respond to new cryptanalysis
3. **Hardware Optimization**: Efficient implementations
4. **Protocol Integration**: TLS, SSH, VPN adoption

## NIST Standardization Status

### 🏆 Final Standards (2024)

#### Key Encapsulation Mechanisms (KEMs)
**Primary:**
- **CRYSTALS-KYBER** (Lattice-based) - **FIPS 203** (ML-KEM)

**Alternates:**
- **Classic McEliece** (Code-based)
- **NTRU** (Lattice-based) 

*Note: SABER was not selected for standardization*

#### Digital Signatures
**Primary:**
- **CRYSTALS-DILITHIUM** (Lattice-based) - **FIPS 204** (ML-DSA)
- **FALCON** (Lattice-based) - **FIPS 205**

**Additional:**
- **SPHINCS+** (Hash-based) - **FIPS 205**

### 📋 Current Status (2024)

| Algorithm | Type | Standard | Status |
|-----------|------|----------|---------|
| **CRYSTALS-KYBER** | KEM | FIPS 203 | **Final Standard** |
| **CRYSTALS-DILITHIUM** | Signature | FIPS 204 | **Final Standard** |
| **FALCON** | Signature | FIPS 205 | **Final Standard** |
| **SPHINCS+** | Signature | FIPS 205 | **Final Standard** |
| **Classic McEliece** | KEM | - | Alternate |
| **NTRU** | KEM | - | Alternate |

### 🔄 Updates from Original Timeline

**Key Changes:**
- **SABER** was not selected for standardization
- **KYBER** renamed to **ML-KEM** in FIPS 203
- **DILITHIUM** renamed to **ML-DSA** in FIPS 204  
- **SPHINCS+** renamed to **SLH-DSA** in FIPS 205
- All standards now have official FIPS numbers

### 🚀 Deployment Status

**Early Adoption (2023-2024):**
- Cloudflare, Google, Amazon implementing PQC
- Chrome, Firefox testing PQC in TLS
- VPN providers adding PQC support
- Government agencies planning migration

**Expected Timeline:**
- 2024-2025: Widespread testing and hybrid deployment
- 2026-2028: Gradual transition to PQC-only
- 2030+: Target for complete migration


## References

- NIST PQC Standardization Process
- CRYSTALS Suite (KYBER + DILITHIUM)
- SPHINCS+ Framework
- Classic McEliece Cryptosystem

# Moving Beyond Trapdoors
The Old Way (Trapdoors): Methods like RSA rely on a mathematical "trapdoor." It's easy to compute in one direction (encryption) but very hard to reverse (decryption) unless you know a secret (the trapdoor). The risk is that someone might find a way to "pick the lock" (e.g., with a powerful quantum computer).

The New Way (Post-Quantum): New algorithms are based on mathematical problems believed to be hard even for quantum computers. They don't use trapdoors.
