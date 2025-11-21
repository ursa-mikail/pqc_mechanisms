use classic_mceliece_rust::{keypair, encapsulate, decapsulate};
use classic_mceliece_rust::{CRYPTO_BYTES, CRYPTO_PUBLICKEYBYTES, CRYPTO_SECRETKEYBYTES};
use hex;

fn main() {
    // Initialize random number generator for cryptographic operations
    let mut rng = rand::thread_rng();
    
    println!("=== McEliece Cryptosystem - Key Encapsulation ===");
    println!("Key Sizes:");
    println!("- Shared Secret: {} bytes ({} bits)", CRYPTO_BYTES, CRYPTO_BYTES * 8);
    println!("- Public Key: {} bytes", CRYPTO_PUBLICKEYBYTES);
    println!("- Secret Key: {} bytes", CRYPTO_SECRETKEYBYTES);
    println!("- Ciphertext: 96 bytes\n");
    
    // Step 1: Bob generates his key pair
    println!("=== Step 1: Key Generation (Bob) ===");
    let mut public_key_buffer = [0u8; CRYPTO_PUBLICKEYBYTES];
    let mut secret_key_buffer = [0u8; CRYPTO_SECRETKEYBYTES];
    
    let (public_key, secret_key) = keypair(
        &mut public_key_buffer, 
        &mut secret_key_buffer, 
        &mut rng
    );
    
    println!("✓ Public Key generated: {} bytes", public_key.as_array().len());
    println!("✓ Secret Key generated: {} bytes", secret_key.as_array().len());
    println!("  Public Key (first 32 bytes): {}...", hex::encode(&public_key.as_array()[..32]));
    println!("  Secret Key (first 32 bytes): {}...", hex::encode(&secret_key.as_array()[..32]));
    
    // Step 2: Alice encrypts a message for Bob and creates shared secret
    println!("\n=== Step 2: Encryption (Alice) ===");
    let mut shared_secret_alice_buffer = [0u8; CRYPTO_BYTES];
    let (ciphertext, shared_secret_alice) = encapsulate(
        &public_key, 
        &mut shared_secret_alice_buffer, 
        &mut rng
    );
    
    println!("✓ Ciphertext created: {} bytes", ciphertext.as_array().len());
    println!("✓ Shared secret generated: {} bytes", shared_secret_alice.as_array().len());
    println!("  Ciphertext: {}", hex::encode(ciphertext.as_array()));
    println!("  Alice's Shared Secret: {}", hex::encode(shared_secret_alice.as_array()));
    
    // Step 3: Bob decrypts the ciphertext to get the same shared secret
    println!("\n=== Step 3: Decryption (Bob) ===");
    let mut shared_secret_bob_buffer = [0u8; CRYPTO_BYTES];
    let shared_secret_bob = decapsulate(
        &ciphertext, 
        &secret_key, 
        &mut shared_secret_bob_buffer
    );
    
    println!("✓ Ciphertext decrypted");
    println!("  Bob's Shared Secret: {}", hex::encode(shared_secret_bob.as_array()));
    
    // Step 4: Verification
    println!("\n=== Step 4: Verification ===");
    let secrets_match = shared_secret_alice.as_array() == shared_secret_bob.as_array();
    
    if secrets_match {
        println!("✅ SUCCESS: Shared secrets match!");
        println!("✅ Both parties now have the same 256-bit key for secure communication");
    } else {
        println!("❌ ERROR: Shared secrets don't match!");
    }
    
    // Summary
    println!("\n=== Summary ===");
    println!("Public Key Size:    {:>8} bytes", CRYPTO_PUBLICKEYBYTES);
    println!("Secret Key Size:    {:>8} bytes", CRYPTO_SECRETKEYBYTES); 
    println!("Ciphertext Size:    {:>8} bytes", 96);
    println!("Shared Secret Size: {:>8} bytes (256 bits)", CRYPTO_BYTES);
}

/*
Shared Secret   32 bytes (256 bits) Symmetric key for encrypted communication
Public Key  261,120 bytes   Used for encryption, can be safely shared
Secret Key  6,492 bytes Used for decryption, must be kept private
Ciphertext  96 bytes    Encrypted message containing the shared secret

=== McEliece Cryptosystem - Key Encapsulation ===
Key Sizes:
- Shared Secret: 32 bytes (256 bits)
- Public Key: 261120 bytes
- Secret Key: 6492 bytes
- Ciphertext: 96 bytes

=== Step 1: Key Generation (Bob) ===
✓ Public Key generated: 261120 bytes
✓ Secret Key generated: 6492 bytes
  Public Key (first 32 bytes): b3b16ee524af6848b8f15e4e8c0dc0c171035df0e9a1ed80081b07cd2d5c993f...
  Secret Key (first 32 bytes): 9714a6e9a6c2a6709ddadb2bc3a2ebe81232d728af487ae32fadfb8bf0d73105...

=== Step 2: Encryption (Alice) ===
✓ Ciphertext created: 96 bytes
✓ Shared secret generated: 32 bytes
  Ciphertext: f66ee432ab4532e3a0d31519cb813046c3e0cc83215641f6efa5088d2fdb1698f698d8cd7665c0883bf53bd8e6cafba1fff61bbd27692f4090d116e6d144573fd8579741320c42ccc89d9b9843152d52fd57baee983dc0c8d369d9f1db7b9328
  Alice's Shared Secret: e1e78fbd74813111c3de5812d3ce2b24c979c392e3ea564b5e19d059f4804792

=== Step 3: Decryption (Bob) ===
✓ Ciphertext decrypted
  Bob's Shared Secret: e1e78fbd74813111c3de5812d3ce2b24c979c392e3ea564b5e19d059f4804792

=== Step 4: Verification ===
✅ SUCCESS: Shared secrets match!
✅ Both parties now have the same 256-bit key for secure communication

=== Summary ===
Public Key Size:      261120 bytes
Secret Key Size:        6492 bytes
Ciphertext Size:          96 bytes
Shared Secret Size:       32 bytes (256 bits)

*/