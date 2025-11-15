import math
from math import gcd
from operator import add, neg
from fractions import Fraction as frac

# ==================== HELPER FUNCTIONS ====================

def extended_gcd(a, b):
    """Extended Euclidean Algorithm for integers"""
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return b, x, y

def mod_inverse(a, m):
    """Find modular inverse using extended GCD"""
    gcd_val, x, y = extended_gcd(a, m)
    if gcd_val != 1:
        return None  # modular inverse does not exist
    return x % m

def fraction_mod(f, m):
    """Handle fraction modulo operations"""
    gcd_val, _, _ = extended_gcd(f.denominator, m)
    if gcd_val != 1:
        raise ValueError("GCD of denominator and modulus is not 1")
    return mod_inverse(f.denominator, m) * f.numerator % m

# ==================== POLYNOMIAL OPERATIONS ====================

def resize_polynomials(poly1, poly2):
    """Add leading zeros to make polynomials same length"""
    if len(poly1) > len(poly2):
        poly2 = poly2 + [0] * (len(poly1) - len(poly2))
    if len(poly1) < len(poly2):
        poly1 = poly1 + [0] * (len(poly2) - len(poly1))
    return [poly1, poly2]

def trim_polynomial(poly):
    """Remove leading zeros from polynomial"""
    if not poly:
        return poly
    for i in range(len(poly) - 1, -1, -1):
        if poly[i] != 0:
            break
    return poly[0:i+1]

def add_polynomials(poly1, poly2):
    """Add two polynomials"""
    poly1, poly2 = resize_polynomials(poly1, poly2)
    result = list(map(add, poly1, poly2))
    return trim_polynomial(result)

def subtract_polynomials(poly1, poly2):
    """Subtract two polynomials"""
    poly1, poly2 = resize_polynomials(poly1, poly2)
    poly2_neg = list(map(neg, poly2))
    result = list(map(add, poly1, poly2_neg))
    return trim_polynomial(result)

def multiply_polynomials(poly1, poly2):
    """Multiply two polynomials"""
    degree = (len(poly1) - 1 + len(poly2) - 1)
    result = [0] * (degree + 1)
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[j + i] += poly1[i] * poly2[j]
    return trim_polynomial(result)

def divide_polynomials(numerator, denominator):
    """Divide two polynomials"""
    num = list(map(frac, trim_polynomial(numerator)))
    den = list(map(frac, trim_polynomial(denominator)))
    deg_num, deg_den = len(num) - 1, len(den) - 1
    
    if deg_num >= deg_den:
        quotient = [0] * (deg_num - deg_den + 1)
        while deg_num >= deg_den and num != [0]:
            d = list(den)
            [d.insert(0, frac(0, 1)) for _ in range(deg_num - deg_den)]
            quotient[deg_num - deg_den] = num[deg_num] / d[len(d) - 1]
            d = [x * quotient[deg_num - deg_den] for x in d]
            num = subtract_polynomials(num, d)
            deg_num = len(num) - 1
        remainder = num
    else:
        quotient = [0]
        remainder = num
    return [trim_polynomial(quotient), trim_polynomial(remainder)]

def mod_polynomial(poly, modulus):
    """Apply modulus to polynomial coefficients"""
    if modulus == 0:
        raise ValueError("Modulus must be non-zero")
    return [fraction_mod(x, modulus) for x in poly]

def center_lift_polynomial(poly, q):
    """Center lift polynomial coefficients"""
    if isinstance(q, int):
        upper = q / 2.0
        lower = -upper
    else:
        upper = float(q) / 2.0
        lower = -upper
        
    poly_mod = mod_polynomial(poly, q)
    result = []
    for x in poly_mod:
        if isinstance(x, int):
            x_val = x
        else:
            x_val = float(x)
            
        if x_val > upper:
            result.append(x % -q)
        elif x_val <= lower:
            result.append(x % q)
        else:
            result.append(x)
    return result

def extended_euclid_polynomial(a, b):
    """Extended Euclidean Algorithm for polynomials"""
    a_trim = trim_polynomial(a)
    b_trim = trim_polynomial(b)
    
    # Ensure a has higher degree than b
    swapped = False
    if len(a_trim) >= len(b_trim):
        a1, b1 = a_trim, b_trim
    else:
        a1, b1 = b_trim, a_trim
        swapped = True

    quotients, remainders = [], []
    while b1 != [0]:
        q, r = divide_polynomials(a1, b1)
        quotients.append(q)
        remainders.append(r)
        a1, b1 = b1, r

    # Initialize S and T arrays
    S = [[1], [0]]
    T = [[0], [1]]

    for i in range(2, len(quotients) + 2):
        S.append(subtract_polynomials(S[i-2], multiply_polynomials(quotients[i-2], S[i-1])))
        T.append(subtract_polynomials(T[i-2], multiply_polynomials(quotients[i-2], T[i-1])))

    gcd_poly = remainders[-2]
    s_out = S[-2]
    t_out = T[-2]

    # Scale so leading coefficient is 1
    scale = gcd_poly[-1]
    gcd_poly = [x / scale for x in gcd_poly]
    s_out = [x / scale for x in s_out]
    t_out = [x / scale for x in t_out]

    if swapped:
        return [gcd_poly, t_out, s_out]
    else:
        return [gcd_poly, s_out, t_out]

def is_ternary(poly, ones_count, neg_ones_count):
    """Check if polynomial is ternary (only -1, 0, 1 coefficients)"""
    ones = sum(1 for x in poly if x == 1)
    neg_ones = sum(1 for x in poly if x == -1)
    return (ones + neg_ones) <= len(poly) and ones == ones_count and neg_ones == neg_ones_count

