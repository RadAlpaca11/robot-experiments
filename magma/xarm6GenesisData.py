import numpy as np
import cv2
# from PIL import Image
import torch
from pytorch3d.transforms import quaternion_to_matrix, matrix_to_euler_angles
# from xarm.wrapper import XArmAPI  # Import xarm-python-sdk
import genesis as gs
from scipy.spatial.transform import Rotation

# libraries for data collection
from itertools import product
import random
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# for huggingface
from huggingface_hub import HfApi
api = HfApi()

# Function to convert quaternion to Euler angles
def quatToEuler(q, scalarFirst=True, order='xyz', degrees=False, cpu=False):
    if cpu:
        q = q[0]
        # print(q)
        if scalarFirst:
            q = [q[1], q[2], q[3], q[0]]
        r = Rotation.from_quat(q)
        return r.as_euler(order, degrees=degrees)
    else:
        q = q[0]
        # print(q)
        if scalarFirst==False:
            q = [q[3], q[0], q[1], q[2]]
        q = quaternion_to_matrix(q)
        r = matrix_to_euler_angles(q, 'XYZ')
        return r

# Function to get the frame from the camera
def getFrame(cam):
    output = cam.render()
    imageData = output[0]
    frame = cv2.cvtColor(imageData, cv2.COLOR_BGR2RGB)
    return frame

# # Initialize the robot.
# remoteArm = XArmAPI('172.20.5.100')

# def initialize_robot(remoteArm):
#     remoteArm.clean_warn()
#     remoteArm.clean_error()
#     remoteArm.motion_enable(True)
#     remoteArm.set_mode(2)
#     remoteArm.set_state(0)
#     # arm.move_gohome()

# initialize_robot(remoteArm)

# Initialize Genesis
gs.init(backend=gs.gpu)

