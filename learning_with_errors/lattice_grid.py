import matplotlib.pyplot as plt
import random

def generate_random_lattice_points(x1, y1, x2, y2, range_val=10):
    """Generate lattice points from basis vectors"""
    x_points = []
    y_points = []
    
    for a in range(-range_val, range_val + 1):
        for b in range(-range_val, range_val + 1):
            x_new = a * x1 + b * x2
            y_new = a * y1 + b * y2
            x_points.append(x_new)
            y_points.append(y_new)
    
    return x_points, y_points

# Generate random basis vectors
x1, y1 = random.randint(1, 5), random.randint(1, 5)
x2, y2 = random.randint(-5, 5), random.randint(-5, 5)

# Ensure vectors are not parallel
while x1 * y2 == x2 * y1:  # Check if parallel
    x2, y2 = random.randint(-5, 5), random.randint(-5, 5)

title = f"Lattice Basis: v1=({x1},{y1}), v2=({x2},{y2})"
print(title)

# Generate and plot lattice points
x_points, y_points = generate_random_lattice_points(x1, y1, x2, y2)

plt.figure(figsize=(10, 8))
plt.title(title, fontsize=14)
plt.xlabel('x')
plt.ylabel('y')

# Plot lattice points
plt.scatter(x_points, y_points, color='blue', alpha=0.6, s=30)

# Plot basis vectors
plt.arrow(0, 0, x1, y1, head_width=0.3, head_length=0.3, fc='red', ec='red', linewidth=2, label='Basis v1')
plt.arrow(0, 0, x2, y2, head_width=0.3, head_length=0.3, fc='green', ec='green', linewidth=2, label='Basis v2')

plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)
plt.legend()
plt.axis('equal')

# Set reasonable axis limits
max_val = max(max(abs(x) for x in x_points), max(abs(y) for y in y_points))
plt.xlim(-max_val-2, max_val+2)
plt.ylim(-max_val-2, max_val+2)

plt.tight_layout()
plt.savefig('random_lattice.png', dpi=150)
plt.show()

print(f"Generated {len(x_points)} lattice points")
print(f"Saved as 'random_lattice.png'")

"""

"""