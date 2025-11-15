import random
import numpy as np

# Configuration with random values
SECRET = random.randint(3, 15) | 1  # Random odd number between 3-15
ERROR = random.randint(5, 20)       # Random error between 5-20
MESSAGE = random.randint(0, 1)      # Random message (0 or 1)

def generate_random_values(count=10, max_value=20):
    """Generate random values for the encryption"""
    return [random.randint(1, max_value) for _ in range(count)]

def encrypt_message(values, secret, error, message):
    """Encrypt a message using the public key system"""
    # Create public key
    public_key = [value * secret + error for value in values]
    
    # Select random half of public key values
    selected_count = len(public_key) // 2
    selected_values = random.sample(public_key, selected_count)
    
    # Calculate sum
    total = sum(selected_values)
    
    # Add message (0 or 1)
    if message == 1:
        total += 1
    
    return public_key, selected_values, total

def decrypt_message(encrypted_total, secret):
    """Decrypt the message from the encrypted total"""
    remainder = encrypted_total % secret
    return 1 if remainder % 2 == 1 else 0

# Generate random values
random_values = generate_random_values()

print("=== ENCRYPTION ===")
print(f"Original message: {MESSAGE}")
print(f"Random values: {random_values}")
print(f"Secret: {SECRET}, Error: {ERROR}")

# Encrypt the message
public_key, selected_values, encrypted_total = encrypt_message(
    random_values, SECRET, ERROR, MESSAGE
)

print(f"\nPublic key: {public_key}")
print(f"Selected values: {selected_values}")
print(f"Encrypted total: {encrypted_total}")

# Decrypt the message
print("\n=== DECRYPTION ===")
received_message = decrypt_message(encrypted_total, SECRET)
print(f"Received message: {received_message}")

# Verify if decryption was successful
print(f"\n=== RESULT ===")
if MESSAGE == received_message:
    print("✓ Success! Message was correctly transmitted.")
else:
    print("✗ Error! Message was corrupted during transmission.")

"""
=== ENCRYPTION ===
Original message: 1
Random values: [5, 10, 13, 17, 19, 14, 18, 7, 15, 17]
Secret: 5, Error: 20

Public key: [45, 70, 85, 105, 115, 90, 110, 55, 95, 105]
Selected values: [110, 95, 55, 90, 85]
Encrypted total: 436

=== DECRYPTION ===
Received message: 1

=== RESULT ===
✓ Success! Message was correctly transmitted.

"""

import numpy as np
import random

def generate_random_matrix(rows, cols, modulus):
    """Generate a random matrix with values in range [0, modulus-1]"""
    return np.random.randint(0, modulus, size=(rows, cols))

def generate_error_vector(rows, modulus):
    """Generate a random error vector with small values"""
    return np.random.randint(-1, 2, size=(rows, 1))

# Configuration
q = 13
matrix_rows = random.randint(5, 10)  # Random number of rows
matrix_cols = random.randint(3, 6)   # Random number of columns

print("=== LWE Matrix Example (Randomly Generated) ===")
print("=" * 50)

# Generate random matrices
A = generate_random_matrix(matrix_rows, matrix_cols, q)
sA = generate_random_matrix(matrix_cols, 1, q)  # Secret vector
eA = generate_error_vector(matrix_rows, q)      # Error vector

print(f"Matrix A ({A.shape[0]}×{A.shape[1]}):")
print("[" + ",\n ".join([f"[{', '.join(map(str, row))}]" for row in A]) + "]")
print()

print(f"Secret vector sA ({sA.shape[0]}×{sA.shape[1]}):")
print("[" + ",\n ".join([f"[{', '.join(map(str, row))}]" for row in sA]) + "]")
print()

print(f"Error vector eA ({eA.shape[0]}×{eA.shape[1]}):")
print("[" + ",\n ".join([f"[{', '.join(map(str, row))}]" for row in eA]) + "]")
print()

