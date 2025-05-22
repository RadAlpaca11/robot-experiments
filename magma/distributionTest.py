from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class Joint:
    name: str
    start: float
    end: float

def generate_joint_points(total_points: int, weights: Dict[str, float], joints: Dict[str, Joint]) -> Dict[str, np.ndarray]:
    """
    Generate weighted distribution of points across joint ranges
    
    Args:
        total_points: Total number of points to distribute
        weights: Dictionary of joint names and their weights (should sum to 100)
        joints: Dictionary of joint names and their range information
    
    Returns:
        Dictionary of joint names and their calculated points
    """
    # Validate weights
    if abs(sum(weights.values()) - 1) > 0.0001:
        raise ValueError("Weights must sum to 100")
    
    # Calculate points per joint based on weights
    points_per_joint = {
        joint: int(round(weight * total_points))
        for joint, weight in weights.items()
    }
    
    # Adjust for rounding errors
    points_diff = total_points - sum(points_per_joint.values())
    if points_diff != 0:
        # Add/subtract remaining points to/from the joint with highest weight
        max_weight_joint = max(weights.items(), key=lambda x: x[1])[0]
        points_per_joint[max_weight_joint] += points_diff
    
    # Generate points for each joint
    result = {}
    for joint_name, num_points in points_per_joint.items():
        if num_points > 0:
            joint = joints[joint_name]
            result[joint_name] = np.linspace(joint.start, joint.end, num_points)
        else:
            result[joint_name] = np.array([])
            
    return result

# Example usage
if __name__ == "__main__":
    # Define joints
    joints = {
        "j1": Joint("j1", -180, 180),
        "j2": Joint("j2", -90, 90),
        "j3": Joint("j3", -170, 170),
        "j4": Joint("j4", -180, 180),
        "j5": Joint("j5", -120, 120),
        "j6": Joint("j6", -360, 360)
    }
    
    # Define weights (must sum to 100)
    weights = {
        "j1": 0.35,
        "j2": 0.25,
        "j3": 0.15,
        "j4": 0.10,
        "j5": 0.05,
        "j6": 0.10
    }
    
    # Generate 100 total points
    result = generate_joint_points(100, weights, joints)
    
    # Print results
    for joint_name, points in result.items():
        print(f"{joint_name}: {len(points)} points")
        print(points)
        print()
    print(len(result))