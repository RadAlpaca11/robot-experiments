from scipy.spatial.transform import Rotation

def quat_to_euler(q, order='xyz', degrees=False):
  """
  Converts a quaternion to Euler angles.

  Args:
    q: A sequence of four numbers representing the quaternion (x, y, z, w).
    order: A string specifying the order of Euler angle rotations. 
           Defaults to 'xyz' (roll, pitch, yaw).
    degrees: A boolean indicating whether to return angles in degrees 
             (True) or radians (False). Defaults to False (radians).

  Returns:
    A NumPy array of three Euler angles.
  """

  r = Rotation.from_quat(q)
  return r.as_euler(order, degrees=degrees)

# Example usage:
quaternion = [1, 0, 0.707, 0.707] # Example quaternion
euler_angles_rad = quat_to_euler(quaternion)
euler_angles_deg = quat_to_euler(quaternion, degrees=True)

print("Euler angles (radians):", euler_angles_rad)
print("Euler angles (degrees):", euler_angles_deg)