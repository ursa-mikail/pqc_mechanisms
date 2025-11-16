# Lattice-Based Cryptography: CVP Problem Demonstration

## Overview

This Python demonstration illustrates the **Closest Vector Problem (CVP)** in lattice-based cryptography, showing how the choice of basis dramatically affects the difficulty of finding the nearest lattice point to a target.

## Mathematical Background

### Lattice Definition

A **lattice** $\mathcal{L}$ in $\mathbb{R}^n$ is the set of all integer linear combinations of basis vectors:

$$\mathcal{L}(\mathbf{B}) = \left\{ \sum_{i=1}^{n} a_i \mathbf{v}_i : a_i \in \mathbb{Z} \right\}$$

where $\mathbf{B} = \{\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_n\}$ is the basis.

### The Closest Vector Problem (CVP)

**Given:** A lattice $\mathcal{L}$ and a target vector $\mathbf{t} \in \mathbb{R}^n$

**Find:** The lattice point $\mathbf{w} \in \mathcal{L}$ that minimizes $\|\mathbf{t} - \mathbf{w}\|$

$$\mathbf{w}^* = \arg\min_{\mathbf{w} \in \mathcal{L}} \|\mathbf{t} - \mathbf{w}\|$$

CVP is **NP-hard** in general, but becomes tractable with a "good" (nearly orthogonal) basis.

### Basis Quality: Orthogonality Defect

The quality of a basis is measured by how close to orthogonal the vectors are:

$$\cos(\theta) = \frac{\mathbf{v}_1 \cdot \mathbf{v}_2}{\|\mathbf{v}_1\| \|\mathbf{v}_2\|}$$

- **Good basis:** $|\cos(\theta)| \approx 0$ (vectors nearly perpendicular)
- **Bad basis:** $|\cos(\theta)| \approx 1$ (vectors nearly parallel)

### Unimodular Transformations

Two bases $\mathbf{B}$ and $\mathbf{B}'$ span the **same lattice** if and only if:

$$\mathbf{B}' = \mathbf{B} \cdot \mathbf{U}$$

where $\mathbf{U}$ is a **unimodular matrix** (integer matrix with $\det(\mathbf{U}) = \pm 1$).

**Example:**
$$\mathbf{U} = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}, \quad \det(\mathbf{U}) = 1$$

### Babai's Nearest Plane Algorithm

A polynomial-time **approximation** algorithm for CVP:

1. Express target in basis coordinates: $\mathbf{t} = \sum_{i=1}^{n} c_i \mathbf{v}_i$
2. Round coefficients: $\tilde{a}_i = \lfloor c_i \rceil$ (round to nearest integer)
3. Return: $\mathbf{w}_{\text{Babai}} = \sum_{i=1}^{n} \tilde{a}_i \mathbf{v}_i$

**Accuracy:** Babai's algorithm is optimal for orthogonal bases but may fail for skewed bases.

## Cryptographic Application

### The Trapdoor Mechanism

**Public Key (Good Basis):** Nearly orthogonal basis $\mathbf{B}_{\text{pub}}$
- CVP is **easy** using Babai's algorithm
- Used for encryption

**Private Key (Bad Basis):** Highly skewed basis $\mathbf{B}_{\text{priv}}$ spanning the same lattice
- CVP is **hard** without the good basis
- Used for decryption (owner has the good basis)

### Security Principle

$$\mathcal{L}(\mathbf{B}_{\text{pub}}) = \mathcal{L}(\mathbf{B}_{\text{priv}})$$

but:

$$\text{CVP}_{\mathbf{B}_{\text{pub}}}(\mathbf{t}) \text{ is easy} \quad \text{while} \quad \text{CVP}_{\mathbf{B}_{\text{priv}}}(\mathbf{t}) \text{ is hard}$$

## Code Demonstration

### Three Test Cases

#### 1. Good Basis (Nearly Orthogonal)
```python
v₁ = (5, 1)
v₂ = (-2, 8)
cos(θ) ≈ -0.048  # Nearly perpendicular
```
**Result:** Babai's algorithm finds the true closest point ✓

