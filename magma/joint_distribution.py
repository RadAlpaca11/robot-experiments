from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np

@dataclass
class Joint:
    name: str
    start: float
    end: float

def generateJointPoints(total_points: int, weights: Dict[str, float], joints: Dict[str, Joint]) -> List[Tuple[float, ...]]:
    if abs(sum(weights.values()) - 1) > 0.0001:
        raise ValueError("Weights must sum to 100")
    
    result = []
    joint_names = sorted(joints.keys())
    
    # Calculate change frequencies based on weights
    changes_per_joint = {
        joint: max(1, int(round((weight / 100) * total_points)))
        for joint, weight in weights.items()
    }
    
    # Generate base values for each joint
    current_values = {
        joint_name: np.linspace(joints[joint_name].start, joints[joint_name].end, changes_per_joint[joint_name])
        for joint_name in joint_names
    }
    
    # Generate exactly total_points combinations
    for i in range(total_points):
        point = []
        for joint_name in joint_names:
            # Select value based on position in sequence
            idx = i % len(current_values[joint_name])
            point.append(current_values[joint_name][idx])
        result.append(tuple(point))
    
    return result

if __name__ == "__main__":
    joints = {
        "j1": Joint("j1", -180, 180),
        "j2": Joint("j2", -90, 90),
        "j3": Joint("j3", -170, 170),
        "j4": Joint("j4", -180, 180),
        "j5": Joint("j5", -120, 120),
        "j6": Joint("j6", -360, 360)
    }
    
    weights = {
        "j1": 0.35, 
        "j2": 0.25, 
        "j3": 0.15,
        "j4": 0.10, 
        "j5": 0.05, 
        "j6": 0.10
    }
    
    requested_points = 10
    points = generateJointPoints(requested_points, weights, joints)
    print(f"Generated exactly {len(points)} points:")
    for point in points:
        print(point)