print(f"Modulus q: {q}")
print()

print("Step 1: Compute A × sA (mod q)")
print("-" * 35)
bA = np.matmul(A, sA) % q
print(f"Result bA_temp ({bA.shape[0]}×{bA.shape[1]}):")
print("[" + ",\n ".join([f"[{', '.join(map(str, row))}]" for row in bA]) + "]")
print()

print("Step 2: Add error eA (mod q)")
print("-" * 35)
bA = np.add(bA, eA) % q
print(f"FINAL OUTPUT bA ({bA.shape[0]}×{bA.shape[1]}):")
print("[" + ",\n ".join([f"[{', '.join(map(str, row))}]" for row in bA]) + "]")
print()

print("=" * 50)
print("Matrix Dimensions:")
print(f"A:  {A.shape[0]}×{A.shape[1]}  (public)")
print(f"sA: {sA.shape[0]}×{sA.shape[1]}  (secret)")
print(f"eA: {eA.shape[0]}×{eA.shape[1]}  (error)")
print(f"bA: {bA.shape[0]}×{bA.shape[1]}  (A×sA + eA)")
print("✓ All matrices are properly rectangular")

"""
=== LWE Matrix Example (Randomly Generated) ===
==================================================
Matrix A (10×3):
[[9, 3, 6],
 [11, 0, 9],
 [8, 3, 0],
 [7, 9, 3],
 [6, 2, 5],
 [1, 12, 5],
 [11, 1, 3],
 [2, 7, 6],
 [9, 5, 12],
 [1, 9, 2]]

Secret vector sA (3×1):
[[8],
 [5],
 [5]]

Error vector eA (10×1):
[[-1],
 [-1],
 [0],
 [-1],
 [0],
 [-1],
 [1],
 [1],
 [1],
 [0]]

Modulus q: 13

Step 1: Compute A × sA (mod q)
-----------------------------------
Result bA_temp (10×1):
[[0],
 [3],
 [1],
 [12],
 [5],
 [2],
 [4],
 [3],
 [1],
 [11]]

Step 2: Add error eA (mod q)
-----------------------------------
FINAL OUTPUT bA (10×1):
[[12],
 [2],
 [1],
 [11],
 [5],
 [1],
 [5],
 [4],
 [2],
 [11]]

==================================================
Matrix Dimensions:
A:  10×3  (public)
sA: 3×1  (secret)
eA: 10×1  (error)
bA: 10×1  (A×sA + eA)
✓ All matrices are properly rectangular

"""

import numpy as np
import random

def generate_random_polynomial(degree, modulus):
    """Generate a random polynomial with coefficients in range [0, modulus-1]"""
    return [random.randint(0, modulus-1) for _ in range(degree)]

def generate_error_polynomial(degree, modulus):
    """Generate a random error polynomial with small coefficients"""
    return [random.randint(-1, 1) for _ in range(degree)]

def polynomial_to_string(poly):
    """Convert polynomial to string representation"""
    terms = []
    for i, coeff in enumerate(poly):
        if coeff != 0:
            if i == 0:
                terms.append(f"{coeff}")
            elif i == 1:
                terms.append(f"{coeff}x")
            else:
                terms.append(f"{coeff}x^{i}")
    return " + ".join(terms) if terms else "0"

# Configuration
q = 13  # Modulus
n = 4   # Polynomial degree

print("=== Ring-LWE Simplified Example ===")
print("=" * 40)

# Generate random values
A = generate_random_polynomial(n, q)
sA = generate_random_polynomial(n, q)
eA = generate_error_polynomial(n, q)

print("Polynomial Representations:")
print(f"A(x)  = {polynomial_to_string(A)}")
print(f"sA(x) = {polynomial_to_string(sA)}")
print(f"eA(x) = {polynomial_to_string(eA)}")
print(f"\nCoefficient form:")
print(f"A  = {A}")
print(f"sA = {sA}")
print(f"eA = {eA}")
print(f"Modulus q = {q}")

