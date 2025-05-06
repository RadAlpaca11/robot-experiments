| Real robot | Model | Status |
| --- | --- | --- | 
| Kuka | [Kuka](genesis/mujoco_menagerie/kuka_iiwa_14/iiwa14.xml) | [Working in genesis](genesis/kukaKinematics.py), [integrated with openVLA](openVLA/openVLAgenKuka.py)|
| Rethink Robotics Sawyer| [sawyer](genesis/mujoco_menagerie/rethink_robotics_sawyer/sawyer.xml) |
| Universal robots UR 10 (with shadow hand)| [UR10e arm](genesis/mujoco_menagerie/universal_robots_ur10e/ur10e.xml) |
|Shadow hand| [Shadow Hand (right)](genesis/mujoco_menagerie/shadow_hand/right_hand.xml) |
| Dobot CR5 |
| XARM 6 | [xarm6 (no gripper)](models/ManiSkill-XArm6/xarm6_nogripper.urdf) [xarm6 modified to be raised like the arm in the lab (no gripper)](models/ManiSkill-XArm6/mod_xarm6_nogripper.urdf) [xarm6 modified to be raised like the arm in the lab (with gripper)](models/ManiSkill-XArm6/mod_xarm6_robotiq.urdf) | [working with genesis and magma](magma/xarm6MagmaGen.py) [digital twin](magma/xarm6DigitalTwin.py) and more in the [magma folder](magma)