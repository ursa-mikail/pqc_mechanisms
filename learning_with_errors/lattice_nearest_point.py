import numpy as np
import math
import matplotlib.pyplot as plt
from itertools import product

def find_closest_lattice_point_bruteforce(x1, y1, x2, y2, target_x, target_y, search_range=20):
    """Find the actual closest lattice point by exhaustive search"""
    min_distance = float('inf')
    best_point = (0, 0)
    best_coeffs = (0, 0)
    
    for a in range(-search_range, search_range + 1):
        for b in range(-search_range, search_range + 1):
            lattice_x = a * x1 + b * x2
            lattice_y = a * y1 + b * y2
            distance = math.sqrt((target_x - lattice_x)**2 + (target_y - lattice_y)**2)
            
            if distance < min_distance:
                min_distance = distance
                best_point = (lattice_x, lattice_y)
                best_coeffs = (a, b)
    
    return best_point[0], best_point[1], best_coeffs[0], best_coeffs[1], min_distance

def babai_approximation(x1, y1, x2, y2, target_x, target_y):
    """Babai's rounding algorithm (fast but approximate)"""
    basis_matrix = np.array([[x1, x2], [y1, y2]])
    target_vector = np.array([target_x, target_y])
    
    try:
        coeffs = np.linalg.solve(basis_matrix, target_vector)
        a_round, b_round = round(coeffs[0]), round(coeffs[1])
        nearest_x = x1 * a_round + x2 * b_round
        nearest_y = y1 * a_round + b_round * y2
        distance = math.sqrt((target_x - nearest_x)**2 + (target_y - nearest_y)**2)
        return nearest_x, nearest_y, a_round, b_round, distance
    except np.linalg.LinAlgError:
        return 0, 0, 0, 0, float('inf')

def plot_lattice_comparison(x1, y1, x2, y2, target_x, target_y, title_suffix=""):
    """Plot lattice with both Babai and true CVP solutions"""
    
    # Generate lattice points
    lattice_points = []
    for a in range(-8, 9):
        for b in range(-8, 9):
            lattice_x = a * x1 + b * x2
            lattice_y = a * y1 + b * y2
            lattice_points.append((lattice_x, lattice_y))
    
    # Get Babai's approximation
    babai_x, babai_y, babai_a, babai_b, babai_dist = babai_approximation(x1, y1, x2, y2, target_x, target_y)
    
    # Get true closest point
    true_x, true_y, true_a, true_b, true_dist = find_closest_lattice_point_bruteforce(
        x1, y1, x2, y2, target_x, target_y, search_range=20)
    
    # Calculate basis quality
    dot_product = x1 * x2 + y1 * y2
    mag1 = math.sqrt(x1*x1 + y1*y1)
    mag2 = math.sqrt(x2*x2 + y2*y2)
    costheta = dot_product / (mag1 * mag2) if mag1 * mag2 != 0 else 0
    angle_deg = math.degrees(math.acos(max(min(costheta, 1), -1)))
    
    # Create plot
    plt.figure(figsize=(12, 10))
    
    # Plot lattice points
    lattice_x_coords, lattice_y_coords = zip(*lattice_points)
    plt.scatter(lattice_x_coords, lattice_y_coords, color='lightblue', alpha=0.4, s=30, label='Lattice Points')
    
    # Plot basis vectors
    plt.arrow(0, 0, x1, y1, head_width=0.8, head_length=0.8, fc='red', ec='red', 
              linewidth=2.5, label=f'v₁=({x1},{y1})', zorder=3)
    plt.arrow(0, 0, x2, y2, head_width=0.8, head_length=0.8, fc='green', ec='green', 
              linewidth=2.5, label=f'v₂=({x2},{y2})', zorder=3)
    
    # Plot target point
    plt.scatter(target_x, target_y, color='purple', s=300, marker='*', 
               label=f'Target ({target_x},{target_y})', zorder=5, edgecolors='black', linewidths=2)
    
    # Plot TRUE closest point
    plt.scatter(true_x, true_y, color='lime', s=200, marker='o', 
               label=f'TRUE Closest ({true_x},{true_y}) - d={true_dist:.2f}', 
               zorder=5, edgecolors='darkgreen', linewidths=2)
    plt.plot([target_x, true_x], [target_y, true_y], 'g-', linewidth=2, alpha=0.7)
    
    # Plot Babai's approximation (if different from true)
    if (babai_x, babai_y) != (true_x, true_y):
        plt.scatter(babai_x, babai_y, color='orange', s=200, marker='s', 
                   label=f'Babai Approx ({babai_x},{babai_y}) - d={babai_dist:.2f}', 
                   zorder=4, edgecolors='darkorange', linewidths=2)
        plt.plot([target_x, babai_x], [target_y, babai_y], 'orange', linestyle='--', 
                linewidth=2, alpha=0.7)
    
    # Formatting
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)
    plt.axis('equal')
    
    # Calculate bounds
    all_x = list(lattice_x_coords) + [target_x, true_x, babai_x]
    all_y = list(lattice_y_coords) + [target_y, true_y, babai_y]
    margin = 5
    plt.xlim(min(all_x) - margin, max(all_x) + margin)
    plt.ylim(min(all_y) - margin, max(all_y) + margin)
    
    # Quality assessment
    quality = "GOOD (≈orthogonal)" if abs(costheta) < 0.3 else "POOR (skewed)"
    babai_accurate = "✓" if (babai_x, babai_y) == (true_x, true_y) else "✗"
    
    plt.title(f'{title_suffix}\n'
             f'Angle: {angle_deg:.1f}° | cos(θ)={costheta:.3f} | Quality: {quality}\n'
             f'Babai Accurate: {babai_accurate}', 
             fontsize=13, pad=15)
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    
    plt.tight_layout()
    
    return true_x, true_y, true_a, true_b, babai_x, babai_y, costheta

