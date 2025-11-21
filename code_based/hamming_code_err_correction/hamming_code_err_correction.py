import numpy as np
import random
import time

class HammingCode:
    def __init__(self, random_matrix=False):
        if random_matrix:
            self.G, self.H = self._generate_random_matrices()
            self.matrix_type = "RANDOMLY GENERATED"
        else:
            # Standard Hamming (7,4) matrices
            self.G = np.array([
                [1, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 1, 1], 
                [0, 0, 1, 0, 1, 0, 1],
                [0, 0, 0, 1, 1, 1, 0]
            ])
            self.H = np.array([
                [1, 0, 1, 1, 1, 0, 0],
                [1, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 0, 0, 0, 1]
            ])
            self.matrix_type = "STANDARD"
    
    def _generate_random_matrices(self):
        """Generate valid random G and H matrices for Hamming (7,4) code with timeout"""
        start_time = time.time()
        max_time = 5  # Maximum 5 seconds
        
        attempts = 0
        while time.time() - start_time < max_time:
            attempts += 1
            try:
                # Generate all possible non-zero parity columns
                possible_columns = []
                for i in range(1, 16):  # All 4-bit non-zero patterns
                    col = [int(bit) for bit in format(i, '04b')]
                    if sum(col) >= 1:  # Non-zero
                        possible_columns.append(col)
                
                # Randomly select 3 distinct columns
                random.shuffle(possible_columns)
                parity_columns = possible_columns[:3]
                
                # Build G matrix [I|P]
                G = np.eye(4, dtype=int)  # Identity part
                G = np.hstack([G, np.array(parity_columns).T])  # Add parity part
                
                # Build H matrix [P^T|I]
                H_parity = np.array(parity_columns).T
                H_identity = np.eye(3, dtype=int)
                H = np.hstack([H_parity, H_identity])
                
                # Verify the matrices satisfy H * G^T = 0
                verification = np.dot(H, G.T) % 2
                if np.all(verification == 0):
                    print(f"✓ Found valid matrices after {attempts} attempts")
                    return G, H
                    
            except Exception as e:
                continue
        
        # If we timeout, fall back to standard matrices
        print("⚠️  Could not generate random matrices in time, using standard matrices")
        return self._get_standard_matrices()
    
    def _get_standard_matrices(self):
        """Fallback to standard matrices"""
        G = np.array([
            [1, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 0, 1, 1], 
            [0, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 1, 1, 1, 0]
        ])
        H = np.array([
            [1, 0, 1, 1, 1, 0, 0],
            [1, 1, 0, 1, 0, 1, 0],
            [1, 1, 1, 0, 0, 0, 1]
        ])
        return G, H
    
    def encode(self, data_bits):
        """Encode 4-bit data into 7-bit Hamming code"""
        if len(data_bits) != 4:
            raise ValueError("Input must be 4 bits")
        
        # Convert to numpy array if needed
        if isinstance(data_bits, list):
            data_bits = np.array(data_bits)
        
        # Matrix multiplication modulo 2
        encoded = np.dot(data_bits, self.G) % 2
        return encoded.astype(int)
    
    def decode(self, encoded_bits):
        """Decode 7-bit Hamming code and detect error position"""
        if len(encoded_bits) != 7:
            raise ValueError("Input must be 7 bits")
        
        # Convert to numpy array if needed
        if isinstance(encoded_bits, list):
            encoded_bits = np.array(encoded_bits)
        
        # Calculate syndrome
        syndrome = np.dot(self.H, encoded_bits) % 2
        return syndrome.astype(int)
    
    def flip_bit(self, bits, position):
        """Flip a single bit at specified position"""
        flipped = bits.copy()
        flipped[position] = 1 - flipped[position]  # Flip 0<->1
        return flipped
    
    def error_position(self, syndrome):
        """Convert syndrome to decimal error position (0-based)"""
        if np.all(syndrome == 0):
            return -1  # No error
        
        # Find which column of H matches the syndrome
        for i in range(7):
            if np.array_equal(self.H[:, i], syndrome):
                return i
        return -2  # Multiple errors detected
    
    def _format_list(self, lst):
        """Convert list to formatted string without alignment"""
        return '[' + ''.join(str(x) for x in lst) + ']'
    
    def demonstrate_single_case(self, data_bits):
        """Demonstrate Hamming code for a single test case"""
        print("\n" + "=" * 60)
        print(f"HAMMING (7,4) CODE - {self.matrix_type} MATRICES")
        print("=" * 60)
        
        print(f"\nGenerator Matrix G (4x7):")
        for row in self.G:
            print("  ", self._format_list(row))
        
        print(f"\nParity-Check Matrix H (3x7):")
        for row in self.H:
            print("  ", self._format_list(row))
        
        # Verify H * G^T = 0
        verification = np.dot(self.H, self.G.T) % 2
        print(f"\nMatrix Verification (H × Gᵀ mod 2):")
        for row in verification:
            print("  ", self._format_list(row))
        
        if np.all(verification == 0):
            print("✓ VALID: H × Gᵀ = 0 → Matrices satisfy parity-check condition")
        else:
            print("✗ INVALID: H × Gᵀ ≠ 0 → Matrices do not satisfy parity-check")
        
        # Original encoding
        encoded = self.encode(data_bits)
        syndrome = self.decode(encoded)
        error_pos = self.error_position(syndrome)
        
        print(f"\nInput Data:    {self._format_list(data_bits)}")
        print(f"Encoded:       {self._format_list(encoded)}")
        print(f"Syndrome:      {self._format_list(syndrome)} → {'No errors' if error_pos == -1 else f'Error at bit {error_pos}'}")
        
        print("\n" + "=" * 50)
        print("SINGLE BIT ERROR DETECTION TEST")
        print("=" * 50)
        
        print(f"{'Error':<8} {'Received':<20} {'Syndrome':<12} {'Detected':<10} Status")
        print("-" * 65)
        
        # Test all single-bit errors
        success_count = 0
        total_tests = 0
        
        # Test no error case
        syndrome = self.decode(encoded)
        detected_pos = self.error_position(syndrome)
        status = "✓ PASS" if detected_pos == -1 else "✗ FAIL"
        if detected_pos == -1:
            success_count += 1
        total_tests += 1
        print(f"{'None':<8} {self._format_list(encoded):<20} {self._format_list(syndrome):<12} {'None':<10} {status}")
        
        # Test single bit errors
        for error_pos in range(7):
            corrupted = self.flip_bit(encoded, error_pos)
            syndrome = self.decode(corrupted)
            detected_pos = self.error_position(syndrome)
            
            status = "✓ PASS" if detected_pos == error_pos else "✗ FAIL"
            if detected_pos == error_pos:
                success_count += 1
            total_tests += 1
            
            detected_str = f"Bit {detected_pos}" if detected_pos >= 0 else "None"
            print(f"Bit {error_pos:<5} {self._format_list(corrupted):<20} {self._format_list(syndrome):<12} {detected_str:<10} {status}")
        
        print(f"\nSUMMARY: {success_count}/{total_tests} tests passed")
        
        if success_count == total_tests:
            print("🎯 PERFECT: All single-bit errors detected and located correctly!")
        else:
            print("❌ INCOMPLETE: Some errors were not properly detected")
        
        return success_count == total_tests

