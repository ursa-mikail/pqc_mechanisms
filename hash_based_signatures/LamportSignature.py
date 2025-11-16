import hashlib
from binascii import unhexlify, hexlify
from os import urandom
import sys

class LamportSignature:
    """
    A clean implementation of the Lamport one-time signature scheme.
    Signs SHA-256 hashes using 256 pairs of random numbers.
    """
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self):
        """Generate Lamport key pair: 256 pairs for 0-bits, 256 pairs for 1-bits"""
        private_key = []
        public_key = []
        
        # Create 256 pairs of random numbers (for each bit position)
        for _ in range(256):
            # Generate two random numbers: one for '0', one for '1'
            zero_key = self._random_bytes(32)  # 256-bit random
            one_key = self._random_bytes(32)   # 256-bit random
            
            private_key.append((zero_key, one_key))
            # Public key is the hash of each private value
            public_key.append((self._sha256(zero_key), self._sha256(one_key)))
        
        self.private_key = private_key
        self.public_key = public_key
        return private_key, public_key
    
    def sign(self, message):
        """Sign a message using the private key"""
        if not self.private_key:
            raise ValueError("Private key not generated. Call generate_keys() first.")
        
        # Get the SHA-256 hash of the message
        message_hash = self._sha256_binary(message)
        signature = []
        
        # For each bit in the hash, select the corresponding private key
        for bit_position in range(256):
            bit_value = message_hash[bit_position]
            
            if bit_value == '0':
                # Use the '0' private key for this position
                signature.append(self.private_key[bit_position][0])
            else:  # bit_value == '1'
                # Use the '1' private key for this position
                signature.append(self.private_key[bit_position][1])
        
        return signature
    
    def verify(self, message, signature, public_key):
        """Verify a signature against a message and public key"""
        # Get the SHA-256 hash of the message
        message_hash = self._sha256_binary(message)
        
        # Verify each position in the signature
        for bit_position in range(256):
            bit_value = message_hash[bit_position]
            signature_element = signature[bit_position]
            
            # Hash the signature element
            hashed_signature = self._sha256(signature_element)
            
            # Check if it matches the corresponding public key
            if bit_value == '0':
                expected_hash = public_key[bit_position][0]
            else:  # bit_value == '1'
                expected_hash = public_key[bit_position][1]
            
            if hashed_signature != expected_hash:
                return False  # Signature verification failed
        
        return True  # All checks passed
    
    def _sha256(self, data):
        """Return hex-encoded SHA-256 hash"""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()
    
    def _sha256_binary(self, data):
        """Return SHA-256 hash as a binary string (256 bits)"""
        if isinstance(data, str):
            data = data.encode()
        hash_bytes = hashlib.sha256(data).digest()
        
        # Convert to binary string (256 bits)
        binary_string = ''
        for byte in hash_bytes:
            binary_string += format(byte, '08b')  # 8 bits per byte
        
        return binary_string
    
    def _random_bytes(self, num_bytes):
        """Generate random bytes and return as hex string"""
        return hexlify(urandom(num_bytes)).decode()

def main():
    # Get message from command line or use default
    message = "Hello" if len(sys.argv) <= 1 else sys.argv[1]
    
    # Create Lamport signature instance
    lamport = LamportSignature()
    
    # Generate key pair
    print("=== Generating Lamport Key Pair ===")
    private_key, public_key = lamport.generate_keys()
    
    # Display sample keys
    print("\n=== Private Key (Keep Secret) ===")
    for i in range(3):  # Show first 3 pairs
        print(f"Position {i}:")
        print(f"  For '0' bit: {private_key[i][0][:16]}...")
        print(f"  For '1' bit: {private_key[i][1][:16]}...")
    
    print("\n=== Public Key (Share Freely) ===")
    for i in range(3):  # Show first 3 pairs
        print(f"Position {i}:")
        print(f"  Hash of '0' key: {public_key[i][0]}")
        print(f"  Hash of '1' key: {public_key[i][1]}")
    
    # Sign the message
    print(f"\n=== Signing Message ===")
    print(f"Message: {message}")
    print(f"SHA-256: {lamport._sha256(message)}")
    
    signature = lamport.sign(message)
    
    print(f"\n=== Signature ===")
    for i in range(3):  # Show first 3 signature elements
        print(f"Position {i}: {signature[i][:16]}...")
    
    # Verify the signature
    print(f"\n=== Verification ===")
    is_valid = lamport.verify(message, signature, public_key)
    print(f"Signature valid: {is_valid}")
    
    # Test with wrong message (should fail)
    print(f"\n=== Testing with Wrong Message ===")
    wrong_message = "Wrong message"
    is_valid_wrong = lamport.verify(wrong_message, signature, public_key)
    print(f"Wrong message verification: {is_valid_wrong} (should be False)")

if __name__ == "__main__":
    main()

"""
=== Generating Lamport Key Pair ===

=== Private Key (Keep Secret) ===
Position 0:
  For '0' bit: c66302a8a90bfed8...
  For '1' bit: 2cca5ab5bc1fb7de...
Position 1:
  For '0' bit: 9d45eb91566cedd1...
  For '1' bit: 60b3cfca63262334...
Position 2:
  For '0' bit: 64b673c000595a5c...
  For '1' bit: 79f7493da1b6bf96...

=== Public Key (Share Freely) ===
Position 0:
  Hash of '0' key: e24be334ba192464cadeea4b1b8136297319cd28d247180cda4be46a8fcc1cb5
  Hash of '1' key: cfbf43dd17a75af733069fadffb427755ea1bf693fe17f45ee2667bee0839aa8
Position 1:
  Hash of '0' key: 310d35e49fc600ca4e53f90553b312fc63ac7c9a47afab4292447eb5e0ff3d1a
  Hash of '1' key: f928c19d0319e170482f23e47ccf2e6e04663b0d49c76fa5816df8502170d84b
Position 2:
  Hash of '0' key: d12c8ab4c14b785f5ec203a43c80b50dad245c8832d6cb51fde5a15ed8dba51c
  Hash of '1' key: 7829dcd79eb5ac83475540f190e2bc54eb45d65c899292ddff6a5488443e4f30

=== Signing Message ===
Message: -f
SHA-256: 0e6503c1ece40e4ea7668463248ea2716eb37643f2c2c605f8bcee4d195a1705

=== Signature ===
Position 0: c66302a8a90bfed8...
Position 1: 9d45eb91566cedd1...
Position 2: 64b673c000595a5c...

=== Verification ===
Signature valid: True

=== Testing with Wrong Message ===
Wrong message verification: False (should be False)
"""    