def generate_unimodular_basis(x1, y1, x2, y2, a, b, c, d):
    """Transform basis using unimodular matrix with det=±1"""
    new_x1 = a * x1 + b * x2
    new_y1 = a * y1 + b * y2
    new_x2 = c * x1 + d * x2  
    new_y2 = c * y1 + d * y2
    return new_x1, new_y1, new_x2, new_y2

# ============ MAIN DEMONSTRATION ============
print("=" * 60)
print("LATTICE-BASED CRYPTOGRAPHY: CVP Problem Demonstration")
print("=" * 60)

# Test parameters
x1, y1 = 5, 1
x2, y2 = -2, 8
target_x, target_y = 27, 8

print(f"\nOriginal Basis: v₁=({x1},{y1}), v₂=({x2},{y2})")
print(f"Target Point: ({target_x},{target_y})")
print("\n" + "=" * 60)

# Plot 1: Good basis (nearly orthogonal)
print("\n[1] GOOD BASIS (Nearly Orthogonal)")
true1_x, true1_y, true1_a, true1_b, babai1_x, babai1_y, cos1 = plot_lattice_comparison(
    x1, y1, x2, y2, target_x, target_y, "Good Basis: Nearly Orthogonal")
print(f"    cos(θ) = {cos1:.4f} → Nearly perpendicular ✓")
print(f"    TRUE closest: ({true1_x},{true1_y}) = {true1_a}v₁ + {true1_b}v₂")
print(f"    Babai result: ({babai1_x},{babai1_y})")
print(f"    Match: {(true1_x, true1_y) == (babai1_x, babai1_y)}")

# Plot 2: Same lattice, different basis (unimodular transform)
print("\n[2] SAME LATTICE, DIFFERENT BASIS (Unimodular Transform)")
new_x1, new_y1, new_x2, new_y2 = generate_unimodular_basis(x1, y1, x2, y2, 1, 1, 0, 1)
print(f"    Transform: [[1,1],[0,1]] → v₁'=({new_x1},{new_y1}), v₂'=({new_x2},{new_y2})")
true2_x, true2_y, true2_a, true2_b, babai2_x, babai2_y, cos2 = plot_lattice_comparison(
    new_x1, new_y1, new_x2, new_y2, target_x, target_y, "Same Lattice: Transformed Basis")
