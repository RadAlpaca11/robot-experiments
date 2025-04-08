#genesis stuff

import genesis as gs
import numpy as np
import cv2

from PIL import Image
import torch
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor

dtype = torch.bfloat16
model = AutoModelForCausalLM.from_pretrained("microsoft/Magma-8B", trust_remote_code=True, torch_dtype=dtype)
processor = AutoProcessor.from_pretrained("microsoft/Magma-8B", trust_remote_code=True)
model.to("cuda")

# Initializing magma
convs = [
    {"role": "system", "content": "You are an agent that can see, talk, and act."},
    {"role": "user", "content": "<image_start><image><image_end>\n What action should I take to move the robot to touch the yellow block?"},
]


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
kuka = scene.add_entity(
    gs.morphs.MJCF(file='../genesis/mujoco_menagerie/kuka_iiwa_14/iiwa14.xml'),
)
box1 = scene.add_entity(
    gs.morphs.Box(
        size=(0.05, 0.05, 0.05),
        pos=(0.65, 0.3, 0.25),
    ),
    surface=gs.surfaces.Default(
        color=(1, 0.8, 0),
    )
)
box2 = scene.add_entity(
    gs.morphs.Box(
        size=(0.05, 0.05, 0.05),
        pos=(0.65, -0.3, 0.25),
    ),
    surface=gs.surfaces.Default(
        color=(0, 0.6, 0.3),
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
    pos    = (0.1, 0.2, 0.75),
    lookat = (0.65, 0.15, 0),
    fov    = 70,
    GUI    = True,
)



scene.build()
camFilm.start_recording()

motors_dof = np.arange(7)


kuka.set_dofs_kp(
    np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000]),
)
kuka.set_dofs_kv(
    np.array([450, 450, 350, 350, 200, 200, 200]),
)
kuka.set_dofs_force_range(
    np.array([-87, -87, -87, -87, -12, -12, -12]),
    np.array([87, 87, 87, 87, 12, 12, 12]),
)

# get the end-effector link
end_effector = kuka.get_link('link7')

import time

# starting position
qpos = kuka.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, -0.2, 0.25]),
    quat = np.array([0, 1, 0, 0]),
)

kuka.control_dofs_position(qpos, motors_dof)

for i in range(150):
    scene.step()
    camFilm.render()

# ret = False

# while ret == False:
#     cam.start_recording()
#     for i in range(25):
#         scene.step()
#         cam.render()
#         camFilm.render()
#     cam.stop_recording(save_to_filename='clip.mp4')

#     currentPos = end_effector.get_pos()
#     print(currentPos)
#     video = cv2.VideoCapture('clip.mp4')
#     video.set(cv2.CAP_PROP_POS_FRAMES, 23)
#     ret, frame = video.read()
#     print(ret)

# cv2.imwrite('frame.jpg', frame)
# image = Image.open('frame.jpg')

# prompt = processor.tokenizer.apply_chat_template(convs, tokenize=False, add_generation_prompt=True)
# inputs = processor(images=[image], texts=prompt, return_tensors="pt")
# inputs['pixel_values'] = inputs['pixel_values'].unsqueeze(0)
# inputs['image_sizes'] = inputs['image_sizes'].unsqueeze(0)
# inputs = inputs.to("cuda").to(dtype)
# generation_args = {
#     "max_new_tokens": 500,
#     "temperature": 0.0,
#     "do_sample": False,
#     "use_cache": True,
#     "num_beams": 1,
# }
# with torch.inference_mode():
#     generate_ids = model.generate(**inputs, **generation_args)
# # get the last action, and convert the action (as token) to a discretized action
# generate_ids = generate_ids[0, -8:-1].cpu().tolist()
# predicted_action_ids = np.array(generate_ids).astype(np.int64)
# discretized_actions = processor.tokenizer.vocab_size - predicted_action_ids
# print(discretized_actions)
# qpos= kuka.inverse_kinematics(
#     link = end_effector,
#     pos = np.array([currentPos[0]+(discretized_actions[0]/1000), currentPos[1]+(discretized_actions[1]/1000), currentPos[2]+(discretized_actions[2]/1000)]),
# )
# kuka.control_dofs_position(qpos, motors_dof)
# for i in range(150):
#     scene.step()
#     cam.render()
#     camFilm.render()



for i in range(75):
    cam.start_recording()
    for i in range(25):
        scene.step()
        cam.render()
        camFilm.render()

    cam.stop_recording(save_to_filename='clip.mp4')

    currentPos = end_effector.get_pos()
    print(currentPos)

    video = cv2.VideoCapture('clip.mp4')
    video.set(cv2.CAP_PROP_POS_FRAMES, 23)
    ret, frame = video.read()
    print(ret)
    cv2.imwrite('frame.jpg', frame)
    image = Image.open('frame.jpg')

    prompt = processor.tokenizer.apply_chat_template(convs, tokenize=False, add_generation_prompt=True)
    inputs = processor(images=[image], texts=prompt, return_tensors="pt")
    inputs['pixel_values'] = inputs['pixel_values'].unsqueeze(0)
    inputs['image_sizes'] = inputs['image_sizes'].unsqueeze(0)
    inputs = inputs.to("cuda").to(dtype)

    generation_args = {
        "max_new_tokens": 500,
        "temperature": 0.0,
        "do_sample": False,
        "use_cache": True,
        "num_beams": 1,
    }

    with torch.inference_mode():
        generate_ids = model.generate(**inputs, **generation_args)
    
    # get the last action, and convert the action (as token) to a discretized action
    generate_ids = generate_ids[0, -8:-1].cpu().tolist()
    predicted_action_ids = np.array(generate_ids).astype(np.int64)
    discretized_actions = processor.tokenizer.vocab_size - predicted_action_ids
    print(discretized_actions)

    qpos= kuka.inverse_kinematics(
        link = end_effector,
        pos = np.array([currentPos[0]+(discretized_actions[0]/10000), currentPos[1]+(discretized_actions[1]/10000), currentPos[2]+(discretized_actions[2]/10000)]),
    )
    print(np.array([currentPos[0]+(discretized_actions[0]/10000), currentPos[1]+(discretized_actions[1]/10000), currentPos[2]+(discretized_actions[2]/10000)]))

    kuka.control_dofs_position(qpos, motors_dof)


camFilm.stop_recording(save_to_filename='picsAndVids/test10.mp4')
# Execute...
# robot.act(action, ...)
# print(robot.act(action, ...))
#print(action)