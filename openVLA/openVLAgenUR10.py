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
    gs.morphs.URDF(file='../ur_description/ur10_robot.urdf'),
)
box = scene.add_entity(
    gs.morphs.Box(
        size=(0.05, 0.1, 0.1),
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
    pos    = (0.75, -1.5, 1),
    lookat = (0.75, 0.5, 0),
    fov    = 20,
    GUI    = True,
)



scene.build()
camFilm.start_recording()

dofs_idx = np.array([0, 1, 2, 3, 4, 5])


kp = np.array([4500, 4500, 3500, 3500, 2000, 2000])
if len(kp) != len(dofs_idx):
    print(len(kp))
    print(len(dofs_idx))
    raise ValueError("Length of kp does not match length of motors_dof")

if kp.ndim != 1:
    raise ValueError("kp must be a 1D array")

if dofs_idx.ndim != 1:
    raise ValueError("dofs_idx must be a 1D array")



ur10.set_dofs_kp(
    np.array([4500, 4500, 3500, 3500, 2000, 2000]),
)
ur10.set_dofs_kv(
    np.array([450, 450, 350, 350, 200, 200]),
)
ur10.set_dofs_force_range(
    np.array([-87, -87, -87, -87, -12, -12]),
    np.array([87, 87, 87, 87, 12, 12]),
)

# get the end-effector link
end_effector = ur10.get_link('wrist_3_link')

import time

# starting position
qpos = ur10.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.5, 0.25]),
    quat = np.array([0, 1, 0, 0]),
)

ur10.control_dofs_position(qpos[:6], motors_dof)

for i in range(500):
    scene.step()
    camFilm.render()

# currentPos = end_effector.get_pos()
# print("currentPos:"+currentPos)    
# for i in range(150):
#     scene.step()
#     cam1.render()
#     cam2.render()
#     if(i%10 == 0):
#         cam2.render()
#         cam2.stop_recording(save_to_filename='openVLA/references/clip.mp4')
#         currentPos = end_effector.get_pos()
#         print(currentPos)

#         something = np.array([0.65, 0.0, 0.25])
#         print(currentPos[0])
#         print(currentPos[0]+something[0])
#         currentQuat = end_effector.get_quat()
#         video = cv2.VideoCapture('openVLA/references/clip.mp4')
#         video.set(cv2.CAP_PROP_POS_FRAMES, 8)
#         ret, frame = video.read()
#         if ret:
#             cv2.imwrite('openVLA/references/pic.png', frame)
#             image = Image.open('pic.png')
#             # Predict Action (7-DoF; un-normalize for BridgeData V2)
#             inputs = processor(prompt, image).to("cuda:0", dtype=torch.bfloat16)
#             action = vla.predict_action(**inputs, unnorm_key="bridge_orig", do_sample=False)

        
#             currentPos  = ur10.get_dofs_position(dofs_idx)
#             qpos=ur10.inverse_kinematics(
#                 link = end_effector,
#                 pos = np.array([0.65,0.0, 0.135])
#                 # pos = np.array([currentPos[0]+action[0], currentPos[1]+action[1], currentPos[2]+action[2]]),
#                 # quat = np.array([currentQuat[0]+action[3], currentQuat[1]+action[4], currentQuat[2]+action[5]]),
#                 #init_qpos = currentPos,
#             )
#             print (qpos)
#             print(np.array([currentPos[0]+action[0], currentPos[1]+action[1], currentPos[2]+action[2]]))
#             ur10.control_dofs_position(qpos[:-2], motors_dof)
#             print(action)
#             # path = ur10.plan_path(
#             #     qpos_goal = qpos,
#             #     qpos_start = currentPos,
#             #     num_waypoints = 20,
#             # )

#             print("path")
#             for i in range(200):
#                 scene.step()
#                 cam1.render()
#             # for waypoint in path:
#             #     print("waypoint")
#             #     ur10.control_dofs_position(waypoint)
#             #     scene.step()
#         print("restarting recording")
#         cam2.start_recording()

for i in range(100):
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

    ur10.control_dofs_position(qpos[:6], motors_dof)


camFilm.stop_recording(save_to_filename='picsAndVids/u10Test.mp4')
# Execute...
# robot.act(action, ...)
# print(robot.act(action, ...))
#print(action)