print(f"    cos(θ) = {cos2:.4f} → More skewed")
print(f"    TRUE closest: ({true2_x},{true2_y}) = {true2_a}v₁' + {true2_b}v₂'")
print(f"    Babai result: ({babai2_x},{babai2_y})")
print(f"    Match: {(true2_x, true2_y) == (babai2_x, babai2_y)}")

# Plot 3: Bad basis (nearly parallel - different lattice)
print("\n[3] BAD BASIS (Nearly Parallel - DIFFERENT LATTICE)")
bad_x1, bad_y1 = 37, 41
bad_x2, bad_y2 = 39, 43
true3_x, true3_y, true3_a, true3_b, babai3_x, babai3_y, cos3 = plot_lattice_comparison(
    bad_x1, bad_y1, bad_x2, bad_y2, target_x, target_y, "Bad Basis: Nearly Parallel (Different Lattice)")
print(f"    Basis: v₁=({bad_x1},{bad_y1}), v₂=({bad_x2},{bad_y2})")
print(f"    cos(θ) = {cos3:.4f} → Nearly parallel (BAD!)")
print(f"    TRUE closest: ({true3_x},{true3_y})")
print(f"    Babai result: ({babai3_x},{babai3_y})")
print(f"    Match: {(true3_x, true3_y) == (babai3_x, babai3_y)}")

# Verification
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)
print(f"Bases 1 & 2 span SAME lattice: {(true1_x, true1_y) == (true2_x, true2_y)}")
print(f"  → Basis 1 closest: ({true1_x},{true1_y})")
print(f"  → Basis 2 closest: ({true2_x},{true2_y})")
print(f"\nBasis 3 spans DIFFERENT lattice: {(true1_x, true1_y) != (true3_x, true3_y)}")
print(f"  → Basis 3 closest: ({true3_x},{true3_y})")

print("\n" + "=" * 60)
print("CRYPTOGRAPHIC IMPLICATIONS")
print("=" * 60)
print("\n🔓 GOOD BASIS (Public Key - Orthogonal):")
print("   • Easy CVP: Babai's algorithm works perfectly")
print("   • Used for ENCRYPTION/DECRYPTION")
print("   • cos(θ) ≈ 0 means vectors are perpendicular")

print("\n🔒 BAD BASIS (Secret Key - Skewed):")
print("   • Hard CVP: Babai fails, need exhaustive search")
print("   • Provides SECURITY against attacks")
print("   • cos(θ) ≈ 1 means vectors are nearly parallel")

print("\n📊 Summary:")
print(f"   Basis 1: |cos(θ)|={abs(cos1):.4f} → {'GOOD' if abs(cos1)<0.3 else 'POOR'}")
print(f"   Basis 2: |cos(θ)|={abs(cos2):.4f} → {'GOOD' if abs(cos2)<0.3 else 'POOR'}")
print(f"   Basis 3: |cos(θ)|={abs(cos3):.4f} → {'GOOD' if abs(cos3)<0.3 else 'POOR'}")

plt.show()

