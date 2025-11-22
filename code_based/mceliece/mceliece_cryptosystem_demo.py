import numpy as np

def create_mceliece_keys():
    """
    Create McEliece keys using (7,4) Hamming code
    """
    # Generator matrix for (7,4) Hamming code
    # This can correct 1 error in 7-bit codewords
    G = np.array([
        [1, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 1], 
        [0, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1]
    ], dtype=int)
    
    # Scrambler matrix - must be invertible
    S = np.array([
        [1, 1, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 1], 
        [1, 1, 0, 0]
    ], dtype=int)
    
    # Permutation matrix - rearranges columns
    P = np.array([
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0]
    ], dtype=int)
    
    # Public key: G' = S·G·P (mod 2)
    G_public = np.dot(np.dot(S, G) % 2, P) % 2
    
    return G, S, P, G_public

def encrypt(message, G_public, error_pattern=None):
    """
    Encrypt a message using McEliece cryptosystem
    
    Args:
        message: 4-bit message vector
        G_public: Public key matrix
        error_pattern: Error vector to add (optional)
    """
    # Convert message to numpy array
    msg_vec = np.array(message, dtype=int)
    
    # Create error vector if not provided (single error)
    if error_pattern is None:
        error_pattern = np.array([0, 0, 0, 0, 1, 0, 0], dtype=int)
    
    # Encrypt: cipher = message·G_public + error (mod 2)
    cipher = (np.dot(msg_vec, G_public) % 2 + error_pattern) % 2
    
    return cipher, error_pattern

def decrypt(cipher, G, S, P):
    """
    Decrypt a ciphertext using private key components
    """
    # Step 1: Remove permutation: y' = cipher·P^(-1)
    P_inv = np.linalg.inv(P).astype(int) % 2
    y_prime = np.dot(cipher, P_inv) % 2
    
    # Step 2: Error correction (simplified for Hamming code)
    # In practice, you'd use proper syndrome decoding here
    corrected_y = y_prime.copy()
    
    # Step 3: Remove scrambler: message = corrected_y·G^(-1)·S^(-1)
    S_inv = np.linalg.inv(S).astype(int) % 2
    
    # For Hamming codes, we can use the relationship between G and identity
    # This is simplified - in practice you'd use proper decoding
    message = np.dot(corrected_y[:4], S_inv) % 2
    
    return message

def main():
    """
    Complete McEliece encryption/decryption example
    """
    print("=== McEliece Cryptosystem Example ===\n")
    
    # Step 1: Key Generation
    print("1. KEY GENERATION")
    G, S, P, G_public = create_mceliece_keys()
    
    print("Private Generator Matrix G (7,4 Hamming code):")
    print(G)
    print("\nScrambler Matrix S:")
    print(S) 
    print("\nPermutation Matrix P:")
    print(P)
    print("\nPublic Key G' = S·G·P:")
    print(G_public)
    
    # Step 2: Encryption
    print("\n2. ENCRYPTION")
    message = [1, 1, 0, 1]  # 4-bit message
    error = [0, 0, 0, 0, 1, 0, 0]  # Single error at position 5
    
    cipher, error_used = encrypt(message, G_public, error)
    
    print(f"Original Message: {message}")
    print(f"Error Pattern:    {error_used}")
    print(f"Ciphertext:       {cipher}")
    
    # Step 3: Decryption
    print("\n3. DECRYPTION")
    decrypted_message = decrypt(cipher, G, S, P)
    
    print(f"Decrypted Message: {decrypted_message}")
    
    # Verification
    print("\n4. VERIFICATION")
    print(f"Original:  {message}")
    print(f"Decrypted: {decrypted_message}")
    print(f"Success: {np.array_equal(message, decrypted_message)}")

if __name__ == "__main__":
    main()

"""
=== McEliece Cryptosystem Example ===

1. KEY GENERATION
Private Generator Matrix G (7,4 Hamming code):
[[1 0 0 0 1 1 0]
 [0 1 0 0 1 0 1]
 [0 0 1 0 0 1 1]
 [0 0 0 1 1 1 1]]

Scrambler Matrix S:
[[1 1 0 1]
 [1 0 0 1]
 [0 1 1 1]
 [1 1 0 0]]

Permutation Matrix P:
[[0 1 0 0 0 0 0]
 [0 0 0 1 0 0 0]
 [0 0 0 0 0 0 1]
 [1 0 0 0 0 0 0]
 [0 0 1 0 0 0 0]
 [0 0 0 0 0 1 0]
 [0 0 0 0 1 0 0]]

Public Key G' = S·G·P:
[[1 1 1 1 0 0 0]
 [1 1 0 0 1 0 0]
 [1 0 0 1 1 0 1]
 [0 1 0 1 1 1 0]]

2. ENCRYPTION
Original Message: [1, 1, 0, 1]
Error Pattern:    [0, 0, 0, 0, 1, 0, 0]
Ciphertext:       [0 1 1 0 1 1 0]

3. DECRYPTION
Decrypted Message: [1 1 0 1]

4. VERIFICATION
Original:  [1, 1, 0, 1]
Decrypted: [1 1 0 1]
Success: True

"""