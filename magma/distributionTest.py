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

def waypointPlan (numWaypoints=100, jointAngles = [
    [0, 360], 
    [-118, 120], 
    [-225, 11], 
    [0, 360], 
    [-97, 180], 
    [0, 360] 
    ]):
    rem = numWaypoints % len(jointAngles)

    splitWaypoints = (numWaypoints - rem) / len(jointAngles)
    

import math

def inverseFact(n):
    if n < 0:
        raise ValueError("Input must be a non-negative integer")

    # Start from 1!
    i = 1
    fact = 1
    while fact < n:
        i += 1
        fact *= i

    # Compare n with i! and (i-1)!
    prevFact = fact // i
    if abs(prevFact - n) <= abs(fact - n):
        return prevFact, i - 1
    else:
        return fact, i

# Example usage
number = int(input("Enter an integer: "))
nearestFact, factOf = inverseFact(number)
print(f"The nearest factorial to {number} is {nearestFact} ({factOf}!).")


inverseFact(100) # 5
print(inverseFact(100))