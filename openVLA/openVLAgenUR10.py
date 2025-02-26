# genesis stuff

import genesis as gs
import numpy as np
import cv2


# openVLA stuff
from transformers import AutoModelForVision2Seq, AutoProcessor
from PIL import Image

import torch

# Load Processor & VLA
processor = AutoProcessor.from_pretrained("openvla/openvla-7b", trust_remote_code=True)
vla = AutoModelForVision2Seq.from_pretrained(
    "openvla/openvla-7b", 
    #attn_implementation="flash_attention_2",  # [Optional] Requires `flash_attn`
    torch_dtype=torch.bfloat16, 
    low_cpu_mem_usage=True, 
    trust_remote_code=True
).to("cuda:0")

# Grab image input & format prompt
#image: Image.Image = 'get_from_camera(...)'
prompt = "In: What action should the robot take to touch the yellow block?\nOut:"
#prompt = "In: What action should the robot take to pick up the coke can?\nOut:"

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
    renderer=gs.renderers.Rasterizer(),
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
ur10 = scene.add_entity(
    gs.morphs.URDF(file='./ur_description/ur10_robot.urdf', pos = (0, 0, 0.12),),
)
box = scene.add_entity(
    gs.morphs.Box(
        size=(0.2, 0.2, 0.2),
        pos=(0.65, 0, 0.25),
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
fingers_dof = np.arange(7,8)
print(motors_dof)
print(fingers_dof)

dofs_idx = np.concatenate((motors_dof, fingers_dof))
lower = np.array([-50, -50, -30, -30, -30, -20, -20, -50])
upper = np.array([50, 50, 30, 30, 30, 20, 20, 50])

# Set the DOFs force range
ur10.set_dofs_force_range(lower, upper, dofs_idx)


# size1 -50 50
# size2 -30 30
# size3 -20 20

# ur10.set_dofs_kp(
#     np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100]),
# )
# ur10.set_dofs_kv(
#     np.array([450, 450, 350, 350, 200, 200, 200, 10]),
# )
# ur10.set_dofs_force_range(
#     np.array([-50, -50, -30, -30, -30, -20, -20, -50]),
#     np.array([50, 50, 30, 30, 30, 20, 20, 50]),
# )

# get the end-effector link
end_effector = ur10.get_link('ur10_gripper_base_link')

# starting position
qpos = ur10.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.0, 0.25]),
    quat = np.array([0, 1, 0, 0]),
)
print(len(qpos))
print(len(qpos[:-1]))
print(len(qpos[:-2]))
print(len(qpos[:-3]))
print(len(qpos[:-4]))
print(len(qpos[:-5]))
print(len(qpos[:-6]))

ur10.control_dofs_position(qpos[:-6], motors_dof)

for i in range(20):
    cam.start_recording()
    for i in range(25):
        scene.step()
        cam.render()
        camFilm.render()

    cam.stop_recording(save_to_filename='clip.mp4')

    currentPos = end_effector.get_pos()
    print(currentPos)

    video = cv2.VideoCapture('clip.mp4')
    video.set(cv2.CAP_PROP_POS_FRAMES, 9)
    ret, frame = video.read()
    print(ret)
    cv2.imwrite('frame.jpg', frame)
    image = Image.open('frame.jpg')

    inputs = processor(prompt, image).to("cuda:0", dtype=torch.bfloat16)
    action = vla.predict_action(**inputs, unnorm_key="bridge_orig", do_sample=False)

    qpos= ur10.inverse_kinematics(
        link = end_effector,
        pos = np.array([currentPos[0]-action[1], currentPos[1]-action[0], currentPos[2]+action[2]]),
    )

    ur10.control_dofs_position(qpos[:-6], motors_dof)


camFilm.stop_recording(save_to_filename='openVLA/picsAndVids/test.mp4')
# Execute...
# robot.act(action, ...)
# print(robot.act(action, ...))
#print(action)
