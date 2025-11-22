import numpy as np
import sys
import io

class McElieceCryptosystem:
    """
    Enhanced McEliece Cryptosystem using (7,4) Hamming Code
    """
    
    def __init__(self):
        # Generator matrix for (7,4) Hamming code (systematic form)
        self.G = np.array([
            [1, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]
        ], dtype=int)
        
        # Parity check matrix for Hamming code
        self.H = np.array([
            [1, 1, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0], 
            [0, 1, 1, 1, 0, 0, 1]
        ], dtype=int)
        
        # Scrambler matrix (must be invertible)
        self.S = np.array([
            [1, 1, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 1],
            [1, 1, 0, 0]
        ], dtype=int)
        
        # Permutation matrix
        self.P = np.array([
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0]
        ], dtype=int)
        
        # Precompute inverses and public key
        self._precompute_matrices()
        
        # Create syndrome mapping for the PERMUTED code
        self._create_syndrome_mapping()
    
    def _precompute_matrices(self):
        """Precompute inverse matrices and public key"""
        try:
            self.P_inv = np.linalg.inv(self.P).astype(int) % 2
            self.S_inv = np.linalg.inv(self.S).astype(int) % 2
            
            # Public key: G' = S·G·P (mod 2)
            self.G_public = np.dot(np.dot(self.S, self.G) % 2, self.P) % 2
            
        except np.linalg.LinAlgError as e:
            raise ValueError("Matrix inversion failed. Ensure S and P are invertible.") from e
    
    def _create_syndrome_mapping(self):
        """Create syndrome mapping for the permuted code"""
        # For the original Hamming code, create error vectors and compute their syndromes
        self.syndrome_mapping = {}
        
        # Test each single error position in the ORIGINAL code
        for i in range(7):
            error = np.zeros(7, dtype=int)
            error[i] = 1
            syndrome = np.dot(self.H, error) % 2
            syndrome_decimal = syndrome[0] * 4 + syndrome[1] * 2 + syndrome[2]
            self.syndrome_mapping[syndrome_decimal] = i + 1  # 1-indexed
        
        print("Syndrome mapping for original code:")
        for syn, pos in self.syndrome_mapping.items():
            print(f"  Syndrome {syn} (binary {syn:03b}) -> Position {pos}")
    
    def validate_message(self, message):
        """Validate input message"""
        if len(message) != 4:
            raise ValueError(f"Message must be 4 bits long, got {len(message)}")
        if not all(bit in [0, 1] for bit in message):
            raise ValueError("Message must contain only 0s and 1s")
        return np.array(message, dtype=int)
    
    def validate_error(self, error):
        """Validate error vector"""
        if len(error) != 7:
            raise ValueError(f"Error vector must be 7 bits long, got {len(error)}")
        if not all(bit in [0, 1] for bit in error):
            raise ValueError("Error vector must contain only 0s and 1s")
        if sum(error) > 1:  # Hamming code can only correct 1 error
            raise ValueError("Hamming code can only correct single-bit errors")
        return np.array(error, dtype=int)
    
    def encrypt(self, message, error_pattern=None):
        """
        Encrypt a message using McEliece cryptosystem
        
        Args:
            message: 4-bit message vector
            error_pattern: 7-bit error vector (optional, single error recommended)
        
        Returns:
            cipher: Encrypted ciphertext
            error_used: Error pattern applied
        """
        message = self.validate_message(message)
        
        # Default error: single bit error at position 5
        if error_pattern is None:
            error_pattern = [0, 0, 0, 0, 1, 0, 0]
        
        error_used = self.validate_error(error_pattern)
        
        # Encrypt: cipher = message·G_public + error (mod 2)
        cipher = (np.dot(message, self.G_public) % 2 + error_used) % 2
        
        return cipher, error_used
    
    def compute_syndrome(self, vector):
        """
        Compute syndrome for error detection and correction
        
        Args:
            vector: 7-bit vector to compute syndrome for
        
        Returns:
            syndrome: 3-bit syndrome vector
            error_position: Detected error position (1-indexed, 0 if no error)
        """
        syndrome = np.dot(self.H, vector) % 2
        syndrome_decimal = syndrome[0] * 4 + syndrome[1] * 2 + syndrome[2]
        
        # Map syndrome to error position (0 means no error)
        error_position = self.syndrome_mapping.get(syndrome_decimal, 0)
        
        return syndrome, error_position
    
    def correct_error(self, vector, error_position):
        """
        Correct single-bit error at specified position
        
        Args:
            vector: 7-bit vector to correct
            error_position: Position to correct (1-indexed)
        
        Returns:
            corrected_vector: Error-corrected vector
        """
        corrected_vector = vector.copy()
        if error_position > 0:
            corrected_vector[error_position - 1] = (corrected_vector[error_position - 1] + 1) % 2
        return corrected_vector
    
    def decrypt(self, cipher):
        """
        Decrypt a ciphertext using private key components
        
        Args:
            cipher: 7-bit ciphertext vector
        
        Returns:
            decrypted_message: Original 4-bit message
            decryption_info: Dictionary with decryption details
        """
        print("\n=== DECRYPTION PROCESS ===")
        
        # Step 1: Remove permutation to get y' = cipher·P^(-1)
        print("1. Applying inverse permutation P^(-1)")
        y_prime = np.dot(cipher, self.P_inv) % 2
        print(f"   y' = cipher · P^(-1) = {y_prime}")
        
        # Step 2: Compute syndrome on y_prime to find error position
        print("\n2. Syndrome computation on y'")
        syndrome, error_position = self.compute_syndrome(y_prime)
        syndrome_decimal = syndrome[0] * 4 + syndrome[1] * 2 + syndrome[2]
        print(f"   Syndrome: {syndrome} (decimal: {syndrome_decimal})")
        print(f"   Error position in y': {error_position}")
        
        # Step 3: Error correction on y_prime
        print("\n3. Error correction on y'")
        corrected_y = y_prime.copy()
        if error_position > 0:
            corrected_y = self.correct_error(corrected_y, error_position)
            print(f"   Corrected error at position {error_position}")
        else:
            print("   No errors detected")
        print(f"   Corrected y': {corrected_y}")
        
        # Step 4: The corrected y' should equal m·S·G
        # Since G is in systematic form, the first 4 bits of m·S·G equal m·S
        print("\n4. Extracting message from corrected codeword")
        message_times_S = corrected_y[:4]
        print(f"   First 4 bits (m·S): {message_times_S}")
        
        # Step 5: Apply inverse scrambler to recover original message
        print("5. Applying inverse scrambler S^(-1)")
        decrypted_message = np.dot(message_times_S, self.S_inv) % 2
        print(f"   Decrypted = (m·S) · S^(-1) = {decrypted_message}")
        
        # Collect decryption information
        decryption_info = {
            'y_prime': y_prime,
            'syndrome': syndrome,
            'error_position': error_position,
            'corrected_y': corrected_y,
            'message_times_S': message_times_S
        }
        
        return decrypted_message, decryption_info
    
    def print_matrix_info(self, matrix, name):
        """Helper function to print matrix information"""
        print(f"\n{name} ({matrix.shape[0]}x{matrix.shape[1]}):")
        print(matrix)
    
    def demonstrate_workflow(self, message=None, error=None):
        """Complete demonstration of the McEliece workflow"""
        print("=" * 60)
        print("         MCELIECE CRYPTOSYSTEM DEMONSTRATION")
        print("=" * 60)
        
        # Use provided values or defaults
        if message is None:
            message = [1, 1, 0, 0]
        if error is None:
            error = [0, 0, 0, 0, 1, 0, 0]
        
        print(f"\nMESSAGE: {message}")
        print(f"ERROR PATTERN: {error}")
        
        # Print key information
        print("\n=== KEY INFORMATION ===")
        self.print_matrix_info(self.G, "Generator Matrix G")
        self.print_matrix_info(self.H, "Parity Check Matrix H")
        self.print_matrix_info(self.S, "Scrambler Matrix S")
        self.print_matrix_info(self.P, "Permutation Matrix P")
        self.print_matrix_info(self.G_public, "Public Key G' = S·G·P")
        self.print_matrix_info(self.S_inv, "Inverse Scrambler S^(-1)")
        self.print_matrix_info(self.P_inv, "Inverse Permutation P^(-1)")
        
        # Verify S·S^(-1) = I
        identity_check_S = np.dot(self.S, self.S_inv) % 2
        print(f"\nVerification S·S^(-1) = I: {np.array_equal(identity_check_S, np.eye(4, dtype=int))}")
        
        # Verify P·P^(-1) = I  
        identity_check_P = np.dot(self.P, self.P_inv) % 2
        print(f"Verification P·P^(-1) = I: {np.array_equal(identity_check_P, np.eye(7, dtype=int))}")
        
        # Step-by-step encryption demonstration
        print("\n=== ENCRYPTION (Step by Step) ===")
        print(f"1. Original message m: {message}")
        
        # m·S
        mS = np.dot(message, self.S) % 2
        print(f"2. m·S: {mS}")
        
        # m·S·G (codeword in original code)
        mSG = np.dot(mS, self.G) % 2
        print(f"3. m·S·G (codeword): {mSG}")
        
        # m·S·G·P (permuted codeword)
        mSGP = np.dot(mSG, self.P) % 2
        print(f"4. m·S·G·P (permuted): {mSGP}")
        
        # Add error
        cipher = (mSGP + error) % 2
        print(f"5. Add error {error}: {cipher}")
        
        # Also compute using public key for verification
        cipher_public, error_used = self.encrypt(message, error)
        print(f"6. Using public key: {cipher_public}")
        print(f"   Match: {np.array_equal(cipher, cipher_public)}")
        
        # Decryption
        decrypted_message, decryption_info = self.decrypt(cipher)
        
        # Results
        print("\n" + "=" * 40)
        print("FINAL RESULTS")
        print("=" * 40)
        print(f"Original message:  {message}")
        print(f"Decrypted message: {decrypted_message}")
        success = np.array_equal(message, decrypted_message)
        print(f"Success: {success}")
        
        if not success:
            print("\nDEBUGGING INFO:")
            print(f"m·S (expected): {mS}")
            print(f"m·S (actual):   {decryption_info['message_times_S']}")
            print(f"Match: {np.array_equal(mS, decryption_info['message_times_S'])}")
        
        return {
            'original_message': message,
            'ciphertext': cipher,
            'decrypted_message': decrypted_message,
            'success': success,
            'decryption_info': decryption_info
        }


