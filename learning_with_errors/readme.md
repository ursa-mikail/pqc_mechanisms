# Learning With Errors (LWE) Encryption
## Overview
Learning With Errors (LWE) is a quantum-resistant cryptographic method developed by Oded Regev in 2005. This implementation demonstrates a simplified version of LWE for educational purposes.

## Key Generation
```
Secret Key (s): An odd integer known only to the receiver

Error Value (e): A small integer that adds noise to the encryption

Random Values: A set of random integers

Public Key: Generated as public_key[i] = random[i] × s + e
```

## Encryption Process
```
Select a random subset of values from the public key

Calculate the sum of selected values

Add the message (0 or 1) to the sum

Send the encrypted total
```

## Decryption Process
```
Calculate remainder = encrypted_total % secret_key

If remainder is even → message was "0"

If remainder is odd → message was "1"
```

## Security Properties
```
Based on the difficulty of solving t = gs + e when only t and g are known

The error term e provides security through noise

Resistant to quantum computer attacks
```

# Learning With Errors (LWE) and Ring-LWE (RLWE)

Learning With Errors (LWE) and its polynomial version, Ring Learning With Errors (RLWE), form the basis of several post-quantum cryptographic systems. 

---

## 1. Learning With Errors (LWE)

LWE is based on the hardness of solving noisy linear equations.  
We generate:

- a secret vector \( s \)
- a small random error vector \( e \)
- a random public matrix \( A \)

We compute:

$$\
B = A s + e
\$$

Here:

- \( s \) is the **secret key**
- \( A \) and \( B \) form the **public key**

Given \( A \) and \( B \), recovering \( s \) is computationally hard due to the added noise \( e \).

---

## 2. Ring Learning With Errors (RLWE)

RLWE replaces matrices with polynomial rings.  
All operations occur in the ring:

\[
\mathbb{Z}_q[x]/(x^n + 1)
\]

where:

- \( n \) is the degree-1 dimension parameter
- \( q = 2^n - 1 \)
- coefficients are reduced modulo \( q \)

---

## 3. Polynomial Setup

### 3.1 Alice chooses:

A public polynomial:

\[
A(x) = a_{n-1}x^{n-1} + \cdots + a_2 x^2 + a_1 x + a_0
\]

She reduces it modulo:

\[
\Phi(x) = x^n + 1
\]

In Python:

```python
xN_1 = [1] + [0] * (n-1) + [1]   # x^n + 1
A = np.floor(p.polydiv(A, xN_1)[1])
```

### 3.2 Alice generates small random polynomials

Alice samples small error and secret polynomials:

\[
e_A(x) = e_{n-1}x^{n-1} + \cdots + e_1 x + e_0 \pmod{q}
\]

\[
s_A(x) = s_{n-1}x^{n-1} + \cdots + s_1 x + s_0 \pmod{q}
\]

She then computes:

\[
b_A(x) = A(x)s_A(x) + e_A(x)
\]

**Python:**
```python
bA = p.polymul(A, sA) % q
bA = np.floor(p.polydiv(sA, xN_1)[1])
bA = p.polyadd(bA, eA) % q
```

## 4. Bob's Setup

Bob generates his own error and secret polynomials:

\[
e_B(x), \quad s_B(x)
\]

Then computes:

\[
b_B(x) = A(x)s_B(x) + e_B(x)
\]

```
sB = gen_poly(n, q)
eB = gen_poly(n, q)

bB = p.polymul(A, sB) % q
bB = np.floor(p.polydiv(sB, xN_1)[1])
bB = p.polyadd(bB, eB) % q

```

Alice sends \( A(x) \) to Bob; Bob sends \( b_B(x) \) to Alice.


---

## 5. Shared Secret Computation

Alice computes:

\[
\text{shared}_A
= \left( b_B(x) \cdot s_A(x) \right) \bmod (x^n + 1)
\]

Bob computes:

\[
\text{shared}_B
= \left( b_A(x) \cdot s_B(x) \right) \bmod (x^n + 1)
\]


```
sharedAlice = np.floor(p.polymul(sA, bB) % q)
sharedAlice = np.floor(p.polydiv(sharedAlice, xN_1)[1]) % q

sharedBob = np.floor(p.polymul(sB, bA) % q)
sharedBob = np.floor(p.polydiv(sharedBob, xN_1)[1]) % q

```

At the end:

\[
\text{shared}_A = \text{shared}_B
\]

Thus, Alice and Bob derive a common shared key.

---

## Summary

- **LWE** uses linear algebra with noise.  
- **RLWE** uses polynomial arithmetic modulo \( x^n + 1 \).  
- Both produce a shared secret via a Diffie–Hellman–like exchange.  
- Noise polynomials make inversion hard, ensuring post-quantum security.

Refer: [url](https://summerschool-croatia.cs.ru.nl/2018/slides/Introduction%20to%20post-quantum%20cryptography%20and%20learning%20with%20errors.pdf)



