# Hamming (7,4) Code Implementation

A comprehensive Python implementation of the Hamming (7,4) error-correcting code with both standard and randomly generated matrix options.

## Overview

The Hamming (7,4) code is a forward error correction (FEC) scheme that encodes 4 bits of data into 7 bits, adding 3 parity bits that allow for both error detection and single-bit error correction.

### Key Features

- **Standard Matrix Implementation**: Uses well-known Hamming (7,4) matrices
- **Random Matrix Generation**: Creates valid random generator and parity-check matrices
- **Error Simulation**: Tests all possible single-bit error scenarios
- **Matrix Verification**: Automatically validates that H × Gᵀ = 0 (mod 2)
- **Comprehensive Testing**: Verifies error detection for all bit positions

## Mathematical Foundation

### Generator Matrix (G)
The generator matrix is in systematic form:
G = [I|P]


Where:
- `I` is a 4×4 identity matrix
- `P` is a 4×3 parity matrix

### Parity-Check Matrix (H)
The parity-check matrix is constructed as:
H = [Pᵀ|I]

Where:
- `Pᵀ` is the transpose of the parity matrix
- `I` is a 3×3 identity matrix

### Verification
Valid matrices must satisfy:

H × Gᵀ = 0 (mod 2)


## Code Structure

### Core Components

1. **HammingCode Class**
   - `__init__()`: Initializes with standard or random matrices
   - `encode()`: Converts 4-bit data to 7-bit codeword
   - `decode()`: Calculates syndrome for error detection
   - `flip_bit()`: Introduces single-bit errors for testing
   - `error_position()`: Converts syndrome to bit position

2. **Matrix Generation**
   - Standard matrices (guaranteed working)
   - Random matrices with timeout protection
   - Automatic fallback to standard if generation fails

3. **Testing Framework**
   - Tests all single-bit error scenarios
   - Validates error detection accuracy
   - Provides clear pass/fail status

## Usage Examples

### Basic Usage
```python
# Standard matrices
hamming = HammingCode(random_matrix=False)
data = [1, 1, 0, 1]
encoded = hamming.encode(data)  # Returns 7-bit codeword
syndrome = hamming.decode(encoded)  # Returns 3-bit syndrome
```

Random Matrix Generation
``` python
# Random matrices with verification
hamming = HammingCode(random_matrix=True)
success = hamming.demonstrate_single_case([1, 0, 1, 0])
```

## Error Simulation
```python
# Test specific error scenarios
encoded = hamming.encode([1, 1, 0, 1])
corrupted = hamming.flip_bit(encoded, 3)  # Flip bit 3
syndrome = hamming.decode(corrupted)
error_pos = hamming.error_position(syndrome)  # Returns 3
```

## Output Example
```text
HAMMING (7,4) CODE - RANDOMLY GENERATED MATRICES
============================================================

Generator Matrix G (4x7):
   [1000111]
   [0100011]
   [0010101]
   [0001110]

Input Data:    [1101]
Encoded:       [1101001]
Syndrome:      [000] → No errors

SINGLE BIT ERROR DETECTION TEST
==================================================
Error    Received    Syndrome    Detected    Status
--------------------------------------------------
None     [1101001]   [000]       None        ✓ PASS
Bit 0    [0101001]   [110]       Bit 0       ✓ PASS
Bit 1    [1001001]   [101]       Bit 1       ✓ PASS
...
Bit 6    [1101000]   [001]       Bit 6       ✓ PASS

SUMMARY: 8/8 tests passed
🎯 PERFECT: All single-bit errors detected and located correctly!
```

### Error Correction Capability
```
Detects: All single-bit errors

Corrects: All single-bit errors

Detects: Some double-bit errors (but cannot correct)

Fails: For 3+ bit errors
```

The syndrome pattern uniquely identifies the error position:
```
Syndrome [000]: No error

Syndrome matching column i of H: Error at bit position i

Syndrome not matching any column: Multiple errors detected
```

### Extensions
The Hamming (7,4) code can be extended to:
```
Hamming (15,11) for longer messages

SECDED (Single Error Correction, Double Error Detection)

Product codes for two-dimensional protectio
```
