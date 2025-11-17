import numpy as np

def solve_linear_modular(A, b, p):
    """Solve A*x = b (mod p) for x - THIS IS WHERE THE INVERSE HAPPENS"""
    print("🔍 SOLVING LINEAR SYSTEM STEP-BY-STEP:")
    print(f"   A = {A.tolist()}")
    print(f"   b = {b.tolist()}")
    print(f"   p = {p}")
    print()
    
    # STEP 1: Calculate determinant
    det = (A[0,0]*A[1,1] - A[0,1]*A[1,0]) % p
    print(f"1. Determinant = ({A[0,0]}×{A[1,1]} - {A[0,1]}×{A[1,0]}) mod {p} = {det}")
    
    # STEP 2: Find modular inverse of determinant
    # This is the key step - finding a number that when multiplied by det gives 1 mod p
    det_inv = None
    for i in range(1, p):
        if (i * det) % p == 1:
            det_inv = i
            break
    
    print(f"2. Modular inverse of {det} mod {p} = {det_inv}")
    print(f"   Because {det} × {det_inv} = {det * det_inv} ≡ {(det * det_inv) % p} mod {p}")
    
    # STEP 3: Calculate adjugate matrix (transpose of cofactor matrix)
    adj = np.array([
        [A[1,1], -A[0,1]],
        [-A[1,0], A[0,0]]
    ]) % p
    
    print(f"3. Adjugate matrix = {adj.tolist()}")
    
    # STEP 4: Calculate inverse matrix = (det_inv × adj) mod p
    A_inv = (det_inv * adj) % p
    print(f"4. Inverse matrix A⁻¹ = {det_inv} × {adj.tolist()} mod {p}")
    print(f"   A⁻¹ = {A_inv.tolist()}")
    
    # STEP 5: Solve for x = A⁻¹ × b mod p
    x = (A_inv @ b) % p
    print(f"5. Solution x = A⁻¹ × b = {A_inv.tolist()} × {b.tolist()} mod {p}")
    print(f"   x = {x.tolist()}")
    
    return x

def oil_and_vinegar_demo():
    """Demo focusing on the inverse calculation"""
    
    p = 97
    w, x = 7, 4
    
    print("🎯 OIL & VINEGAR - INVERSE CALCULATION DEMO")
    print("=" * 60)
    
    # After substituting vinegar variables, we get:
    A = np.array([[14, -2],  # Coefficients for y and z in equation 1
                  [28, 52]]) # Coefficients for y and z in equation 2
    
    b = np.array([10, 34])   # Right-hand side values
    
    print("OUR LINEAR SYSTEM:")
    print(f"14y - 2z = 10 (mod 97)")
    print(f"28y + 52z = 34 (mod 97)")
    print()
    print("IN MATRIX FORM: A × x = b")
    print(f"A = {A.tolist()}")
    print(f"b = {b.tolist()}")
    print()
    
    # This is where the magic happens!
    solution = solve_linear_modular(A, b, p)
    y, z = solution
    
    print("\n" + "=" * 60)
    print(f"🎉 FINAL SOLUTION: y = {y}, z = {z}")
    
    # Verify
    eq1_check = (14*y - 2*z) % p
    eq2_check = (28*y + 52*z) % p
    print(f"✅ Verification:")
    print(f"   Equation 1: 14×{y} - 2×{z} = {eq1_check} (expected: 10)")
    print(f"   Equation 2: 28×{y} + 52×{z} = {eq2_check} (expected: 34)")

def explain_modular_inverse():
    """Extra explanation of modular inverse concept"""
    print("\n" + "🔍 EXTRA: WHAT IS MODULAR INVERSE?")
    print("=" * 50)
    print("In normal math: inverse of 3 is 1/3 because 3 × (1/3) = 1")
    print("In modular math: inverse of 3 mod 97 is a number x such that:")
    print("   3 × x ≡ 1 (mod 97)")
    print()
    print("Let's find it:")
    for x in range(1, 10):
        result = (3 * x) % 97
        print(f"   3 × {x} = {3*x} ≡ {result} mod 97 {'← FOUND!' if result == 1 else ''}")
    
    print("\nSo the modular inverse of 3 mod 97 is 65")
    print("Because 3 × 65 = 195 ≡ 1 mod 97")

if __name__ == "__main__":
    oil_and_vinegar_demo()
    explain_modular_inverse()

"""
🎯 OIL & VINEGAR - INVERSE CALCULATION DEMO
============================================================
OUR LINEAR SYSTEM:
14y - 2z = 10 (mod 97)
28y + 52z = 34 (mod 97)

IN MATRIX FORM: A × x = b
A = [[14, -2], [28, 52]]
b = [10, 34]

🔍 SOLVING LINEAR SYSTEM STEP-BY-STEP:
   A = [[14, -2], [28, 52]]
   b = [10, 34]
   p = 97

1. Determinant = (14×52 - -2×28) mod 97 = 8
2. Modular inverse of 8 mod 97 = 85
   Because 8 × 85 = 680 ≡ 1 mod 97
3. Adjugate matrix = [[52, 2], [69, 14]]
4. Inverse matrix A⁻¹ = 85 × [[52, 2], [69, 14]] mod 97
   A⁻¹ = [[55, 73], [45, 26]]
5. Solution x = A⁻¹ × b = [[55, 73], [45, 26]] × [10, 34] mod 97
   x = [25, 73]

============================================================
🎉 FINAL SOLUTION: y = 25, z = 73
✅ Verification:
   Equation 1: 14×25 - 2×73 = 10 (expected: 10)
   Equation 2: 28×25 + 52×73 = 34 (expected: 34)

🔍 EXTRA: WHAT IS MODULAR INVERSE?
==================================================
In normal math: inverse of 3 is 1/3 because 3 × (1/3) = 1
In modular math: inverse of 3 mod 97 is a number x such that:
   3 × x ≡ 1 (mod 97)

Let's find it:
   3 × 1 = 3 ≡ 3 mod 97 
   3 × 2 = 6 ≡ 6 mod 97 
   3 × 3 = 9 ≡ 9 mod 97 
   3 × 4 = 12 ≡ 12 mod 97 
   3 × 5 = 15 ≡ 15 mod 97 
   3 × 6 = 18 ≡ 18 mod 97 
   3 × 7 = 21 ≡ 21 mod 97 
   3 × 8 = 24 ≡ 24 mod 97 
   3 × 9 = 27 ≡ 27 mod 97 

So the modular inverse of 3 mod 97 is 65
Because 3 × 65 = 195 ≡ 1 mod 97

"""    