# Define polynomial modulus: x^n + 1
xN_1 = [1] + [0] * (n-1) + [1]
print(f"\nPolynomial modulus: Φ(x) = x^{n} + 1")
print(f"Coefficient form: {xN_1}")

print("\n" + "=" * 40)
print("Step 1: Compute A × sA (mod q and mod Φ(x))")
print("-" * 40)

# Polynomial multiplication: A * sA
raw_mult = np.polymul(A, sA)
print(f"Raw multiplication: {raw_mult}")

# Reduce modulo q
mod_q = raw_mult % q
print(f"After mod {q}:     {mod_q}")

# Reduce modulo x^n + 1
bA = np.floor(np.polydiv(mod_q, xN_1)[1]).astype(int)
print(f"After mod Φ(x):    {bA}")

print("\n" + "=" * 40)
print("Step 2: Add error eA (mod q and mod Φ(x))")
print("-" * 40)

# Add error polynomial
with_error = np.polyadd(bA, eA)
print(f"After adding error: {with_error}")

# Reduce modulo q
mod_q2 = with_error % q
print(f"After mod {q}:      {mod_q2}")

# Reduce modulo x^n + 1 (final result)
bA_final = np.floor(np.polydiv(mod_q2, xN_1)[1]).astype(int)
print(f"After mod Φ(x):     {bA_final}")

print("\n" + "=" * 40)
print("FINAL RESULTS")
print("-" * 40)
print(f"Input:")
print(f"  A(x)  = {polynomial_to_string(A)}")
print(f"  sA(x) = {polynomial_to_string(sA)}")
print(f"  eA(x) = {polynomial_to_string(eA)}")
print(f"\nOutput:")
print(f"  bA(x) = {polynomial_to_string(bA_final)}")
print(f"\nIn coefficient form:")
print(f"  bA = {list(bA_final)}")

print("\nVerification:")
print(f"  bA = (A × sA + eA) mod q mod (x^{n} + 1)")
print(f"     = ({A} × {sA} + {eA}) mod {q} mod {xN_1}")
print(f"     = {list(bA_final)}")

"""
=== Ring-LWE Simplified Example ===
========================================
Polynomial Representations:
A(x)  = 6 + 3x + 9x^2 + 8x^3
sA(x) = 11 + 2x + 11x^2 + 3x^3
eA(x) = -1 + 1x + -1x^2

Coefficient form:
A  = [6, 3, 9, 8]
sA = [11, 2, 11, 3]
eA = [-1, 1, -1, 0]
Modulus q = 13

Polynomial modulus: Φ(x) = x^4 + 1
Coefficient form: [1, 0, 0, 0, 1]

========================================
Step 1: Compute A × sA (mod q and mod Φ(x))
----------------------------------------
Raw multiplication: [ 66  45 171 157 124 115  24]
After mod 13:     [ 1  6  2  1  7 11 11]
After mod Φ(x):    [1 6 5 9]

========================================
Step 2: Add error eA (mod q and mod Φ(x))
----------------------------------------
After adding error: [0 7 4 9]
After mod 13:      [0 7 4 9]
After mod Φ(x):     [7 4 9]

========================================
FINAL RESULTS
----------------------------------------
Input:
  A(x)  = 6 + 3x + 9x^2 + 8x^3
  sA(x) = 11 + 2x + 11x^2 + 3x^3
  eA(x) = -1 + 1x + -1x^2

Output:
  bA(x) = 7 + 4x + 9x^2

In coefficient form:
  bA = [np.int64(7), np.int64(4), np.int64(9)]

Verification:
  bA = (A × sA + eA) mod q mod (x^4 + 1)
     = ([6, 3, 9, 8] × [11, 2, 11, 3] + [-1, 1, -1, 0]) mod 13 mod [1, 0, 0, 0, 1]
     = [np.int64(7), np.int64(4), np.int64(9)]

"""

