# genesis stuff

import genesis as gs
import numpy as np
import cv2

gs.init(backend=gs.cpu)

scene = gs.Scene(
    show_viewer = True,
    # this is the viewer window that opens while the simulation is running, rather than the camera that records the video
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (3.5, 0.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 40,
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
    renderer=gs.renderers.Rasterizer(),
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
panda = scene.add_entity(
    gs.morphs.MJCF(file='genesis/mujoco_menagerie/franka_emika_panda/panda.xml'),
)
box = scene.add_entity(
    gs.morphs.Box(
        size=(0.2, 0.2, 0.2),
        pos=(0.5, 0.5, 0.1),
    ),
)



cam1 = scene.add_camera(
    res    = (640, 480),
    pos    = (3.5, 0.0, 0.5),
    lookat = (0, 0, 0),
    fov    = 35,
    GUI    = False,
)
cam2 = scene.add_camera(
    res    = (640, 480),
    pos    = (3.5, 0.0, 0.5),
    lookat = (0, 0, 0),
    fov    = 35,
    GUI    = False,
)



scene.build()

jnt_names = [
    'joint1',
    'joint2',
    'joint3',
    'joint4',
    'joint5',
    'joint6',
    'joint7',
    'finger_joint1',
    'finger_joint2',
]
dofs_idx = [panda.get_joint(name).dof_idx_local for name in jnt_names]

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

panda.control_dofs_position(
    np.array([0, 0, 0, -0.07, 0, 0, 0, 0, 0]),
)

# cam1 for filming, cam2 for processing
cam1.start_recording()
cam2.start_recording()

# openVLA stuff
from transformers import AutoModelForVision2Seq, AutoProcessor
from PIL import Image

import torch

# Load Processor & VLA
processor = AutoProcessor.from_pretrained("openvla/openvla-7b", trust_remote_code=True)
vla = AutoModelForVision2Seq.from_pretrained(
    "openvla/openvla-7b", 
    attn_implementation="flash_attention_2",  # [Optional] Requires `flash_attn`
    torch_dtype=torch.bfloat16, 
    low_cpu_mem_usage=True, 
    trust_remote_code=True
).to("cuda:0")

# Grab image input & format prompt
#image: Image.Image = 'get_from_camera(...)'
prompt = "In: What action should the robot take to touch the block?\nOut:"
#prompt = "In: What action should the robot take to pick up the coke can?\nOut:"

import time

end_effector = panda.get_link('hand')


for i in range(2000):
    scene.step()
    cam1.render()
    cam2.render()

    if(i%10 == 0):
        cam2.stop_recording(save_to_filename='clip.mp4')

        video=cv2.VideoCapture('clip.mp4')
        print(video.isOpened())
        video.set(cv2.CAP_PROP_POS_FRAMES, 1)
        print(video.get(cv2.CAP_PROP_POS_FRAMES))
        time.sleep(1)
        ret, frame = video.read()
        if(ret):

            print(ret)
            cv2.imwrite('pic.png', frame)
            image = Image.open('pic.png')
            # Predict Action (7-DoF; un-normalize for BridgeData V2)
            inputs = processor(prompt, image).to("cuda:0", dtype=torch.bfloat16)
            action = vla.predict_action(**inputs, unnorm_key="bridge_orig", do_sample=False)
            currentPos  = panda.get_dofs_position(dofs_idx)
            qpos=panda.inverse_kinematics(
                link = end_effector,
                pos = np.array([currentPos[0]+action[0], currentPos[1]+action[1], currentPos[2]+action[2]]),
            )
            path = panda.plan_path(
                qpos_goal = qpos,
                num_waypoints = 20,
            )
            for waypoint in path:
                panda.control_dofs_position(waypoint)
                scene.step()

        cam2.start_recording()

cam1.stop_recording(save_to_filename='openvla/test.mp4')
# Execute...
# robot.act(action, ...)
# print(robot.act(action, ...))
#print(action)