"""
 WARNING:matplotlib.axes._base:Ignoring fixed x limits to fulfill fixed data aspect with adjustable data limits.
============================================================
LATTICE-BASED CRYPTOGRAPHY: CVP Problem Demonstration
============================================================

Original Basis: v₁=(5,1), v₂=(-2,8)
Target Point: (27,8)

============================================================

[1] GOOD BASIS (Nearly Orthogonal)
    cos(θ) = -0.0476 → Nearly perpendicular ✓
    TRUE closest: (25,5) = 5v₁ + 0v₂
    Babai result: (30,6)
    Match: False

[2] SAME LATTICE, DIFFERENT BASIS (Unimodular Transform)
    Transform: [[1,1],[0,1]] → v₁'=(3,9), v₂'=(-2,8)
WARNING:matplotlib.axes._base:Ignoring fixed x limits to fulfill fixed data aspect with adjustable data limits.
WARNING:matplotlib.axes._base:Ignoring fixed x limits to fulfill fixed data aspect with adjustable data limits.
WARNING:matplotlib.axes._base:Ignoring fixed x limits to fulfill fixed data aspect with adjustable data limits.
    cos(θ) = 0.8437 → More skewed
    TRUE closest: (25,5) = 5v₁' + -5v₂'
    Babai result: (28,14)
    Match: False

[3] BAD BASIS (Nearly Parallel - DIFFERENT LATTICE)
    Basis: v₁=(37,41), v₂=(39,43)
    cos(θ) = 1.0000 → Nearly parallel (BAD!)
    TRUE closest: (18,18)
    Babai result: (17,-3)
    Match: False

============================================================
VERIFICATION
============================================================
Bases 1 & 2 span SAME lattice: True
  → Basis 1 closest: (25,5)
  → Basis 2 closest: (25,5)

Basis 3 spans DIFFERENT lattice: True
  → Basis 3 closest: (18,18)

============================================================
CRYPTOGRAPHIC IMPLICATIONS
============================================================

🔓 GOOD BASIS (Public Key - Orthogonal):
   • Easy CVP: Babai's algorithm works perfectly
   • Used for ENCRYPTION/DECRYPTION
   • cos(θ) ≈ 0 means vectors are perpendicular

🔒 BAD BASIS (Secret Key - Skewed):
   • Hard CVP: Babai fails, need exhaustive search
   • Provides SECURITY against attacks
   • cos(θ) ≈ 1 means vectors are nearly parallel

📊 Summary:
   Basis 1: |cos(θ)|=0.0476 → GOOD
   Basis 2: |cos(θ)|=0.8437 → POOR
   Basis 3: |cos(θ)|=1.0000 → POOR
WARNING:matplotlib.axes._base:Ignoring fixed y limits to fulfill fixed data aspect with adjustable data limits.
WARNING:matplotlib.axes._base:Ignoring fixed y limits to fulfill fixed data aspect with adjustable data limits.

"""

import numpy as np
import math
import matplotlib.pyplot as plt

def find_closest_lattice_point_bruteforce(x1, y1, x2, y2, target_x, target_y, search_range=20):
    """Find the actual closest lattice point by exhaustive search"""
    min_distance = float('inf')
    best_point = (0, 0)
    best_coeffs = (0, 0)
    
    for a in range(-search_range, search_range + 1):
        for b in range(-search_range, search_range + 1):
            lattice_x = a * x1 + b * x2
            lattice_y = a * y1 + b * y2
            distance = math.sqrt((target_x - lattice_x)**2 + (target_y - lattice_y)**2)
            
            if distance < min_distance:
                min_distance = distance
                best_point = (lattice_x, lattice_y)
                best_coeffs = (a, b)
    
    return best_point[0], best_point[1], best_coeffs[0], best_coeffs[1], min_distance

def babai_rounding(x1, y1, x2, y2, target_x, target_y):
    """Babai's ROUNDING algorithm (simplest, fast but less accurate)"""
    basis_matrix = np.array([[x1, x2], [y1, y2]])
    target_vector = np.array([target_x, target_y])
    
    try:
        # Solve: target = a*v1 + b*v2
        coeffs = np.linalg.solve(basis_matrix, target_vector)
        # Simple rounding
        a_round, b_round = round(coeffs[0]), round(coeffs[1])
        nearest_x = x1 * a_round + x2 * b_round
        nearest_y = y1 * a_round + b_round * y2
        distance = math.sqrt((target_x - nearest_x)**2 + (target_y - nearest_y)**2)
        return nearest_x, nearest_y, a_round, b_round, distance
    except np.linalg.LinAlgError:
        return 0, 0, 0, 0, float('inf')

