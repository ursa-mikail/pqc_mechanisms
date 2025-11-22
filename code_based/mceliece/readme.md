# McEliece Cryptosystem Implementation
## Overview
The McEliece cryptosystem is a public-key encryption scheme based on error-correcting codes. This implementation uses a (7,4) Hamming code that can correct one error in 7-bit codewords.

Mathematical Foundation
```
Key Generation
The system uses 3 matrices:

G: Generator matrix of the error-correcting code

S: Scrambler matrix (invertible)

P: Permutation matrix

The public key is derived as: G' = S·G·P mod 2
```

## Encryption Process
```
Ciphertext = Message × G' + Error

text
c = m × G' + e
```

## Decryption Process
```
Remove permutation: y' = c × P⁻¹

Error correction: Correct errors using the underlying code

Remove scrambler: m = corrected × G⁻¹ × S⁻¹
```

## Step-by-Step Example

```
Step 1: Key Generation
Generator Matrix G (7,4 Hamming Code):

text
[1 0 0 0 1 1 0]
[0 1 0 0 1 0 1]
[0 0 1 0 0 1 1]
[0 0 0 1 1 1 1]


Scrambler Matrix S:

text
[1 1 0 1]
[1 0 0 1]
[0 1 1 1]
[1 1 0 0]


Permutation Matrix P:

text
[0 1 0 0 0 0 0]
[0 0 0 1 0 0 0]
[0 0 0 0 0 0 1]
[1 0 0 0 0 0 0]
[0 0 1 0 0 0 0]
[0 0 0 0 0 1 0]
[0 0 0 0 1 0 0]


Public Key G' = S·G·P:

text
[1 1 1 1 0 0 0]
[1 1 0 0 1 0 0]
[1 0 0 1 1 0 1]
[0 1 0 1 1 1 0]
```

```
Step 2: Encryption
Message: m = [1, 1, 0, 1]

Compute m × G':
[1, 1, 0, 1] × G' = [1, 0, 1, 1, 0, 1, 0]

Add Error Vector: e = [0, 0, 0, 0, 1, 0, 0]

Ciphertext: c = m × G' + e = [1, 0, 1, 1, 1, 1, 0]
```

```
Step 3: Decryption
Remove Permutation: y' = c × P⁻¹ = [0, 1, 1, 1, 1, 1, 0]

Error Correction: Detect and correct error at position 5 → [0, 1, 1, 1, 0, 1, 0]

Remove Scrambler: m = corrected × G⁻¹ × S⁻¹ = [1, 1, 0, 1]
```

### Security Properties
```
Public Key: G' appears random due to S and P

Private Key: (G, S, P) must be kept secret

Error Vector: Small weight errors provide security while allowing correction

NP-hard Problem: Security relies on the difficulty of decoding random linear codes
```

### Advantages
```
Resistant to quantum computer attacks

Fast encryption and decryption

Proven security reduction
```
###Limitations
```
Large public key sizes

Limited to specific error patterns

Requires careful parameter selection
```

This implementation demonstrates the core concepts of the McEliece cryptosystem using a simple (7,4) Hamming code. Real-world implementations use much larger codes like Goppa codes for enhanced security.


A code-based scheme was not chosen as the primary winner. Code-based cryptography, whose most prominent candidate was Classic McEliece, was not selected as the primary standard, but it was not rejected either. It was placed into a special category.

NIST created a Fourth Round specifically for code-based and other promising KEMs. The finalists in this round are:
```
Classic McEliece (Code-based)
BIKE (Code-based)
HQC (Code-based)
```

# Why Code-Based Cryptography Wasn't Chosen as NIST's Primary Post-Quantum Standard

## The Security vs. Performance Trade-Off

NIST's decision ultimately balanced the competing advantages of lattice-based and code-based cryptography:

| Characteristic | **Lattice-Based (Kyber)** | **Code-Based (Classic McEliece)** |
|----------------|---------------------------|-----------------------------------|
| **Public Key Size** | Small (~1 KB) | Very Large (hundreds of KB to over 1 MB) |
| **Ciphertext Size** | Small (~1 KB) | Small (~200 bytes) |
| **Speed** | Very Fast | Fast (slower key generation) |
| **Security History** | Relatively newer (20-25 years) | Very old and well-studied (since 1978) |
| **Confidence in Security** | High, but newer mathematics | Extremely High, resisted cryptanalysis for 40+ years |


For quantum robustness it is recommended that N is 6960, k is 5,412 and t is 119 (giving a large key size of 8,373,911 bits.

## NIST's Primary Rationale

**Practicality and Adoption:** The massive public key size of Classic McEliece (often exceeding 1MB) posed significant barriers for widespread protocol adoption, particularly in TLS handshakes where certificate chains would become impractically large. Kyber's compact key sizes enable easier "drop-in" replacement for existing algorithms like RSA and ECC.

**Balanced Compromise:** NIST selected the candidate offering the optimal balance of security, performance, and size for mainstream use cases. While McEliece excels in proven security, Kyber provided the better overall profile for general-purpose adoption.

## The Future of Code-Based Cryptography

**Standardization Still Likely:** NIST has explicitly committed to standardizing at least one additional KEM from the fourth-round finalists, with Classic McEliece as the strong frontrunner due to its unparalleled security confidence.

**Niche Applications:** Code-based schemes remain ideal for specific environments:
- **Bandwidth-insensitive scenarios** (secure firmware updates, stored data encryption)
- **Long-term security priorities** (document encryption for 50+ years)

**Algorithmic Diversity:** Code-based cryptography provides crucial backup security. If devastating attacks emerge against lattice-based systems, the cryptographic ecosystem will have a mature, well-studied alternative ready for deployment.

## Conclusion

While code-based cryptography wasn't selected as the primary standard, it was not rejected. NIST made a pragmatic choice favoring widespread adoption (Kyber) while continuing to mature and likely standardize a code-based alternative (Classic McEliece) for long-term security needs.



This demonstrates a Key Encapsulation Mechanism (KEM) where two parties can establish a shared secret over an insecure channel.

## Concepts Explained
Step 1: Bob generates cryptographic keys (public key for encryption, private key for decryption)
Key Generation: Bob creates a public/private key pair

Step 2: Alice encrypts data using Bob's public key, creating a ciphertext and shared secret
Encapsulation: Alice uses Bob's public key to encrypt and create a shared secret

Step 3: Bob decrypts the ciphertext using his private key to recover the shared secret
Decapsulation: Bob uses his private key to decrypt and recover the shared secret

Step 4: Both parties verify they have the same shared secret for secure communication
Shared Secret: Both parties now have the same secret key for secure communication

```
# Show all available commands
make help

# Build and run in debug mode (most common during development)
make run

# Build optimized release version
make release

# Run the release version
make run-release

# Clean build artifacts
make clean

# Run tests
make test

# Format code
make fmt

# Check code quality
make lint

# Build for production (optimized and stripped)
make production

# Show binary sizes
make size

# Get project information
make info

# Common development workflow
make clean && make test && make run
```
```
Clean Target: Removes all build artifacts completely
Multiple Build Types: Debug, Release, and Production (stripped)
Development Tools: Formatting, linting, testing
Information Targets: Size analysis, project info
Safety: Security audit, dependency checking
Help System: Comprehensive help with examples
```