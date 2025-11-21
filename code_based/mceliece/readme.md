
This demonstrates a Key Encapsulation Mechanism (KEM) where two parties can establish a shared secret over an insecure channel.

## Concepts Explained
Step 1: Bob generates cryptographic keys (public key for encryption, private key for decryption)
Key Generation: Bob creates a public/private key pair

Step 2: Alice encrypts data using Bob's public key, creating a ciphertext and shared secret
Encapsulation: Alice uses Bob's public key to encrypt and create a shared secret

Step 3: Bob decrypts the ciphertext using his private key to recover the shared secret
Decapsulation: Bob uses his private key to decrypt and recover the shared secret

Step 4: Both parties verify they have the same shared secret for secure communication
Shared Secret: Both parties now have the same secret key for secure communication

```
# Show all available commands
make help

# Build and run in debug mode (most common during development)
make run

# Build optimized release version
make release

# Run the release version
make run-release

# Clean build artifacts
make clean

# Run tests
make test

# Format code
make fmt

# Check code quality
make lint

# Build for production (optimized and stripped)
make production

# Show binary sizes
make size

# Get project information
make info

# Common development workflow
make clean && make test && make run
```
```
Clean Target: Removes all build artifacts completely
Multiple Build Types: Debug, Release, and Production (stripped)
Development Tools: Formatting, linting, testing
Information Targets: Size analysis, project info
Safety: Security audit, dependency checking
Help System: Comprehensive help with examples
```