def babai_nearest_plane(x1, y1, x2, y2, target_x, target_y):
    """Babai's NEAREST PLANE algorithm (better approximation)"""
    try:
        # Work with vectors
        v1 = np.array([x1, y1])
        v2 = np.array([x2, y2])
        t = np.array([target_x, target_y])
        
        # Process basis vectors in order
        # For v1: project and round
        dot_t_v1 = np.dot(t, v1)
        dot_v1_v1 = np.dot(v1, v1)
        c1 = dot_t_v1 / dot_v1_v1 if dot_v1_v1 != 0 else 0
        a1 = round(c1)
        
        # Update target by removing v1 component
        t_remaining = t - a1 * v1
        
        # For v2: project and round
        dot_t2_v2 = np.dot(t_remaining, v2)
        dot_v2_v2 = np.dot(v2, v2)
        c2 = dot_t2_v2 / dot_v2_v2 if dot_v2_v2 != 0 else 0
        a2 = round(c2)
        
        # Final lattice point
        result = a1 * v1 + a2 * v2
        distance = np.linalg.norm(t - result)
        
        return result[0], result[1], a1, a2, distance
    except:
        return 0, 0, 0, 0, float('inf')

def plot_lattice_comparison(x1, y1, x2, y2, target_x, target_y, title_suffix=""):
    """Plot lattice with Rounding, Nearest Plane, and true CVP solutions"""
    
    # Generate lattice points
    lattice_points = []
    for a in range(-8, 9):
        for b in range(-8, 9):
            lattice_x = a * x1 + b * x2
            lattice_y = a * y1 + b * y2
            lattice_points.append((lattice_x, lattice_y))
    
    # Get all three approximations
    round_x, round_y, round_a, round_b, round_dist = babai_rounding(
        x1, y1, x2, y2, target_x, target_y)
    
    plane_x, plane_y, plane_a, plane_b, plane_dist = babai_nearest_plane(
        x1, y1, x2, y2, target_x, target_y)
    
    true_x, true_y, true_a, true_b, true_dist = find_closest_lattice_point_bruteforce(
        x1, y1, x2, y2, target_x, target_y, search_range=20)
    
    # Calculate basis quality
    dot_product = x1 * x2 + y1 * y2
    mag1 = math.sqrt(x1*x1 + y1*y1)
    mag2 = math.sqrt(x2*x2 + y2*y2)
    costheta = dot_product / (mag1 * mag2) if mag1 * mag2 != 0 else 0
    angle_deg = math.degrees(math.acos(max(min(costheta, 1), -1)))
    
    # Create plot
    plt.figure(figsize=(13, 10))
    
    # Plot lattice points
    lattice_x_coords, lattice_y_coords = zip(*lattice_points)
    plt.scatter(lattice_x_coords, lattice_y_coords, color='lightblue', alpha=0.4, s=30, label='Lattice Points')
    
    # Plot basis vectors
    plt.arrow(0, 0, x1, y1, head_width=0.8, head_length=0.8, fc='red', ec='red', 
              linewidth=2.5, label=f'v₁=({x1},{y1})', zorder=3)
    plt.arrow(0, 0, x2, y2, head_width=0.8, head_length=0.8, fc='green', ec='green', 
              linewidth=2.5, label=f'v₂=({x2},{y2})', zorder=3)
    
    # Plot target point
    plt.scatter(target_x, target_y, color='purple', s=300, marker='*', 
               label=f'Target ({target_x},{target_y})', zorder=6, edgecolors='black', linewidths=2)
    
    # Plot TRUE closest point (always shown)
    plt.scatter(true_x, true_y, color='lime', s=250, marker='o', 
               label=f'TRUE CVP ({true_x},{true_y}) d={true_dist:.2f}', 
               zorder=5, edgecolors='darkgreen', linewidths=3)
    plt.plot([target_x, true_x], [target_y, true_y], 'lime', linewidth=3, alpha=0.8)
    
    # Plot Nearest Plane result (if different from true)
    if (plane_x, plane_y) != (true_x, true_y):
        plt.scatter(plane_x, plane_y, color='blue', s=200, marker='D', 
                   label=f'Nearest Plane ({plane_x},{plane_y}) d={plane_dist:.2f}', 
                   zorder=4, edgecolors='darkblue', linewidths=2)
        plt.plot([target_x, plane_x], [target_y, plane_y], 'blue', linestyle='--', 
                linewidth=2, alpha=0.7)
    
    # Plot Rounding result (if different from both)
    if (round_x, round_y) != (true_x, true_y) and (round_x, round_y) != (plane_x, plane_y):
        plt.scatter(round_x, round_y, color='orange', s=180, marker='s', 
                   label=f'Rounding ({round_x},{round_y}) d={round_dist:.2f}', 
                   zorder=3, edgecolors='darkorange', linewidths=2)
        plt.plot([target_x, round_x], [target_y, round_y], 'orange', linestyle=':', 
                linewidth=2, alpha=0.7)
    
    # Formatting
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)
    plt.axis('equal')
    
    # Calculate bounds
    all_x = list(lattice_x_coords) + [target_x, true_x, plane_x, round_x]
    all_y = list(lattice_y_coords) + [target_y, true_y, plane_y, round_y]
    margin = 5
    plt.xlim(min(all_x) - margin, max(all_x) + margin)
    plt.ylim(min(all_y) - margin, max(all_y) + margin)
    
    # Quality assessment
    quality = "GOOD (≈orthogonal)" if abs(costheta) < 0.3 else "POOR (skewed)"
    round_correct = "✓" if (round_x, round_y) == (true_x, true_y) else "✗"
    plane_correct = "✓" if (plane_x, plane_y) == (true_x, true_y) else "✗"
    
    plt.title(f'{title_suffix}\n'
             f'Angle: {angle_deg:.1f}° | cos(θ)={costheta:.3f} | Quality: {quality}\n'
             f'Rounding: {round_correct} | Nearest Plane: {plane_correct}', 
             fontsize=12, pad=15)
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    
    plt.tight_layout()
    
    return {
        'true': (true_x, true_y, true_a, true_b, true_dist),
        'plane': (plane_x, plane_y, plane_a, plane_b, plane_dist),
        'round': (round_x, round_y, round_a, round_b, round_dist),
        'costheta': costheta
    }

