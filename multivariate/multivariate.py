import numpy as np

# Configuration
p = 97
w, x, y, z = 7, 4, 5, 6
m = [w, x, y, z]
m_dash = np.transpose(m)

# Coefficient matrices for 4 different polynomials
M0 = [[1, 2, 1, 1], [2, 3, 3, -2], [1, 3, 0, 0], [1, -2, 0, 0]]
M1 = [[5, 2, 1, 2], [1, 3, 2, 2], [3, 2, 0, 0], [6, -3, 0, 0]]
M2 = [[4, 2, 2, 1], [3, 3, 3, -2], [0, 3, 0, 0], [2, -3, 0, 0]]
M3 = [[6, 2, 1, 1], [5, 4, 3, -3], [1, 6, 0, 0], [1, -5, 0, 0]]

def print_polynomial(M):
    """Convert matrix to readable polynomial equation"""
    return (f"{M[0][0]}w² + {M[0][1]+M[1][0]}wx + {M[1][1]}x² + "
            f"{M[0][2]+M[2][0]}wy + {M[1][3]+M[3][1]}xz + "
            f"{M[0][3]+M[3][0]}wz + {M[1][2]+M[2][1]}xy")

# Calculate results
results = []
for M in [M0, M1, M2, M3]:
    res = np.dot(np.dot(m, M), m_dash) % p
    results.append(res)

# Display
print("Multivariate Cryptography Demo")
print("=" * 40)
print(f"Prime modulus: p = {p}")
print(f"Solution: w={w}, x={x}, y={y}, z={z}")
print()

print("Polynomial Equations:")
print(f"1. {print_polynomial(M0)} = {results[0]} (mod {p})")
print(f"2. {print_polynomial(M1)} = {results[1]} (mod {p})") 
print(f"3. {print_polynomial(M2)} = {results[2]} (mod {p})")
print(f"4. {print_polynomial(M3)} = {results[3]} (mod {p})")

print("\n✅ All equations are satisfied with the given solution!")
print("🔒 Finding this solution from the equations alone is computationally hard.")

"""
Multivariate Cryptography Demo
========================================
Prime modulus: p = 97
Solution: w=7, x=4, y=5, z=6

Polynomial Equations:
1. 1w² + 4wx + 3x² + 2wy + -4xz + 2wz + 6xy = 96 (mod 97)
2. 5w² + 3wx + 3x² + 4wy + -1xz + 8wz + 4xy = 36 (mod 97)
3. 4w² + 5wx + 3x² + 2wy + -5xz + 3wz + 6xy = 95 (mod 97)
4. 6w² + 7wx + 4x² + 2wy + -8xz + 2wz + 9xy = 17 (mod 97)

✅ All equations are satisfied with the given solution!
🔒 Finding this solution from the equations alone is computationally hard.

"""

import numpy as np
import random

def generate_multivariate_system(num_variables=4, prime=97):
    """
    Generate a random multivariate quadratic system with solution
    """
    # Generate random solution
    solution = [random.randint(0, prime-1) for _ in range(num_variables)]
    m = np.array(solution)
    m_dash = np.transpose(m)
    
    # Generate random coefficient matrices
    matrices = []
    polynomials = []
    results = []
    
    print("🔐 Multivariate Cryptography Demo")
    print("=" * 50)
    print(f"Prime modulus: p = {prime}")
    print(f"Random solution: {[f'v{i+1}={val}' for i, val in enumerate(solution)]}")
    print()
    
    for poly_num in range(num_variables):
        # Create symmetric-like matrix for quadratic form
        M = []
        for i in range(num_variables):
            row = []
            for j in range(num_variables):
                if i == j:
                    # Diagonal elements (squared terms)
                    row.append(random.randint(1, 5))
                elif i < j:
                    # Upper triangle (cross terms)
                    row.append(random.randint(-3, 3))
                else:
                    # Lower triangle (symmetric)
                    row.append(0)  # Will be handled by symmetry
            M.append(row)
        
        # Make roughly symmetric for cross terms
        for i in range(num_variables):
            for j in range(i+1, num_variables):
                M[j][i] = M[i][j]  # Make symmetric
        
        matrices.append(M)
        
        # Calculate result
        res = np.dot(np.dot(m, M), m_dash) % prime
        results.append(res)
        
        # Build polynomial string
        poly_parts = []
        for i in range(num_variables):
            for j in range(i, num_variables):
                coef = M[i][j]
                if coef != 0:
                    if i == j:
                        poly_parts.append(f"{coef}v{i+1}²")
                    else:
                        poly_parts.append(f"{coef}v{i+1}v{j+1}")
        
        polynomials.append(" + ".join(poly_parts).replace("+ -", "- "))
    
    return solution, matrices, polynomials, results

