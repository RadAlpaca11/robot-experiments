# This code will not run. 
# The purpose of this code is to provide an outline for how you could integrate a VLA with genesis.
# You will need to add code where noted to make this work with your VLA.
# We create a scene that spawns a Panda arm, and a block.

# Import libraries
import numpy as np
import genesis as gs
import cv2
from PIL import Image
# Add any other libraries required for your VLA


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
    gs.morphs.MJCF(file='path/to/file',) # Replace the path with the path to your model
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

# Camera setup, you should finetune the settings to fit your needs
# camFilm is the camera that is used to film the scene so that you have a video at the end
cam = scene.add_camera(
    res = (640, 480),
    pos = (0.5, -1.5, 0.5),
    lookat = (0.5, 0.0, 0.5),
    fov = 30,
    GUI = True,
)

camFilm = scene.add_camera(
    res = (640, 480),
    pos = (0.5, -1.5, 0.5),
    lookat = (0.5, 0.0, 0.5),
    fov = 30,
    GUI = True,
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

# The scene is now set up
# Add code here to integrate with your VLA
# Add initialization, processor import, and prompt here.

for i in range(100): # This is how many times the vla will evaluate the scene
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

    # Add code here to feed image and prompt to VLA
    action = output # Add code here to get the output from the VLA, which should be an array of floats

    qpos = panda.inverse_kinematics(
        link = end_effector,
        pos = np.array([currentPos[0]+action[0], currentPos[1]+action[1], currentPos[2]+action[2]]),
        # If your VLA outputs seven values, that means that the rotational values are an euler transformation, if it is 8 it is quaterion
        quat = np.array([currentPos[3]+action[3], currentPos[4]+action[4], currentPos[5]+action[5], currentPos[6]+action[6]]),
    )
    
    panda.control_dofs_position(qpos[:-2], motors_dof)  # This is the code that actually moves the arm. The [:-2] is because the last two values are the fingers, and we are not using those

camFilm.stop_recording(save_to_filename='film.mp4') # Save the final video