scene = gs.Scene(
    show_viewer = False,
    # this is the viewer window that opens while the simulation is running, not the camera that records the video
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (3.5, 0.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        max_FPS       = 60,
    ),
    vis_options = gs.options.VisOptions(
        show_world_frame = False,
        world_frame_size = 1.0,
        show_link_frame  = False,
        show_cameras     = False,
        plane_reflection = True,
        ambient_light    = (0.1, 0.1, 0.1),
    ),
        sim_options = gs.options.SimOptions(
        dt = 0.01,
        substeps = 4,
    ),
    rigid_options=gs.options.RigidOptions(
        enable_self_collision=True,
    ),
    renderer=gs.renderers.Rasterizer(),
    show_FPS=False
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
xarm6 = scene.add_entity(
    gs.morphs.URDF(file='../models/ManiSkill-XArm6/mod_xarm6_robotiq.urdf'),

)

box1 = scene.add_entity(
    gs.morphs.Box(
        size=(0.05, 0.05, 0.05),
        pos=(1, 0, 0.0),
    ),
    surface=gs.surfaces.Default(
        color=(1, 0.8, 0),
    )
)


# for long video
camFilm = scene.add_camera(
    res    = (640, 480),
    pos    = (3.5, 0.0, 2.5),
    lookat = (0.65, 0, 0.25),
    fov    = 20,
    GUI    = False,
)

# for data
cam = scene.add_camera(
    res    = (640, 480),
    pos    = (-2.5, 3, 1.8),
    lookat = (0, 0, 0.25),
    fov    = 15,
    GUI    = False,
)

envNum = 10000
scene.build(n_envs=envNum, env_spacing=(4, 4), n_envs_per_row=envNum, center_envs_at_origin=False) # offsets y by 4 in one row

camFilm.start_recording()
cam.start_recording()

# set up motors and joints
motors_dof = np.arange(10)

jnt_names = [
    'joint1',
    'joint2',
    'joint3',
    'joint4',
    'joint5',
    'joint6',
    'left_outer_knuckle_joint',
    'left_inner_finger_joint',
    'right_outer_knuckle_joint',
    'right_inner_finger_joint'
]
dofs_idx = [xarm6.get_joint(name).dof_idx_local for name in jnt_names]

# Turns out these were making things worse, and we could just let the model do it's thing.
# # pulled from urdf
# xarm6.set_dofs_kp(
#     np.array([100, 100, 100, 100, 100, 100, 10, 10, 10, 10]),
#     motors_dof
# )
# xarm6.set_dofs_kv(
#     np.array([40, 40, 40, 40, 40, 40, 2, 2, 2, 2]),
#     motors_dof
# )
# xarm6.set_dofs_force_range(
#     np.array([-50, -50, -32, -32, -32, -20,  -1000, -1000, -1000, -1000]),
#     np.array([50, 50, 32, 32, 32, 20, 1000, 1000, 1000, 1000]),
#     motors_dof
# )

# get the end-effector link
end_effector = xarm6.get_link('link6')

# defining the gripper positions
gripperOpenPos = torch.Tensor([0, 0, 0, 0])
gripperOpenPos = gripperOpenPos.to(0)
gripperClosePos = torch.Tensor([0.81, -0.88, 0.81, -0.88])
gripperClosePos = gripperClosePos.to(0)


from typing import List, Dict, Tuple
import numpy as np

def generateJointPoints(total_points: int, weights: Dict[str, float], joints: List[str], lowerRange: Dict[str, float], upperRange: Dict[str, float]) -> List[Tuple[float, ...]]:
    if abs(sum(weights.values()) - 1) > 0.0001:
        raise ValueError("Weights must sum to 1")
    
    result = []
    joint_names = joints
    # print(joint_names)

    
    # Calculate change frequencies based on weights
    changes_per_joint = {
        joint: max(1, int(round(weight* total_points)))
        for joint, weight in weights.items()
    }
    
    # Generate base values for each joint
    current_values = {
        joint_name: np.linspace(lowerRange[joint_name], upperRange[joint_name], changes_per_joint[joint_name])
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


joints = [
    'j1',
    'j2',
    'j3',
    'j4',
    'j5',
    'j6'
]

weights = {
    'j1': 0.35,
    'j2': 0.25,
    'j3': 0.15,
    'j4': 0.10,
    'j5': 0.05,
    'j6': 0.10
}

lowerRange = {
    'j1': 0,  # Joint 1 range
    'j2': -2.05949,  # Joint 2 range
    'j3': -3.92699,  # Joint 3 range
    'j4': 0,  # Joint 4 range
    'j5': -1.69297,  # Joint 5 range
    'j6': 0,  # Joint 6 range
}

upperRange = {
    'j1': 6.28319,  # Joint 1 range
    'j2': 2.0944,  # Joint 2 range
    'j3': 0.191986,  # Joint 3 range
    'j4': 6.28319,  # Joint 4 range
    'j5': 3.14159,  # Joint 5 range
    'j6': 6.28319,  # Joint 6 range
}


comboNums = envNum/2
comboNums = int(comboNums-1)
points = generateJointPoints(comboNums, weights, joints, lowerRange, upperRange)
# print(f"Generated exactly {len(points)} points:")


# Setting up the data for the file
columns = ['episodeIdx', 'endEffectorPosition', 'observedJointAngles', 'targetJointAngles', 'deltaAngles', 'gripperOpen', 'image']

episodeIdx = np.array([]) # the index of the episode
gripperOpen = np.array([]) # list if the gripper is open or closed (boolean)
image = np.array([]) # list of paths to the images


ep = 0
# zero positions
zeroPos = torch.Tensor([0, 0, 0, 0, 0, 0, gripperOpenPos[0], gripperOpenPos[1], gripperOpenPos[2], gripperOpenPos[3]])
xarm6.control_dofs_position(
    zeroPos,
    dofs_idx,
    envs_idx=[ep],
)
zeroPos = zeroPos.to(0)
zeroPos = zeroPos.unsqueeze(0)
# Adding the data to the lists
episodeIdx = np.append(episodeIdx, ep)
targetJointAngles = zeroPos
# print(targetJointAngles.shape)
# print(targetJointAngles)
targetJointAngles = targetJointAngles.to(0)
gripperOpen = np.append(gripperOpen, True)

# incrementing the episode index
ep += 1

zeroPos = torch.Tensor([0, 0, 0, 0, 0, 0, gripperClosePos[0], gripperClosePos[1], gripperClosePos[2], gripperClosePos[3]])
zeroPos = zeroPos.to(0)
zeroPos = zeroPos.unsqueeze(0)
xarm6.control_dofs_position(
    zeroPos,
    dofs_idx,
    envs_idx=[ep]
)

# Adding the data to the lists
episodeIdx = np.append(episodeIdx, ep)
targetJointAngles = torch.cat((targetJointAngles, zeroPos), dim=0)
# print(targetJointAngles.shape)
# print(targetJointAngles)
gripperOpen = np.append(gripperOpen, False)

# incrementing the episode index
ep += 1

# goes through and uses the random positions to move, get the data, and add the data to the lists
for sample in points:
    # print("ep:", ep)
    # print(sample)
    sample1 = torch.Tensor(sample)
    sample1 = sample1.to(0)
    goToPos = torch.cat((sample1, gripperOpenPos))
    # print(goToPos)
    # print(goToPos.shape)
    xarm6.control_dofs_position(
        goToPos,
        dofs_idx,
        envs_idx=[ep]
    )

    goToPos = goToPos.unsqueeze(0)
    episodeIdx = np.append(episodeIdx, ep)
    targetJointAngles = torch.cat((targetJointAngles, goToPos), dim=0)
    # deltaAngles = np.vstack((deltaAngles, currentDelta))
    gripperOpen = np.append(gripperOpen, True)

    ep += 1

    sample2 = torch.Tensor(sample)
    sample2 = sample2.to(0)
    goToPos = torch.cat((sample2, gripperClosePos))
    xarm6.control_dofs_position(
        goToPos,
        dofs_idx,
        envs_idx=[ep]
    )
    
    episodeIdx = np.append(episodeIdx, ep)
    goToPos = goToPos.unsqueeze(0)
    targetJointAngles = torch.cat((targetJointAngles, goToPos), dim=0)
    gripperOpen = np.append(gripperOpen, False)

    ep += 1



# Usage in main code:
for i in range(500):
    scene.step()
    camFilm.render()

camPos = [-2.5, 3, 1.8]
camLookAt = [0, 0, 0.25]

# saves the recorded video
camFilm.stop_recording(save_to_filename='lerobotTests/picsAndVids/xarm6/video.mp4')
# cam.stop_recording(save_to_filename='robotCam.mp4')

for env in range(envNum):
    currentPos = xarm6.get_dofs_position(dofs_idx, [env])
    currentWorldPos = end_effector.get_pos([env])
    currentWorldPos = currentWorldPos.to(0)
    currentWorldQuat = end_effector.get_quat([env])
    currentWolrdEuler = quatToEuler(currentWorldQuat, scalarFirst=True)
    currentWolrdEuler = currentWolrdEuler.to(0)
    currentWorldPos = torch.cat((currentWorldPos[0], currentWolrdEuler))
    currentWorldPos = currentWorldPos.unsqueeze(0)
    currentDelta = torch.sub(currentPos, targetJointAngles[env])
    if env == 0:
        endEffectorPosition = torch.Tensor(currentWorldPos) # the end effector position in world coordinates with euler rotation
        endEffectorPosition = endEffectorPosition.to(0)
        observedJointAngles = torch.Tensor(currentPos) # the joint angles of the robot
        observedJointAngles = observedJointAngles.to(0)
        deltaAngles = torch.Tensor(currentDelta) # the difference between the joint angles and the target joint angles
        deltaAngles = deltaAngles.to(0)
        frame = getFrame(cam)
        cv2.imwrite('lerobotTests/picsAndVids/xarm6/ep' + str(env) + '.jpg', frame)
        image = np.append(image, 'lerobotTests/picsAndVids/xarm6/ep' + str(env) + '.jpg')

    else:
        endEffectorPosition = torch.cat((endEffectorPosition, currentWorldPos), dim=0)
        observedJointAngles = torch.cat((observedJointAngles, currentPos), dim=0)
        deltaAngles = torch.cat((deltaAngles, currentDelta), dim=0)
        camPos = [camPos[0], camPos[1]+4, camPos[2]]
        camLookAt = [camLookAt[0], camLookAt[1]+4, camLookAt[2]]
        cam.set_pose(
            pos=camPos,
            lookat=camLookAt,
        )
        frame = getFrame(cam)
        cv2.imwrite('lerobotTests/picsAndVids/xarm6/ep' + str(env) + '.jpg', frame)
        image = np.append(image, 'lerobotTests/picsAndVids/xarm6/ep' + str(env) + '.jpg')


# Converts the data that is arrays, to a list that can be written to the file
endEffectorPosition = endEffectorPosition.tolist()
observedJointAngles = observedJointAngles.tolist()
targetJointAngles = targetJointAngles.tolist()
deltaAngles = deltaAngles.tolist()

# print("episodeIdx length", len(episodeIdx))
# print("endEffectorPosition length", len(endEffectorPosition))
# print("observedJointAngles length", len(observedJointAngles))
# print("targetJointAngles length", len(targetJointAngles))
# print("deltaAngles length", len(deltaAngles))
# print("gripperOpen length", len(gripperOpen))
# print("image length", len(image))

# puts the data into a pandas dataframe
df = pd.DataFrame({
    'episodeIdx': episodeIdx,
    'endEffectorPosition': endEffectorPosition,
    'observedJointAngles': observedJointAngles,
    'targetJointAngles': targetJointAngles,
    'deltaAngles': deltaAngles,
    'gripperOpen': gripperOpen,
    'image': image
})

# # converts the data to a parquet file
table = pa.Table.from_pandas(df)
# writes the data to a parquet file
pq.write_table(table, 'lerobotTests/xarm6RobotDataTest.parquet')

# Uploads the file to huggingface
api.upload_file(
    path_or_fileobj='lerobotTests/xarm6RobotDataTest.parquet',
    path_in_repo='xarm6RobotDataTest.parquet',
    repo_id='RadAlpaca11/lerobotTests',
    repo_type='dataset',
    commit_message='Add robot data test from code',
)