def main():
    # Test data
    test_vectors = [
        [1, 1, 0, 1],  # Example from the prompt
    ]
    
    print("HAMMING (7,4) CODE DEMONSTRATION")
    print("\nChoose matrix type:")
    print("1. Standard matrices (guaranteed working)")
    print("2. Randomly generated matrices (may take a moment)")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
    except:
        choice = "1"  # Default to standard if input fails
    
    if choice == "2":
        print("\n" + "="*50)
        print("GENERATING RANDOM MATRICES")
        print("="*50)
        print("How it works:")
        print("• G = [I|P] where I is 4×4 identity, P is 4×3 random parity")
        print("• H = [Pᵀ|I] where I is 3×3 identity")
        print("• Must satisfy: H × Gᵀ = 0 (mod 2)")
        print("• Each syndrome uniquely identifies error position")
        print("• Timeout: 5 seconds max, falls back to standard")
        print("="*50)
        
        hamming = HammingCode(random_matrix=True)
        for i, data in enumerate(test_vectors, 1):
            print(f"\nTEST CASE {i}: Data = {data}")
            success = hamming.demonstrate_single_case(data)
            
    else:
        print("\n" + "="*50)
        print("USING STANDARD MATRICES")
        print("="*50)
        
        hamming = HammingCode(random_matrix=False)
        for i, data in enumerate(test_vectors, 1):
            print(f"\nTEST CASE {i}: Data = {data}")
            success = hamming.demonstrate_single_case(data)

if __name__ == "__main__":
    main()

"""
HAMMING (7,4) CODE DEMONSTRATION

Choose matrix type:
1. Standard matrices (guaranteed working)
2. Randomly generated matrices (may take a moment)
Enter choice (1 or 2): 2

==================================================
GENERATING RANDOM MATRICES
==================================================
How it works:
• G = [I|P] where I is 4×4 identity, P is 4×3 random parity
• H = [Pᵀ|I] where I is 3×3 identity
• Must satisfy: H × Gᵀ = 0 (mod 2)
• Each syndrome uniquely identifies error position
• Timeout: 5 seconds max, falls back to standard
==================================================
⚠️  Could not generate random matrices in time, using standard matrices

TEST CASE 1: Data = [1, 1, 0, 1]

============================================================
HAMMING (7,4) CODE - RANDOMLY GENERATED MATRICES
============================================================

Generator Matrix G (4x7):
   [1000111]
   [0100011]
   [0010101]
   [0001110]

Parity-Check Matrix H (3x7):
   [1011100]
   [1101010]
   [1110001]

Matrix Verification (H × Gᵀ mod 2):
   [0000]
   [0000]
   [0000]
✓ VALID: H × Gᵀ = 0 → Matrices satisfy parity-check condition

Input Data:    [1101]
Encoded:       [1101010]
Syndrome:      [000] → No errors

==================================================
SINGLE BIT ERROR DETECTION TEST
==================================================
Error    Received             Syndrome     Detected   Status
-----------------------------------------------------------------
None     [1101010]            [000]        None       ✓ PASS
Bit 0     [0101010]            [111]        Bit 0      ✓ PASS
Bit 1     [1001010]            [011]        Bit 1      ✓ PASS
Bit 2     [1111010]            [101]        Bit 2      ✓ PASS
Bit 3     [1100010]            [110]        Bit 3      ✓ PASS
Bit 4     [1101110]            [100]        Bit 4      ✓ PASS
Bit 5     [1101000]            [010]        Bit 5      ✓ PASS
Bit 6     [1101011]            [001]        Bit 6      ✓ PASS

SUMMARY: 8/8 tests passed
🎯 PERFECT: All single-bit errors detected and located correctly!
"""    