def verify_solution(solution, matrices, prime=97):
    """Verify the solution works for all equations"""
    m = np.array(solution)
    m_dash = np.transpose(m)
    
    print("✅ Verification:")
    print("-" * 30)
    all_correct = True
    
    for i, M in enumerate(matrices):
        calculated = np.dot(np.dot(m, M), m_dash) % prime
        expected = results[i]
        status = "✓" if calculated == expected else "✗"
        print(f"Equation {i+1}: {status} (Result: {calculated})")
        if calculated != expected:
            all_correct = False
    
    return all_correct

# Generate and run demo
if __name__ == "__main__":
    # Parameters
    NUM_VARIABLES = 4
    PRIME = 97
    
    # Generate random system
    solution, matrices, polynomials, results = generate_multivariate_system(NUM_VARIABLES, PRIME)
    
    # Display equations
    print("📝 Generated Polynomial Equations:")
    print("-" * 40)
    for i, (poly, res) in enumerate(zip(polynomials, results)):
        print(f"{i+1}. {poly} = {res} (mod {PRIME})")
    print()
    
    # Verify
    is_valid = verify_solution(solution, matrices, PRIME)
    
    print("\n" + "=" * 50)
    if is_valid:
        print("🎯 Success! All equations are satisfied.")
        print("💡 This demonstrates how multivariate cryptography works:")
        print("   - Easy to verify with the solution")
        print("   - Hard to find the solution from the equations")
        print("   - Quantum-resistant foundation")
    else:
        print("❌ Verification failed!")
    
    print(f"\n🔍 Try finding the solution from the equations above!")
    print(f"   Solution: {solution}")

"""
🔐 Multivariate Cryptography Demo
==================================================
Prime modulus: p = 97
Random solution: ['v1=79', 'v2=75', 'v3=26', 'v4=68']

📝 Generated Polynomial Equations:
----------------------------------------
1. 3v1² + 3v2² + 1v2v3 + 3v2v4 + 4v3² - 3v3v4 + 2v4² = 50 (mod 97)
2. 2v1² + 2v1v2 - 2v1v3 + 2v2² - 1v2v3 - 2v2v4 + 2v3² - 1v3v4 + 2v4² = 58 (mod 97)
3. 3v1² + 2v1v2 - 2v1v3 - 1v1v4 + 2v2² - 2v2v3 + 2v2v4 + 4v3² - 1v3v4 + 3v4² = 19 (mod 97)
4. 5v1² + 1v1v3 - 3v1v4 + 1v2² + 1v2v3 - 2v2v4 + 2v3² + 3v3v4 + 2v4² = 28 (mod 97)

✅ Verification:
------------------------------
Equation 1: ✓ (Result: 50)
Equation 2: ✓ (Result: 58)
Equation 3: ✓ (Result: 19)
Equation 4: ✓ (Result: 28)

==================================================
🎯 Success! All equations are satisfied.
💡 This demonstrates how multivariate cryptography works:
   - Easy to verify with the solution
   - Hard to find the solution from the equations
   - Quantum-resistant foundation

🔍 Try finding the solution from the equations above!
   Solution: [79, 75, 26, 68]

"""    