def generate_unimodular_basis(x1, y1, x2, y2, a, b, c, d):
    """Transform basis using unimodular matrix with det=±1"""
    new_x1 = a * x1 + b * x2
    new_y1 = a * y1 + b * y2
    new_x2 = c * x1 + d * x2  
    new_y2 = c * y1 + d * y2
    return new_x1, new_y1, new_x2, new_y2

# ============ MAIN DEMONSTRATION ============
print("=" * 70)
print("LATTICE CVP: Comparing Babai's Rounding vs Nearest Plane")
print("=" * 70)

# Test parameters
x1, y1 = 5, 1
x2, y2 = -2, 8
target_x, target_y = 27, 8

print(f"\nOriginal Basis: v₁=({x1},{y1}), v₂=({x2},{y2})")
print(f"Target Point: ({target_x},{target_y})")
print("\n" + "=" * 70)

# Plot 1: Good basis (nearly orthogonal)
print("\n[1] GOOD BASIS (Nearly Orthogonal)")
result1 = plot_lattice_comparison(x1, y1, x2, y2, target_x, target_y, 
                                   "Good Basis: Nearly Orthogonal")
print(f"    cos(θ) = {result1['costheta']:.4f} → Nearly perpendicular ✓")
print(f"    TRUE CVP:       ({result1['true'][0]},{result1['true'][1]}) - distance: {result1['true'][4]:.3f}")
print(f"    Nearest Plane:  ({result1['plane'][0]},{result1['plane'][1]}) - distance: {result1['plane'][4]:.3f}")
print(f"    Rounding:       ({result1['round'][0]},{result1['round'][1]}) - distance: {result1['round'][4]:.3f}")

