# Import libraries
import numpy as np
import genesis as gs
import cv2
from PIL import Image
from src.openpi.training import config
from src.openpi.policies import policy_config
from src.openpi.shared import download



# Initialize genesis
gs.init(backend=gs.cpu)

# Load the scene
scene = gs.Scene( # This is just an example scene
    show_viewer    = True,
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (3.5, 0.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        max_FPS       = 60,
    ),
    vis_options = gs.options.VisOptions(
        show_world_frame = True, # visualize the coordinate frame of `world` at its origin
        world_frame_size = 1.0, # length of the world frame in meters
        show_link_frame  = False, # do not visualize coordinate frames of entity links
        show_cameras     = False, # do not visualize mesh and frustum of the cameras added
        plane_reflection = True, # turn on plane reflection
        ambient_light    = (0.1, 0.1, 0.1), # ambient light setting
    ),
    sim_options = gs.options.SimOptions(
        dt = 0.01,
        substeps = 4,
    ),
    renderer = gs.renderers.Rasterizer(), # using rasterizer for camera rendering
)

plane = scene.add_entity(gs.morphs.Plane())

panda = scene.add_entity(
    gs.morphs.MJCF(file='././genesis/mujoco_menagerie/franka_emika_panda/panda.xml',)
)

cube = scene.add_entity(
    gs.morphs.Box(
        size = (0.04, 0.04, 0.08),
        pos = (0.65, 0.0, 0.25),
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
    GUI    = True,
)
# for openVLA
cam = scene.add_camera(
    res    = (640, 480),
    pos    = (1.25, -2.5, 1.3),
    lookat = (0.65, 0, 0.25),
    fov    = 20,
    GUI    = True,
)

scene.build()
camFilm.start_recording()

motors_dof = np.arange(7)
fingers_dof = np.arange(7,9)

# These values are tuned for the specific robot (panda)
panda.set_dofs_kp(
    np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]),
)
panda.set_dofs_kv(
    np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
)
panda.set_dofs_force_range(
    np.array([-87, -87, -87, -87, -12, -12, -12, -100, -100]),
    np.array([87, 87, 87, 87, 12, 12, 12, 100, 100]),
)

# Get the end-effector link
end_effector = panda.get_link('hand')

# Set a starting position
qpos = panda.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.0, 0.25]),
    quat = np.array([0, 1, 0, 0]),
)
panda.control_dofs_position(qpos[:-2], motors_dof)

# Allow time for the arm to move to the starting position
for i in range(100):
    scene.step()

config = config.get_config("pi0_fast_droid")
checkpoint_dir = download.maybe_download("s3://openpi-assets/checkpoints/pi0_fast_droid")

# Create a trained policy.
policy = policy_config.create_trained_policy(config, checkpoint_dir)


for i in range(5): # This is how many times the vla will evaluate the scene
    cam.start_recording()
    for i in range(25): # This is how many times the scene will step in between evaluations
        scene.step()
        cam.render()
        camFilm.render()

    # Save the clip that the we will use for the VLA
    cam.stop_recording(save_to_filename='clip.mp4')

    # This tells us the current position of the grabber
    # The output is a tensor array that might look something like this: 
    # tensor([ 6.4834e-01, -4.6508e-04,  2.4258e-01]) 
    currentPos = end_effector.get_pos()
    currentQuat = end_effector.get_quat()


    video = cv2.VideoCapture('clip.mp4')
    video.set(cv2.CAP_PROP_POS_FRAMES, 24) # We reccomend setting the frame to 1 less than the number of frames rendered
    # ret returns a boolean value. If the frame is read correctly, it will be True
    ret, frame = video.read()
    cv2.imwrite('frame.jpg', frame)
    image = Image.open('frame.jpg')

    jointPositions= panda.get_dofs_position()
    print (jointPositions[:7])
    print(jointPositions[7:8])
    inputs = {
    "observation/exterior_image_1_left": image,
    "observation/wrist_image_left": image,
    # might be able to add other camera perspectives here
    "observation/joint_position": jointPositions[:7],
    "observation/gripper_position": jointPositions[7:8],
    "prompt": "touch the yellow block"
    }
    action_chunk = policy.infer(inputs)["actions"]
    print(action_chunk[1])
    for action in action_chunk:
        qpos = panda.inverse_kinematics(
            link = end_effector,
            pos = np.array([currentPos[0]+action[0], currentPos[1]+action[1], currentPos[2]+action[2]]),
            # If your VLA outputs seven values, that means that the rotational values are an euler transformation, if it is 8 it is quaterion
            quat = np.array([currentQuat[0]+action[3], currentQuat[1]+action[4], currentQuat[2]+action[5], currentQuat[3]+action[6]]),
        )
        panda.control_dofs_position(qpos[:-2], motors_dof)
        for i in range(50):
            scene.step()
            camFilm.render()