def parse_command_line_message():
    """Parse message from command line with proper error handling"""
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        try:
            # Remove brackets and split by commas
            msg_str = sys.argv[1].replace('[', '').replace(']', '').replace('(', '').replace(')', '')
            message = [int(x.strip()) for x in msg_str.split(',')]
            
            if len(message) != 4:
                print(f"Warning: Message should be 4 bits, got {len(message)}. Using default.")
                return [1, 1, 0, 0]
            
            print("Using command line message:", message)
            return message
        except (ValueError, IndexError) as e:
            print(f"Error parsing command line argument: {e}")
            print("Using default message...")
    return [1, 1, 0, 0]


def run_comprehensive_tests():
    """Run comprehensive tests of the cryptosystem"""
    crypto = McElieceCryptosystem()
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE ERROR CORRECTION TESTS")
    print("=" * 60)
    
    test_message = [1, 0, 1, 0]
    test_cases = [
        ([0, 0, 0, 0, 0, 0, 0], "No error"),
        ([1, 0, 0, 0, 0, 0, 0], "Error at position 1"),
        ([0, 1, 0, 0, 0, 0, 0], "Error at position 2"), 
        ([0, 0, 1, 0, 0, 0, 0], "Error at position 3"),
        ([0, 0, 0, 1, 0, 0, 0], "Error at position 4"),
        ([0, 0, 0, 0, 1, 0, 0], "Error at position 5"),
        ([0, 0, 0, 0, 0, 1, 0], "Error at position 6"),
        ([0, 0, 0, 0, 0, 0, 1], "Error at position 7"),
    ]
    
    results = []
    
    for error_pattern, description in test_cases:
        try:
            print(f"\n--- Test: {description} ---")
            print(f"Message: {test_message}, Error: {error_pattern}")
            
            # Encrypt
            cipher, _ = crypto.encrypt(test_message, error_pattern)
            print(f"Ciphertext: {cipher}")
            
            # Decrypt
            decrypted, info = crypto.decrypt(cipher)
            
            # Verify
            success = np.array_equal(test_message, decrypted)
            status = "✓ SUCCESS" if success else "✗ FAILED"
            print(f"Result: {status}")
            
            results.append({
                'test': description,
                'success': success,
                'error_pattern': error_pattern,
                'decrypted': decrypted
            })
            
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({
                'test': description, 
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    successful_tests = sum(1 for r in results if r['success'])
    print(f"Successful tests: {successful_tests}/{len(results)}")
    
    for result in results:
        status = "✓" if result['success'] else "✗"
        print(f"{status} {result['test']}")
    
    return results


def main():
    """Main function with command line support"""
    # Parse command line message first (ignore flags like -f)
    message = parse_command_line_message()
    
    # Run main demonstration
    crypto = McElieceCryptosystem()
    print("\n" + "=" * 60)
    print("MAIN DEMONSTRATION")
    print("=" * 60)
    result = crypto.demonstrate_workflow(message)
    
    # Run comprehensive tests
    test_results = run_comprehensive_tests()
    
    # Final verification
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION")
    print("=" * 60)
    if result['success']:
        print("✓ Main demonstration: SUCCESS")
    else:
        print("✗ Main demonstration: FAILED")
        print("Debug information has been printed above")
    
    successful_tests = sum(1 for r in test_results if r['success'])
    print(f"✓ Error correction tests: {successful_tests}/{len(test_results)} successful")


if __name__ == "__main__":
    main()

"""
Syndrome mapping for original code:
  Syndrome 6 (binary 110) -> Position 1
  Syndrome 5 (binary 101) -> Position 2
  Syndrome 3 (binary 011) -> Position 3
  Syndrome 7 (binary 111) -> Position 4
  Syndrome 4 (binary 100) -> Position 5
  Syndrome 2 (binary 010) -> Position 6
  Syndrome 1 (binary 001) -> Position 7

============================================================
MAIN DEMONSTRATION
============================================================
============================================================
         MCELIECE CRYPTOSYSTEM DEMONSTRATION
============================================================

MESSAGE: [1, 1, 0, 0]
ERROR PATTERN: [0, 0, 0, 0, 1, 0, 0]

=== KEY INFORMATION ===

Generator Matrix G (4x7):
[[1 0 0 0 1 1 0]
 [0 1 0 0 1 0 1]
 [0 0 1 0 0 1 1]
 [0 0 0 1 1 1 1]]

Parity Check Matrix H (3x7):
[[1 1 0 1 1 0 0]
 [1 0 1 1 0 1 0]
 [0 1 1 1 0 0 1]]

Scrambler Matrix S (4x4):
[[1 1 0 1]
 [1 0 0 1]
 [0 1 1 1]
 [1 1 0 0]]

Permutation Matrix P (7x7):
[[0 1 0 0 0 0 0]
 [0 0 0 1 0 0 0]
 [0 0 0 0 0 0 1]
 [1 0 0 0 0 0 0]
 [0 0 1 0 0 0 0]
 [0 0 0 0 0 1 0]
 [0 0 0 0 1 0 0]]

Public Key G' = S·G·P (4x7):
[[1 1 1 1 0 0 0]
 [1 1 0 0 1 0 0]
 [1 0 0 1 1 0 1]
 [0 1 0 1 1 1 0]]

Inverse Scrambler S^(-1) (4x4):
[[1 1 0 1]
 [1 1 0 0]
 [0 1 1 1]
 [1 0 0 1]]

Inverse Permutation P^(-1) (7x7):
[[0 0 0 1 0 0 0]
 [1 0 0 0 0 0 0]
 [0 0 0 0 1 0 0]
 [0 1 0 0 0 0 0]
 [0 0 0 0 0 0 1]
 [0 0 0 0 0 1 0]
 [0 0 1 0 0 0 0]]

Verification S·S^(-1) = I: True
Verification P·P^(-1) = I: True

=== ENCRYPTION (Step by Step) ===
1. Original message m: [1, 1, 0, 0]
2. m·S: [0 1 0 0]
3. m·S·G (codeword): [0 1 0 0 1 0 1]
4. m·S·G·P (permuted): [0 0 1 1 1 0 0]
5. Add error [0, 0, 0, 0, 1, 0, 0]: [0 0 1 1 0 0 0]
6. Using public key: [0 0 1 1 0 0 0]
   Match: True

=== DECRYPTION PROCESS ===
1. Applying inverse permutation P^(-1)
   y' = cipher · P^(-1) = [0 1 0 0 1 0 0]

2. Syndrome computation on y'
   Syndrome: [0 0 1] (decimal: 1)
   Error position in y': 7

3. Error correction on y'
   Corrected error at position 7
   Corrected y': [0 1 0 0 1 0 1]

4. Extracting message from corrected codeword
   First 4 bits (m·S): [0 1 0 0]
5. Applying inverse scrambler S^(-1)
   Decrypted = (m·S) · S^(-1) = [1 1 0 0]

========================================
FINAL RESULTS
========================================
Original message:  [1, 1, 0, 0]
Decrypted message: [1 1 0 0]
Success: True
Syndrome mapping for original code:
  Syndrome 6 (binary 110) -> Position 1
  Syndrome 5 (binary 101) -> Position 2
  Syndrome 3 (binary 011) -> Position 3
  Syndrome 7 (binary 111) -> Position 4
  Syndrome 4 (binary 100) -> Position 5
  Syndrome 2 (binary 010) -> Position 6
  Syndrome 1 (binary 001) -> Position 7

============================================================
COMPREHENSIVE ERROR CORRECTION TESTS
============================================================

--- Test: No error ---
Message: [1, 0, 1, 0], Error: [0, 0, 0, 0, 0, 0, 0]
Ciphertext: [0 1 1 0 1 0 1]

=== DECRYPTION PROCESS ===
1. Applying inverse permutation P^(-1)
   y' = cipher · P^(-1) = [1 0 1 0 1 0 1]

2. Syndrome computation on y'
   Syndrome: [0 0 0] (decimal: 0)
   Error position in y': 0

3. Error correction on y'
   No errors detected
   Corrected y': [1 0 1 0 1 0 1]

4. Extracting message from corrected codeword
   First 4 bits (m·S): [1 0 1 0]
5. Applying inverse scrambler S^(-1)
   Decrypted = (m·S) · S^(-1) = [1 0 1 0]
Result: ✓ SUCCESS

--- Test: Error at position 1 ---
Message: [1, 0, 1, 0], Error: [1, 0, 0, 0, 0, 0, 0]
Ciphertext: [1 1 1 0 1 0 1]

=== DECRYPTION PROCESS ===
1. Applying inverse permutation P^(-1)
   y' = cipher · P^(-1) = [1 0 1 1 1 0 1]

2. Syndrome computation on y'
   Syndrome: [1 1 1] (decimal: 7)
   Error position in y': 4

3. Error correction on y'
   Corrected error at position 4
   Corrected y': [1 0 1 0 1 0 1]

4. Extracting message from corrected codeword
   First 4 bits (m·S): [1 0 1 0]
5. Applying inverse scrambler S^(-1)
   Decrypted = (m·S) · S^(-1) = [1 0 1 0]
Result: ✓ SUCCESS

--- Test: Error at position 2 ---
Message: [1, 0, 1, 0], Error: [0, 1, 0, 0, 0, 0, 0]
Ciphertext: [0 0 1 0 1 0 1]

=== DECRYPTION PROCESS ===
1. Applying inverse permutation P^(-1)
   y' = cipher · P^(-1) = [0 0 1 0 1 0 1]

2. Syndrome computation on y'
   Syndrome: [1 1 0] (decimal: 6)
   Error position in y': 1

3. Error correction on y'
   Corrected error at position 1
   Corrected y': [1 0 1 0 1 0 1]

4. Extracting message from corrected codeword
   First 4 bits (m·S): [1 0 1 0]
5. Applying inverse scrambler S^(-1)
   Decrypted = (m·S) · S^(-1) = [1 0 1 0]
Result: ✓ SUCCESS

--- Test: Error at position 3 ---
Message: [1, 0, 1, 0], Error: [0, 0, 1, 0, 0, 0, 0]
Ciphertext: [0 1 0 0 1 0 1]

=== DECRYPTION PROCESS ===
1. Applying inverse permutation P^(-1)
   y' = cipher · P^(-1) = [1 0 1 0 0 0 1]

2. Syndrome computation on y'
   Syndrome: [1 0 0] (decimal: 4)
   Error position in y': 5

3. Error correction on y'
   Corrected error at position 5
   Corrected y': [1 0 1 0 1 0 1]

4. Extracting message from corrected codeword
   First 4 bits (m·S): [1 0 1 0]
5. Applying inverse scrambler S^(-1)
   Decrypted = (m·S) · S^(-1) = [1 0 1 0]
Result: ✓ SUCCESS

--- Test: Error at position 4 ---
Message: [1, 0, 1, 0], Error: [0, 0, 0, 1, 0, 0, 0]
Ciphertext: [0 1 1 1 1 0 1]

=== DECRYPTION PROCESS ===
1. Applying inverse permutation P^(-1)
   y' = cipher · P^(-1) = [1 1 1 0 1 0 1]

2. Syndrome computation on y'
   Syndrome: [1 0 1] (decimal: 5)
   Error position in y': 2

3. Error correction on y'
   Corrected error at position 2
   Corrected y': [1 0 1 0 1 0 1]

4. Extracting message from corrected codeword
   First 4 bits (m·S): [1 0 1 0]
5. Applying inverse scrambler S^(-1)
   Decrypted = (m·S) · S^(-1) = [1 0 1 0]
Result: ✓ SUCCESS

--- Test: Error at position 5 ---
Message: [1, 0, 1, 0], Error: [0, 0, 0, 0, 1, 0, 0]
Ciphertext: [0 1 1 0 0 0 1]

=== DECRYPTION PROCESS ===
1. Applying inverse permutation P^(-1)
   y' = cipher · P^(-1) = [1 0 1 0 1 0 0]

2. Syndrome computation on y'
   Syndrome: [0 0 1] (decimal: 1)
   Error position in y': 7

3. Error correction on y'
   Corrected error at position 7
   Corrected y': [1 0 1 0 1 0 1]

4. Extracting message from corrected codeword
   First 4 bits (m·S): [1 0 1 0]
5. Applying inverse scrambler S^(-1)
   Decrypted = (m·S) · S^(-1) = [1 0 1 0]
Result: ✓ SUCCESS

--- Test: Error at position 6 ---
Message: [1, 0, 1, 0], Error: [0, 0, 0, 0, 0, 1, 0]
Ciphertext: [0 1 1 0 1 1 1]

=== DECRYPTION PROCESS ===
1. Applying inverse permutation P^(-1)
   y' = cipher · P^(-1) = [1 0 1 0 1 1 1]

2. Syndrome computation on y'
   Syndrome: [0 1 0] (decimal: 2)
   Error position in y': 6

3. Error correction on y'
   Corrected error at position 6
   Corrected y': [1 0 1 0 1 0 1]

4. Extracting message from corrected codeword
   First 4 bits (m·S): [1 0 1 0]
5. Applying inverse scrambler S^(-1)
   Decrypted = (m·S) · S^(-1) = [1 0 1 0]
Result: ✓ SUCCESS

--- Test: Error at position 7 ---
Message: [1, 0, 1, 0], Error: [0, 0, 0, 0, 0, 0, 1]
Ciphertext: [0 1 1 0 1 0 0]

=== DECRYPTION PROCESS ===
1. Applying inverse permutation P^(-1)
   y' = cipher · P^(-1) = [1 0 0 0 1 0 1]

2. Syndrome computation on y'
   Syndrome: [0 1 1] (decimal: 3)
   Error position in y': 3

3. Error correction on y'
   Corrected error at position 3
   Corrected y': [1 0 1 0 1 0 1]

4. Extracting message from corrected codeword
   First 4 bits (m·S): [1 0 1 0]
5. Applying inverse scrambler S^(-1)
   Decrypted = (m·S) · S^(-1) = [1 0 1 0]
Result: ✓ SUCCESS

==================================================
TEST SUMMARY
==================================================
Successful tests: 8/8
✓ No error
✓ Error at position 1
✓ Error at position 2
✓ Error at position 3
✓ Error at position 4
✓ Error at position 5
✓ Error at position 6
✓ Error at position 7

============================================================
FINAL VERIFICATION
============================================================
✓ Main demonstration: SUCCESS
✓ Error correction tests: 8/8 successful

"""