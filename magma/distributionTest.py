from itertools import product

# Define the ranges for each joint
joint_ranges = [
    [0, 360],  # Joint 1 range
    [-118, 120],  # Joint 2 range
    [-225, 11],  # Joint 3 range
    [0, 360],  # Joint 4 range
    [-97, 180],  # Joint 5 range
    [0, 360],  # Joint 6 range
]

# Number of steps per joint
n = 10  # Adjust this based on how fine you want the discretization

# Discretize each joint's range
discretized_joints = [
    [r[0] + i * (r[1] - r[0]) / (n - 1) for i in range(n)] for r in joint_ranges
]

# Generate all combinations
joint_combinations = list(product(*discretized_joints))
print(f"Total combinations: {len(joint_combinations)}")

import random

k = 10  # Number of combinations to sample
sampled_combinations = random.sample(joint_combinations, k)
print(f"Sampled combinations: {sampled_combinations}")