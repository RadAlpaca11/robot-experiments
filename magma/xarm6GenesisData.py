import numpy as np
import cv2
from PIL import Image
# import torch
from xarm.wrapper import XArmAPI  # Import xarm-python-sdk
import genesis as gs
from scipy.spatial.transform import Rotation

# libraries for data collection
from itertools import product
import random
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Function to convert quaternion to Euler angles
def quatToEuler(q, scalarFirst=True, order='xyz', degrees=False):
    if scalarFirst:
        q = [q[1], q[2], q[3], q[0]]
    r = Rotation.from_quat(q)
    return r.as_euler(order, degrees=degrees)

# Function to get the frame from the camera
def getFrame(cam):
    output = cam.render()
    imageData = output[0]
    frame = cv2.cvtColor(imageData, cv2.COLOR_BGR2RGB)
    return frame

# Initialize the robot.
remoteArm = XArmAPI('172.20.5.100')


def initialize_robot(remoteArm):
    remoteArm.clean_warn()
    remoteArm.clean_error()
    remoteArm.motion_enable(True)
    remoteArm.set_mode(2)
    remoteArm.set_state(0)
    # arm.move_gohome()

initialize_robot(remoteArm)

# Initialize Genesis
gs.init(backend=gs.cpu)

scene = gs.Scene(
    show_viewer = True,
    # this is the viewer window that opens while the simulation is running, rather than the camera that records the video
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (3.5, 0.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        max_FPS       = 60,
    ),
    vis_options = gs.options.VisOptions(
        show_world_frame = True,
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

# for vla
cam = scene.add_camera(
    res    = (640, 480),
    pos    = (-2.5, 3, 1.8),
    lookat = (1, 0, 0),
    fov    = 15,
    GUI    = False,
)

scene.build()
camFilm.start_recording()

# set up motors and joints
motors_dof = np.arange(6)

jnt_names = [
    'joint1',
    'joint2',
    'joint3',
    'joint4',
    'joint5',
    'joint6'
]
dofs_idx = [xarm6.get_joint(name).dof_idx_local for name in jnt_names]

# pulled from urdf
xarm6.set_dofs_kp(
    np.array([100, 100, 100, 100, 100, 100]),
    motors_dof
)
xarm6.set_dofs_kv(
    np.array([40, 40, 40, 40, 40, 40]),
    motors_dof
)
xarm6.set_dofs_force_range(
    np.array([-6.28318530718, -2.059, -3.8, -6.28318530718, -1.69297, -6.28318530718]),
    np.array([6.28318530718, 2.0944, 0.19198, 6.28318530718, 3.14159265359, 6.28318530718]),
    motors_dof
)

# get the end-effector link
end_effector = xarm6.get_link('link6')


# print(end_effector.get_pos())
# print(xarm6.get_dofs_position())

# # zero position
# zeroPos = np.array([0, 0, 0, 0, 0, 0])
# xarm6.control_dofs_position(
#     zeroPos,
#     dofs_idx
# )
# for i in range(250):
#     scene.step()
#     camFilm.render()
# frame = getFrame(cam)
# cv2.imwrite('picsAndVids/positions/zeroPos.jpg', frame)
# rotated position
# rest position



# Define the ranges for each joint
jointRanges = [
    [0, 6.28319],  # Joint 1 range
    [-2.05949, 2.0944],  # Joint 2 range
    [-3.92699, 0.191986],  # Joint 3 range
    [0, 6.28319],  # Joint 4 range
    [-1.69297, 3.14159],  # Joint 5 range
    [0, 6.28319],  # Joint 6 range
]

# Number of steps per joint
n = 10  # Adjust this based on how fine you want the discretization

# Discretize each joint's range
discretizedJoints = [
    np.linspace(r[0], r[1], n) for r in jointRanges
]

# Generate all combinations of joint positions
jointCombinations = list(product(*discretizedJoints))
# print(f"Total combinations: {len(jointCombinations)}")

# number of positions you want to use
# the data will record the zero position, and then 5 random positions
# so 6 total
randomSamples = random.sample(jointCombinations, 5)
# print(f"Random samples: {randomSamples}")

# Defining finger joints
fingers = (0.81, 0.88, 0.81, 0.88, -0.8, -0.8)

# Setting up the data for the file
columns = ['episodeIdx', 'observedPosition', 'controlPosition', 'image']

episodeIdx = np.array([])
observedPosition = np.array([])
controlPosition = np.array([])
image = np.array([])

ep = 0
# zero position
zeroPos = np.array([0, 0, 0, 0, 0, 0])
xarm6.control_dofs_position(
    zeroPos,
    dofs_idx
)
for i in range(250):
    scene.step()
    camFilm.render()
# getting the data from the simulation
frame = getFrame(cam)
cv2.imwrite('lerobotTests/picsAndVids/ep' + str(ep) + '.jpg', frame)
currentPos = xarm6.get_dofs_position()

# Adding the data to the lists
episodeIdx = np.append(episodeIdx, ep)
observedPosition = np.append(observedPosition, currentPos)
controlPosition = np.append(controlPosition, zeroPos)
image = np.append(image, 'picsAndVids/ep' + str(ep) + '.jpg')

# incrementing the episode index
ep += 1

# goes through and uses the random positions to move, get the data, and add the data to the lists
for sample in randomSamples:
    print(sample)
    xarm6.control_dofs_position(
        np.array(sample),
        dofs_idx,
    )
    for i in range(100):
        scene.step()
        camFilm.render()
    frame = getFrame(cam)
    cv2.imwrite('lerobotTests/picsAndVids/ep' + str(ep) + '.jpg', frame)
    
    currentPos = xarm6.get_dofs_position()

    episodeIdx = np.append(episodeIdx, ep)
    observedPosition = np.vstack((observedPosition, currentPos))
    controlPosition = np.vstack((controlPosition, np.array(sample)))
    image = np.append(image, 'picsAndVids/ep' + str(ep) + '.jpg')
    ep += 1

# saves the recorded video
camFilm.stop_recording(save_to_filename='video.mp4')

# Converts the data that is arrays, to a list that can be written to the file
observedPosition = observedPosition.tolist()
controlPosition = controlPosition.tolist()

# puts the data into a pandas dataframe
df = pd.DataFrame({
    'episodeIdx': episodeIdx,
    'observedPosition': observedPosition,
    'controlPosition': controlPosition,
    'image': image
})

# converts the data to a parquet file
table = pa.Table.from_pandas(df)
# writes the data to a parquet file
pq.write_table(table, 'lerobotTests/robotDataTest.parquet')