# ==================== NTRU ENCRYPTION CLASS ====================

class NTRU:
    def __init__(self, N, p, q):
        self.N = N
        self.p = p
        self.q = q
        self.f = None
        self.g = None
        self.h = None
        self.f_p = None
        self.f_q = None
        # Polynomial modulus: x^N - 1
        self.D = [-1] + [0] * (N - 1) + [1]
    
    def generate_public_key(self, f, g, d):
        """Generate public key from private polynomials f and g"""
        self.f = f
        self.g = g
        
        # Compute inverses modulo p and q
        gcd_poly, s_f, _ = extended_euclid_polynomial(f, self.D)
        self.f_p = mod_polynomial(s_f, self.p)
        self.f_q = mod_polynomial(s_f, self.q)
        
        # Public key: h = f_q * g mod q
        h_temp = multiply_polynomials(self.f_q, g)
        self.h = self._reduce_modulo(h_temp, self.D, self.q)
    
    def get_public_key(self):
        return self.h
    
    def set_public_key(self, public_key):
        self.h = public_key
    
    def encrypt(self, message, random_poly):
        """Encrypt message using public key and random polynomial"""
        if self.h is None:
            raise ValueError("Public key not set!")
        
        # Encryption: e = p * random * h + message mod q
        term1 = multiply_polynomials([self.p], random_poly)
        term2 = multiply_polynomials(term1, self.h)
        e_temp = add_polynomials(term2, message)
        return self._reduce_modulo(e_temp, self.D, self.q)
    
    def decrypt(self, encrypted_message):
        """Decrypt message using private key"""
        # Step 1: a = f * e mod q
        a_temp = multiply_polynomials(self.f, encrypted_message)
        a = self._reduce_modulo(a_temp, self.D, self.q)
        
        # Step 2: Center lift
        a_centered = center_lift_polynomial(a, self.q)
        
        # Step 3: m = f_p * a mod p
        m_temp = multiply_polynomials(self.f_p, a_centered)
        m = self._reduce_modulo(m_temp, self.D, self.p)
        
        return trim_polynomial(m)
    
    def _reduce_modulo(self, poly, divisor, modulus):
        """Reduce polynomial modulo divisor and modulus"""
        _, remainder = divide_polynomials(poly, divisor)
        return mod_polynomial(remainder, modulus)
    
    def validate_parameters(self, d):
        """Validate NTRU parameters"""
        if not self._is_prime(self.N):
            raise ValueError("N must be prime")
        if gcd(self.N, self.p) != 1:
            raise ValueError("gcd(N, p) must be 1")
        if gcd(self.N, self.q) != 1:
            raise ValueError("gcd(N, q) must be 1")
        if self.q <= (6 * d + 1) * self.p:
            raise ValueError("q must be > (6*d + 1)*p")
        if not is_ternary(self.f, d + 1, d):
            raise ValueError("f must be ternary with d+1 ones and d negative ones")
        if not is_ternary(self.g, d, d):
            raise ValueError("g must be ternary with d ones and d negative ones")
        return True
    
    def _is_prime(self, n):
        """Check if number is prime"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        return all(n % i != 0 for i in range(3, int(math.sqrt(n)) + 1, 2))

# ==================== DEMONSTRATION ====================

def demonstrate_ntru():
    print("=== NTRU Encryption Demo ===\n")
    
    # Parameters
    N, p, q = 7, 29, 491531
    
    print("Parameters:")
    print(f"N = {N}, p = {p}, q = {q}\n")
    
    # Bob generates keys
    print("=== Bob Generates Keys ===")
    bob = NTRU(N, p, q)
    
    f = [1, 1, -1, 0, -1, 1]      # Bob's private key
    g = [-1, 0, 1, 1, 0, 0, -1]   # Used to generate public key
    d = 2
    
    print(f"Private f: {f}")
    print(f"Private g: {g}")
    
    bob.generate_public_key(f, g, d)
    public_key = bob.get_public_key()
    print(f"Public Key: {public_key}\n")
    
    # Alice encrypts
    print("=== Alice Encrypts ===")
    alice = NTRU(N, p, q)
    alice.set_public_key(public_key)
    
    message = [1, 0, 1, 0, 1, 1, 1]
    random_poly = [-1, -1, 1, 1]
    
    print(f"Message: {message}")
    print(f"Random: {random_poly}")
    
    encrypted = alice.encrypt(message, random_poly)
    print(f"Encrypted: {encrypted}\n")
    
    # Bob decrypts
    print("=== Bob Decrypts ===")
    decrypted = bob.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    
    # Verify
    if message == decrypted:
        print("✅ SUCCESS: Decryption correct!")
    else:
        print("❌ FAILURE: Decryption failed!")

if __name__ == "__main__":
    demonstrate_ntru()


"""
=== NTRU Encryption Demo ===

Parameters:
N = 7, p = 29, q = 491531

=== Bob Generates Keys ===
Private f: [1, 1, -1, 0, -1, 1]
Private g: [-1, 0, 1, 1, 0, 0, -1]
Public Key: [394609, 27692, 62307, 263073, 346149, 41538, 339225]

=== Alice Encrypts ===
Message: [1, 0, 1, 0, 1, 1, 1]
Random: [-1, -1, 1, 1]
Encrypted: [283889, 269991, 484569, 353054, 179995, 159222, 235409]

=== Bob Decrypts ===
Decrypted: [1, 0, 1, 0, 1, 1, 1]
✅ SUCCESS: Decryption correct!

"""    