# Plot 2: Same lattice, different basis (unimodular transform)
print("\n[2] SAME LATTICE, SKEWED BASIS (Unimodular Transform)")
new_x1, new_y1, new_x2, new_y2 = generate_unimodular_basis(x1, y1, x2, y2, 1, 1, 0, 1)
print(f"    Transform: [[1,1],[0,1]] → v₁'=({new_x1},{new_y1}), v₂'=({new_x2},{new_y2})")
result2 = plot_lattice_comparison(new_x1, new_y1, new_x2, new_y2, target_x, target_y, 
                                   "Same Lattice: Transformed Basis (Skewed)")
print(f"    cos(θ) = {result2['costheta']:.4f} → Highly skewed")
print(f"    TRUE CVP:       ({result2['true'][0]},{result2['true'][1]}) - distance: {result2['true'][4]:.3f}")
print(f"    Nearest Plane:  ({result2['plane'][0]},{result2['plane'][1]}) - distance: {result2['plane'][4]:.3f}")
print(f"    Rounding:       ({result2['round'][0]},{result2['round'][1]}) - distance: {result2['round'][4]:.3f}")

# Plot 3: Bad basis (nearly parallel - different lattice)
print("\n[3] BAD BASIS (Nearly Parallel - DIFFERENT LATTICE)")
bad_x1, bad_y1 = 37, 41
bad_x2, bad_y2 = 39, 43
result3 = plot_lattice_comparison(bad_x1, bad_y1, bad_x2, bad_y2, target_x, target_y, 
                                   "Bad Basis: Nearly Parallel (Different Lattice)")
print(f"    Basis: v₁=({bad_x1},{bad_y1}), v₂=({bad_x2},{bad_y2})")
print(f"    cos(θ) = {result3['costheta']:.4f} → Nearly parallel (WORST!)")
print(f"    TRUE CVP:       ({result3['true'][0]},{result3['true'][1]}) - distance: {result3['true'][4]:.3f}")
print(f"    Nearest Plane:  ({result3['plane'][0]},{result3['plane'][1]}) - distance: {result3['plane'][4]:.3f}")
print(f"    Rounding:       ({result3['round'][0]},{result3['round'][1]}) - distance: {result3['round'][4]:.3f}")

# Verification
print("\n" + "=" * 70)
print("VERIFICATION: Same Lattice → Same CVP")
print("=" * 70)
true1 = (result1['true'][0], result1['true'][1])
true2 = (result2['true'][0], result2['true'][1])
true3 = (result3['true'][0], result3['true'][1])

print(f"Bases 1 & 2 (same lattice): {true1 == true2}")
print(f"  → Basis 1 TRUE CVP: {true1}")
print(f"  → Basis 2 TRUE CVP: {true2}")
print(f"\nBasis 3 (different lattice): {true1 != true3}")
print(f"  → Basis 3 TRUE CVP: {true3}")

# Algorithm comparison
print("\n" + "=" * 70)
print("ALGORITHM COMPARISON")
print("=" * 70)
print("\n📊 Performance Summary:")
print(f"\n  Basis 1 (Good, cos={result1['costheta']:.3f}):")
print(f"    Rounding correct:      {true1 == (result1['round'][0], result1['round'][1])}")
print(f"    Nearest Plane correct: {true1 == (result1['plane'][0], result1['plane'][1])}")

print(f"\n  Basis 2 (Skewed, cos={result2['costheta']:.3f}):")
print(f"    Rounding correct:      {true2 == (result2['round'][0], result2['round'][1])}")
print(f"    Nearest Plane correct: {true2 == (result2['plane'][0], result2['plane'][1])}")

print(f"\n  Basis 3 (Parallel, cos={result3['costheta']:.3f}):")
print(f"    Rounding correct:      {true3 == (result3['round'][0], result3['round'][1])}")
print(f"    Nearest Plane correct: {true3 == (result3['plane'][0], result3['plane'][1])}")

