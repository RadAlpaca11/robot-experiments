# import abc
import numpy as np
import cv2
from PIL import Image
import torch
from transformers import AutoModelForCausalLM, AutoProcessor
from xarm.wrapper import XArmAPI  # Import xarm-python-sdk
import genesis as gs
from scipy.spatial.transform import Rotation

def quatToEuler(q, scalarFirst=True, order='xyz', degrees=False):
    if scalarFirst:
        q = [q[1], q[2], q[3], q[0]]
    r = Rotation.from_quat(q)
    return r.as_euler(order, degrees=degrees)

# Initialize magma
dtype = torch.bfloat16
model = AutoModelForCausalLM.from_pretrained("microsoft/Magma-8B", trust_remote_code=True, torch_dtype=dtype)
processor = AutoProcessor.from_pretrained("microsoft/Magma-8B", trust_remote_code=True)
model.to("cuda")

convs = [
    {"role": "system", "content": "You are an agent that can see, talk, and act."},
    {"role": "user", "content": "<image_start><image><image_end>\n What action should I take to move the robot to touch the yellow block?"},
]

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
    renderer=gs.renderers.Rasterizer(),
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
xarm6 = scene.add_entity(
    gs.morphs.URDF(file='../models/ManiSkill-XArm6/mod_xarm6_nogripper.urdf'),
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

print(end_effector.get_pos())
print(xarm6.get_dofs_position())

xarm6.control_dofs_position(
    np.array([0, 0, -2, 0, 0, 0]),
    dofs_idx,
)


camFilm.start_recording()

for i in range(100):
    scene.step()

# print('joints done')

for i in range(25):

    for i in range(25):
        scene.step()
        camFilm.render()
    output = cam.render()
    imageData = output[0]
    image = cv2.cvtColor(imageData, cv2.COLOR_BGR2RGB)

    # magma setup
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

    # robot information

    currentPos = end_effector.get_pos()
    print(currentPos)
    currentQuat = end_effector.get_quat()
    currentEuler = quatToEuler(currentQuat)
    simPosition = [currentPos[0], currentPos[1], currentPos[2], currentEuler[0], currentEuler[1], currentEuler[2]]
    print(simPosition)

    simTarget = np.array([currentPos[0] + (discretized_actions[0] / 100), currentPos[1] + (discretized_actions[1] / 100), currentPos[2] + (discretized_actions[2] / 100), currentEuler[0]+(discretized_actions[3]/100), currentEuler[1]+(discretized_actions[4]/100), currentEuler[2]+(discretized_actions[5]/100)])
    print(simTarget)
    ik = remoteArm.get_inverse_kinematics(simTarget, input_is_radian=True, return_is_radian=True)
    print(ik)
    xarm6.control_dofs_position(
        ik[1][:6],
        dofs_idx
    )


camFilm.stop_recording(save_to_filename='video.mp4')