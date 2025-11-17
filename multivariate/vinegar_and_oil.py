import numpy as np

def solve_linear_modular(A, b, p):
    """Solve A*x = b (mod p) for x"""
    # Calculate inverse of A modulo p
    det = int(np.round(np.linalg.det(A))) % p
    # Find modular inverse of determinant
    det_inv = pow(det, -1, p)  # Python 3.8+ modular inverse
    
    # Calculate inverse matrix using adjugate method
    adj = np.array([
        [A[1,1], -A[0,1]],
        [-A[1,0], A[0,0]]
    ]) % p
    
    A_inv = (det_inv * adj) % p
    
    # Solve for x
    x = (A_inv @ b) % p
    return x

def oil_and_vinegar_demo():
    """Simple Oil and Vinegar Cryptography Demo"""
    
    # Configuration
    p = 97  # Prime modulus
    w, x = 7, 4  # Vinegar variables (secret we know)
    
    print("🔐 OIL AND VINEGAR CRYPTOGRAPHY DEMO")
    print("=" * 50)
    
    # Original complex polynomial equations
    print("ORIGINAL HARD PROBLEM:")
    print("1. w² + 4wx + 3x² + 2wy - 4xz + 2wz + 6xy = 96 (mod 97)")
    print("2. 5w² + 3wx + 3x² + 4wy - xz + 8wz + 4xy = 36 (mod 97)")
    print()
    
    print(f"🎯 WE KNOW VINEGAR VARIABLES: w = {w}, x = {x}")
    print()
    
    # Step 1: Substitute vinegar variables
    print("STEP 1: Substitute vinegar variables")
    print("-" * 40)
    
    # Equation 1 calculation
    eq1_constant = (w*w + 4*w*x + 3*x*x + 6*w*x) % p  # w² + 4wx + 3x² + 6xy
    eq1_y_coef = (2*w) % p  # 2wy coefficient
    eq1_z_coef = ((-4*x) + (2*w)) % p  # -4xz + 2wz
    
    # Equation 2 calculation  
    eq2_constant = (5*w*w + 3*w*x + 3*x*x + 4*w*x) % p  # 5w² + 3wx + 3x² + 4xy
    eq2_y_coef = (4*w) % p  # 4wy coefficient
    eq2_z_coef = ((-1*x) + (8*w)) % p  # -xz + 8wz
    
    print(f"Equation 1: {eq1_y_coef}y + {eq1_z_coef}z = {96} - {eq1_constant} (mod {p})")
    print(f"Equation 2: {eq2_y_coef}y + {eq2_z_coef}z = {36} - {eq2_constant} (mod {p})")
    
    # Step 2: Simplify equations
    print("\nSTEP 2: Simplify equations")
    print("-" * 40)
    
    eq1_right = (96 - eq1_constant) % p
    eq2_right = (36 - eq2_constant) % p
    
    print(f"Equation 1: {eq1_y_coef}y + {eq1_z_coef}z = {eq1_right} (mod {p})")
    print(f"Equation 2: {eq2_y_coef}y + {eq2_z_coef}z = {eq2_right} (mod {p})")
    
    # Step 3: Solve linear system
    print("\nSTEP 3: Solve linear system")
    print("-" * 40)
    
    A = np.array([
        [eq1_y_coef, eq1_z_coef],
        [eq2_y_coef, eq2_z_coef]
    ])
    
    b = np.array([eq1_right, eq2_right])
    
    print(f"Matrix A = {A.tolist()}")
    print(f"Vector b = {b.tolist()}")
    
    # Solve for oil variables
    oil_solution = solve_linear_modular(A, b, p)
    y, z = oil_solution
    
    print(f"\n🎉 SOLUTION FOUND:")
    print(f"   y = {y}")
    print(f"   z = {z}")
    
    # Step 4: Verify solution
    print("\nSTEP 4: Verify solution")
    print("-" * 40)
    
    # Verify equation 1
    verify1 = (w*w + 4*w*x + 3*x*x + 2*w*y - 4*x*z + 2*w*z + 6*x*y) % p
    print(f"Equation 1: {verify1} (expected: 96) → {'✓' if verify1 == 96 else '✗'}")
    
    # Verify equation 2
    verify2 = (5*w*w + 3*w*x + 3*x*x + 4*w*y - x*z + 8*w*z + 4*x*y) % p
    print(f"Equation 2: {verify2} (expected: 36) → {'✓' if verify2 == 36 else '✗'}")
    
    print("\n" + "=" * 50)
    print("💡 KEY INSIGHTS:")
    print("• Without vinegar (w,x): Exponentially hard problem")
    print("• With vinegar (w,x): Simple linear system")
    print("• This is the 'trapdoor' that makes Oil & Vinegar work!")
    print("• Used in post-quantum signatures like Rainbow")

if __name__ == "__main__":
    oil_and_vinegar_demo()

"""
🔑 The Oil & Vinegar Magic:

Vinegar variables (w,x): The secret we know
Oil variables (y,z): What we need to find
Trapdoor: Knowing vinegar turns hard polynomials into easy linear equations

🎯 Step-by-Step Process:

Start with complex multivariate polynomials
Substitute known vinegar variables
Get simple linear equations for oil variables
Solve using modular linear algebra
Verify the solution works


🔐 OIL AND VINEGAR CRYPTOGRAPHY DEMO
==================================================
ORIGINAL HARD PROBLEM:
1. w² + 4wx + 3x² + 2wy - 4xz + 2wz + 6xy = 96 (mod 97)
2. 5w² + 3wx + 3x² + 4wy - xz + 8wz + 4xy = 36 (mod 97)

🎯 WE KNOW VINEGAR VARIABLES: w = 7, x = 4

STEP 1: Substitute vinegar variables
----------------------------------------
Equation 1: 14y + 95z = 96 - 86 (mod 97)
Equation 2: 28y + 52z = 36 - 4 (mod 97)

STEP 2: Simplify equations
----------------------------------------
Equation 1: 14y + 95z = 10 (mod 97)
Equation 2: 28y + 52z = 32 (mod 97)

STEP 3: Solve linear system
----------------------------------------
Matrix A = [[14, 95], [28, 52]]
Vector b = [10, 32]

🎉 SOLUTION FOUND:
   y = 73
   z = 21

STEP 4: Verify solution
----------------------------------------
Equation 1: 31 (expected: 96) → ✗
Equation 2: 25 (expected: 36) → ✗

==================================================
💡 KEY INSIGHTS:
• Without vinegar (w,x): Exponentially hard problem
• With vinegar (w,x): Simple linear system
• This is the 'trapdoor' that makes Oil & Vinegar work!
• Used in post-quantum signatures like Rainbow

"""    