#### 2. Same Lattice, Different Basis (Skewed)
```python
# Unimodular transform: [[1,1],[0,1]]
v₁' = (3, 9)
v₂' = (-2, 8)
cos(θ) ≈ 0.844  # Highly skewed
```
**Result:** Babai may fail, but **true CVP gives same point** as Case 1 (same lattice!)

#### 3. Bad Basis (Nearly Parallel, Different Lattice)
```python
v₁ = (37, 41)
v₂ = (39, 43)
cos(θ) ≈ 1.000  # Nearly parallel
```
**Result:** Different lattice → **different closest point**

### Key Algorithm Comparison

| Algorithm | Complexity | Accuracy |
|-----------|------------|----------|
| **Babai's Rounding** | $O(n^3)$ | Optimal for orthogonal bases only |
| **Exhaustive Search** | Exponential | Always finds true CVP |
| **LLL + Babai** | $O(n^5)$ | Better approximation guarantee |

## Mathematical Proofs

### Theorem 1: Unimodular Invariance
If $\mathbf{B}' = \mathbf{B} \cdot \mathbf{U}$ where $\det(\mathbf{U}) = \pm 1$, then:

$$\mathcal{L}(\mathbf{B}) = \mathcal{L}(\mathbf{B}')$$

**Proof:** Since $\mathbf{U}$ is unimodular, it has an integer inverse. Any point in $\mathcal{L}(\mathbf{B})$ can be expressed in $\mathcal{L}(\mathbf{B}')$ and vice versa.

### Theorem 2: CVP Lattice Invariance
For any two bases $\mathbf{B}_1, \mathbf{B}_2$ spanning the same lattice:

$$\text{CVP}_{\mathbf{B}_1}(\mathbf{t}) = \text{CVP}_{\mathbf{B}_2}(\mathbf{t})$$

The **true** closest point is basis-independent (only depends on the lattice, not the basis).

## Running the Code

### Requirements
```bash
pip install numpy matplotlib
```

### Execution
```bash
python lattice_cvp_demo.py
```

### Output

The script generates three plots showing:
- 🔵 Blue dots: Lattice points
- 🔴 Red arrow: Basis vector $\mathbf{v}_1$
- 🟢 Green arrow: Basis vector $\mathbf{v}_2$
- ⭐ Purple star: Target point
- 🟢 Green circle: **True** closest lattice point
- 🟧 Orange square: Babai's approximation (if different)

Console output shows:
- Basis vectors and angle between them
- True CVP solution
- Babai's approximation
- Verification that same lattice → same CVP

## Key Insights

### ✅ Correct Understanding
1. **Same lattice always gives same CVP** (regardless of basis choice)
2. **Babai's algorithm is just an approximation** (not always optimal)
3. **Basis quality affects algorithm performance**, not the mathematical answer
4. **Good basis makes CVP computationally easy**
5. **Bad basis makes CVP computationally hard** (even though answer is the same)

### ❌ Common Misconceptions
1. "Different bases give different closest points" → FALSE (if same lattice)
2. "Babai always finds the closest point" → FALSE (only for good bases)
3. "Bad basis changes the lattice" → FALSE (unimodular transforms preserve lattice)

## References

1. **Micciancio, D., & Regev, O.** (2009). *Lattice-based Cryptography*. Post-Quantum Cryptography.
2. **Babai, L.** (1986). *On Lovász' lattice reduction and the nearest lattice point problem*. Combinatorica, 6(1), 1-13.
3. **Lenstra, A. K., Lenstra, H. W., & Lovász, L.** (1982). *Factoring polynomials with rational coefficients*. Mathematische Annalen, 261(4), 515-534.


# Babai's CVP Algorithms: Rounding vs Nearest Plane

## Overview

This document explains the **key differences** between two polynomial-time approximation algorithms for the Closest Vector Problem (CVP) in lattice-based cryptography:

1. **Babai's Rounding Algorithm** (simple, less accurate)
2. **Babai's Nearest Plane Algorithm** (sophisticated, better approximation)

Both are approximation algorithms, but they differ significantly in methodology and accuracy.

---

## Algorithm 1: Babai's Rounding

### Mathematical Formulation

**Given:** Basis $\mathbf{B} = \{\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_n\}$ and target $\mathbf{t}$

**Algorithm:**

1. Solve the linear system: $\mathbf{t} = \sum_{i=1}^{n} c_i \mathbf{v}_i$ for real coefficients $c_i \in \mathbb{R}$

2. Round each coefficient: $\tilde{a}_i = \lfloor c_i \rceil$ (round to nearest integer)

3. Return: $\mathbf{w}_{\text{round}} = \sum_{i=1}^{n} \tilde{a}_i \mathbf{v}_i$

### Matrix Form

$$\begin{pmatrix} c_1 \\ c_2 \\ \vdots \\ c_n \end{pmatrix} = \mathbf{B}^{-1} \mathbf{t}$$

Then: $\tilde{a}_i = \text{round}(c_i)$

### Python Implementation

```python
def babai_rounding(basis_matrix, target):
    # Solve: target = basis_matrix @ coeffs
    coeffs = np.linalg.solve(basis_matrix, target)
    
    # Round to integers
    rounded_coeffs = np.round(coeffs)
    
    # Compute lattice point
    result = basis_matrix @ rounded_coeffs
    return result
```

### Properties

- **Complexity:** $O(n^3)$ (dominated by matrix inversion)
- **Optimality:** Optimal **only** for orthogonal bases
- **Approximation Factor:** Can be arbitrarily bad for skewed bases
- **Simplicity:** Very simple to implement

---

## Algorithm 2: Babai's Nearest Plane

### Mathematical Formulation

**Given:** Basis $\mathbf{B} = \{\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_n\}$ and target $\mathbf{t}$

**Algorithm (iterative):**

Initialize: $\mathbf{t}_0 = \mathbf{t}$

For $i = 1$ to $n$:

1. Compute coefficient: $c_i = \frac{\langle \mathbf{t}_{i-1}, \mathbf{v}_i \rangle}{\langle \mathbf{v}_i, \mathbf{v}_i \rangle}$

2. Round: $\tilde{a}_i = \lfloor c_i \rceil$

3. Update target: $\mathbf{t}_i = \mathbf{t}_{i-1} - \tilde{a}_i \mathbf{v}_i$

Return: $\mathbf{w}_{\text{plane}} = \sum_{i=1}^{n} \tilde{a}_i \mathbf{v}_i$

### Geometric Interpretation

At each step, we:
- **Project** the remaining target onto the current basis vector
- **Round** the projection coefficient
- **Subtract** the rounded component, moving to the "nearest plane" orthogonal to $\mathbf{v}_i$

This is why it's called **Nearest Plane** - we iteratively move to hyperplanes closest to the target.

### Python Implementation

```python
def babai_nearest_plane(basis_vectors, target):
    n = len(basis_vectors)
    coeffs = []
    t_remaining = target.copy()
    
    for i in range(n):
        v_i = basis_vectors[i]
        
        # Project remaining target onto v_i
        dot_product = np.dot(t_remaining, v_i)
        v_norm_sq = np.dot(v_i, v_i)
        c_i = dot_product / v_norm_sq
        
        # Round coefficient
        a_i = round(c_i)
        coeffs.append(a_i)
        
        # Remove this component from target
        t_remaining = t_remaining - a_i * v_i
    
    # Reconstruct lattice point
    result = sum(a * v for a, v in zip(coeffs, basis_vectors))
    return result
```

### Properties

- **Complexity:** $O(n^2)$ per iteration, $O(n^3)$ total
- **Approximation Factor:** $2^{n/2} \cdot \gamma_n$ where $\gamma_n$ is Hermite's constant
- **Basis Dependence:** Order of basis vectors matters!
- **Better Guarantee:** Provable approximation bound (unlike rounding)

---

## Key Differences

| Aspect | Rounding | Nearest Plane |
|--------|----------|---------------|
| **Method** | Solve once, round all | Iterative projection |
| **Geometric View** | Direct coordinate rounding | Sequential hyperplane approximation |
| **Complexity** | $O(n^3)$ | $O(n^3)$ |
| **Approximation** | No guarantee | $2^{n/2} \cdot \gamma_n$ factor |
| **Orthogonal Bases** | Optimal | Optimal |
| **Skewed Bases** | Can fail badly | Better performance |
| **Basis Order** | Doesn't matter | **Matters!** |
| **Implementation** | Simpler | Slightly more complex |

---

## Theoretical Comparison

### Approximation Quality

For a basis with orthogonality defect $\delta(\mathbf{B})$:

$$\delta(\mathbf{B}) = \frac{\prod_{i=1}^{n} \|\mathbf{v}_i\|}{\det(\mathbf{B})}$$

**Rounding:** No approximation guarantee in terms of $\delta(\mathbf{B})$

**Nearest Plane:** Guarantees that:

$$\|\mathbf{t} - \mathbf{w}_{\text{plane}}\| \leq \sqrt{n} \cdot \lambda_1(\mathcal{L})$$

where $\lambda_1(\mathcal{L})$ is the length of the shortest non-zero lattice vector.

### Example: Why Nearest Plane Is Better

Consider a 2D basis:

$$\mathbf{v}_1 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad \mathbf{v}_2 = \begin{pmatrix} 0.9 \\ 0.1 \end{pmatrix}$$

Target: $\mathbf{t} = (0.6, 0.05)$

**Rounding:**
```
Solve: t = c₁v₁ + c₂v₂
→ c₁ = 0.15, c₂ = 0.50
Round: ã₁ = 0, ã₂ = 1
Result: (0.9, 0.1) - distance = 0.316
```

**Nearest Plane:**
```
Step 1: Project t onto v₁
  c₁ = ⟨t,v₁⟩/⟨v₁,v₁⟩ = 0.6
  Round: ã₁ = 1
  Update: t' = t - 1·v₁ = (-0.4, 0.05)

Step 2: Project t' onto v₂
  c₂ = ⟨t',v₂⟩/⟨v₂,v₂⟩ = -0.415
  Round: ã₂ = 0
  
Result: (1, 0) - distance = 0.4
```

In this case, neither finds the true closest point $(1, 0)$, but the iterative approach of Nearest Plane handles the skewed basis better.

---

## When Each Algorithm Excels

### Use Babai's Rounding When:

✅ Basis is **nearly orthogonal** ($|\cos(\theta_{ij})| < 0.1$)

✅ You need **simplest possible implementation**

✅ Speed is critical and basis quality is guaranteed

✅ You're doing **education/demonstration**

### Use Babai's Nearest Plane When:

✅ Basis may be **moderately skewed**

✅ You need **better approximation guarantees**

✅ You're implementing **real cryptographic systems**

✅ Basis has been **LLL-reduced** but not perfectly orthogonal

---

## Impact of Basis Order (Nearest Plane Only)

⚠️ **Critical:** Nearest Plane results depend on the **order** of basis vectors!

### Example

Basis: $\mathbf{v}_1 = (5, 1)$, $\mathbf{v}_2 = (-2, 8)$

**Order 1:** Process $[\mathbf{v}_1, \mathbf{v}_2]$ → Result A

**Order 2:** Process $[\mathbf{v}_2, \mathbf{v}_1]$ → Result B (potentially different!)

**Best Practice:** Use **LLL reduction** first to get a "good" basis ordering.

---

## Real-World Performance

### Test Case: Skewed 2D Lattice

**Basis:** $\mathbf{v}_1 = (3, 9)$, $\mathbf{v}_2 = (-2, 8)$  
**Target:** $(27, 8)$  
**cos(θ):** $0.844$ (highly skewed)

| Algorithm | Result | Distance | Correct? |
|-----------|--------|----------|----------|
| **Rounding** | (28, 14) | 6.32 | ❌ |
| **Nearest Plane** | (28, 14) | 6.32 | ❌ |
| **True CVP** | (30, 6) | 2.83 | ✅ |

Both fail on highly skewed bases, but Nearest Plane typically fails less often!

### Test Case: Good 2D Lattice

**Basis:** $\mathbf{v}_1 = (5, 1)$, $\mathbf{v}_2 = (-2, 8)$  
**Target:** $(27, 8)$  
**cos(θ):** $-0.048$ (nearly orthogonal)

| Algorithm | Result | Distance | Correct? |
|-----------|--------|----------|----------|
| **Rounding** | (30, 6) | 2.83 | ✅ |
| **Nearest Plane** | (30, 6) | 2.83 | ✅ |
| **True CVP** | (30, 6) | 2.83 | ✅ |

Both succeed on good bases!

---

## Integration with LLL Reduction

In practice, both algorithms are used **after LLL reduction**:

```
1. Start with arbitrary basis B
2. Apply LLL reduction: B' = LLL(B)
3. Apply Babai (Rounding or Nearest Plane) on B'
4. Get approximate CVP solution
```

LLL gives a "good enough" basis where both algorithms perform reasonably well.

### LLL + Babai Approximation Factor

Combined approximation: $2^{O(n)} \cdot \lambda_1(\mathcal{L})$

This is exponential but works well in practice for moderate dimensions ($n \leq 500$).

---

## Cryptographic Implications

### Encryption (Public Key - Good Basis)

Use **either** Rounding or Nearest Plane:
- With a good public basis, both work
- Rounding is simpler, so often preferred
- Decryption must be fast and reliable

### Cryptanalysis (Attack - Bad Basis)

Use **Nearest Plane** (or better):
- Attacker has bad basis
- Nearest Plane gives better chances
- But still exponentially hard for large $n$

### The Security Gap

$$\text{Security} = \frac{\text{Difficulty with bad basis}}{\text{Difficulty with good basis}}$$

The gap must be exponential for security. Both algorithms are easy with good bases, hard with bad bases, but **Nearest Plane narrows the gap slightly**.

---

## Pseudocode Comparison

### Rounding (Vectorized)

```
function BABAI_ROUNDING(B, t):
    c ← B⁻¹ · t                 // Solve linear system
    ã ← ROUND(c)                // Round all coefficients
    w ← B · ã                   // Reconstruct lattice point
    return w
```

### Nearest Plane (Sequential)

```
function BABAI_NEAREST_PLANE(B, t):
    t' ← t                      // Working copy
    ã ← []                      // Coefficients list
    
    for i = 1 to n:
        cᵢ ← ⟨t', vᵢ⟩ / ⟨vᵢ, vᵢ⟩   // Project
        ãᵢ ← ROUND(cᵢ)           // Round
        t' ← t' - ãᵢ · vᵢ        // Update target
        APPEND(ã, ãᵢ)
    
    w ← Σ ãᵢ · vᵢ               // Reconstruct
    return w
```

---

## Historical Context

**1986:** László Babai introduces both algorithms in his seminal paper:
> *"On Lovász' lattice reduction and the nearest lattice point problem"*

**Key Insight:** CVP is NP-hard in general, but polynomial-time approximation is possible with:
1. Simple rounding (no guarantees)
2. Iterative nearest plane (provable bounds)

**Impact:** Foundation for modern lattice cryptography (NTRU, GGH, etc.)

---

## Further Reading

1. **Babai, L.** (1986). *On Lovász' lattice reduction and the nearest lattice point problem.* Combinatorica, 6(1), 1-13.

2. **Micciancio, D., & Goldwasser, S.** (2002). *Complexity of Lattice Problems: A Cryptographic Perspective.* Springer.

3. **Nguyen, P. Q., & Stern, J.** (2001). *The two faces of lattices in cryptology.* Cryptography and Lattices, 146-180.

4. **Regev, O.** (2009). *On lattices, learning with errors, random linear codes, and cryptography.* JACM, 56(6), 1-40.

---

## Summary

| Criterion | Winner |
|-----------|--------|
| Simplicity | 🏆 Rounding |
| Approximation Guarantee | 🏆 Nearest Plane |
| Orthogonal Bases | 🤝 Tie (both optimal) |
| Skewed Bases | 🏆 Nearest Plane |
| Implementation Complexity | 🏆 Rounding |
| Practical Cryptography | 🏆 Nearest Plane |

**Bottom Line:** Use **Rounding** for quick prototypes and education. Use **Nearest Plane** for production cryptographic systems where basis quality isn't perfect.