print("\n" + "=" * 70)
print("KEY INSIGHTS")
print("=" * 70)
print("\n🔹 Babai's ROUNDING:")
print("   • Simplest & fastest")
print("   • Only optimal for orthogonal bases")
print("   • Fails on skewed bases")

print("\n🔹 Babai's NEAREST PLANE:")
print("   • Better approximation than rounding")
print("   • Still may fail on highly skewed bases")
print("   • Polynomial time: O(n²)")

print("\n🔹 TRUE CVP (Exhaustive Search):")
print("   • Always finds correct answer")
print("   • Exponential time in general")
print("   • Lattice-dependent, not basis-dependent")

plt.show()

"""
 ======================================================================
LATTICE CVP: Comparing Babai's Rounding vs Nearest Plane
======================================================================

Original Basis: v₁=(5,1), v₂=(-2,8)
Target Point: (27,8)

======================================================================

[1] GOOD BASIS (Nearly Orthogonal)
WARNING:matplotlib.axes._base:Ignoring fixed x limits to fulfill fixed data aspect with adjustable data limits.
    cos(θ) = -0.0476 → Nearly perpendicular ✓
    TRUE CVP:       (25,5) - distance: 3.606
    Nearest Plane:  (30,6) - distance: 3.606
    Rounding:       (30,6) - distance: 3.606

[2] SAME LATTICE, SKEWED BASIS (Unimodular Transform)
    Transform: [[1,1],[0,1]] → v₁'=(3,9), v₂'=(-2,8)
WARNING:matplotlib.axes._base:Ignoring fixed x limits to fulfill fixed data aspect with adjustable data limits.
WARNING:matplotlib.axes._base:Ignoring fixed x limits to fulfill fixed data aspect with adjustable data limits.
    cos(θ) = 0.8437 → Highly skewed
    TRUE CVP:       (25,5) - distance: 3.606
    Nearest Plane:  (10,2) - distance: 18.028
    Rounding:       (28,14) - distance: 6.083

[3] BAD BASIS (Nearly Parallel - DIFFERENT LATTICE)
WARNING:matplotlib.axes._base:Ignoring fixed x limits to fulfill fixed data aspect with adjustable data limits.
    Basis: v₁=(37,41), v₂=(39,43)
    cos(θ) = 1.0000 → Nearly parallel (WORST!)
    TRUE CVP:       (18,18) - distance: 13.454
    Nearest Plane:  (0,0) - distance: 28.160
    Rounding:       (17,-3) - distance: 14.866

======================================================================
VERIFICATION: Same Lattice → Same CVP
======================================================================
Bases 1 & 2 (same lattice): True
  → Basis 1 TRUE CVP: (25, 5)
  → Basis 2 TRUE CVP: (25, 5)

Basis 3 (different lattice): True
  → Basis 3 TRUE CVP: (18, 18)

======================================================================
ALGORITHM COMPARISON
======================================================================

📊 Performance Summary:

  Basis 1 (Good, cos=-0.048):
    Rounding correct:      False
    Nearest Plane correct: False

  Basis 2 (Skewed, cos=0.844):
    Rounding correct:      False
    Nearest Plane correct: False

  Basis 3 (Parallel, cos=1.000):
    Rounding correct:      False
    Nearest Plane correct: False

======================================================================
KEY INSIGHTS
======================================================================

🔹 Babai's ROUNDING:
   • Simplest & fastest
   • Only optimal for orthogonal bases
   • Fails on skewed bases

🔹 Babai's NEAREST PLANE:
   • Better approximation than rounding
   • Still may fail on highly skewed bases
   • Polynomial time: O(n²)

🔹 TRUE CVP (Exhaustive Search):
   • Always finds correct answer
   • Exponential time in general
   • Lattice-dependent, not basis-dependent
WARNING:matplotlib.axes._base:Ignoring fixed y limits to fulfill fixed data aspect with adjustable data limits.
WARNING:matplotlib.axes._base:Ignoring fixed y limits to fulfill fixed data aspect with adjustable data limits.

"""