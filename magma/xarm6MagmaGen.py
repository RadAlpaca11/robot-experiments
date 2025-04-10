# import abc
import numpy as np
# import cv2
# from PIL import Image
# import torch
# from transformers import AutoModelForCausalLM, AutoProcessor
# # from xarm.wrapper import XArmAPI  # Import xarm-python-sdk
# import cv2
# import time
import genesis as gs

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
    gs.morphs.URDF(file='../models/ManiSkill-XArm6/xarm6_nogripper.urdf'),
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
# box2 = scene.add_entity(
#     gs.morphs.Box(
#         size=(0.05, 0.05, 0.05),
#         pos=(0.65, -0.3, 0.25),
#     ),
#     surface=gs.surfaces.Default(
#         color=(0, 0.6, 0.3),
#     )
# )


# for long video
camFilm = scene.add_camera(
    res    = (640, 480),
    pos    = (3.5, 0.0, 2.5),
    lookat = (0.65, 0, 0.25),
    fov    = 20,
    GUI    = True,
)
# for vla
cam = scene.add_camera(
    res    = (640, 480),
    pos    = (0.1, 0.2, 0.75),
    lookat = (0.65, 0.15, 0),
    fov    = 70,
    GUI    = True,
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
    np.array([0, 0, 0, 1, 1.25, 1.25]),
    dofs_idx,
)

for i in range(150):
    scene.step()

# starting position
qpos = xarm6.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.065, -0.02, 0.025]),
    quat = np.array([0, 1, 0, 0]),
)

xarm6.set_dofs_position(qpos[:6], motors_dof)

for i in range(150):
    scene.step()
    # camFilm.render()


# STARTING_STATE = [207.000366, 0.0, 112.002014]
# GOAL_STATE = [409.403961, -175.418945, 176.487289]
# RPY = [-180.00002, 0.0, -0.0] # hold static 
# points = np.linspace(STARTING_STATE, GOAL_STATE, num=100)

# class VLAModel(abc):
#     def __init__(self, model) -> None:
#         self.model = model

#     def __call__(self, image, text) -> np.ndarray:
#         """
#         Args:
#             image: The image to be processed.
#             text: The text prompt to be processed.
#         Returns:
#             action: The action to be taken.
#         """


# class Mock_VLAModel(VLAModel):
#     def __init__(self, starting_state, goal_state):
#         points = np.linspace(starting_state, goal_state, num=100)

#     def __call__(self, image, text):
#         # Mock function to simulate the VLAModel's behavior
#         # In a real scenario, this would be replaced with actual model inference
#         return np.random.rand(6)  # Random action for demonstration

# def mock_magma():
#     # Mock function to simulate the Magma model's behavior
#     # In a real scenario, this would be replaced with actual model inference
#     return np.random.rand(6)  # Random action for demonstration


# dtype = torch.bfloat16
# model = AutoModelForCausalLM.from_pretrained("microsoft/Magma-8B", trust_remote_code=True, torch_dtype=dtype)
# processor = AutoProcessor.from_pretrained("microsoft/Magma-8B", trust_remote_code=True)
# model.to("cuda")

# # Replace '192.168.1.100' with your xArm6 IP address.
# # arm = XArmAPI('172.20.5.100')

# # Initialize the robot.
# def initialize_robot(arm):
#     arm.clean_warn()
#     arm.clean_error()
#     arm.motion_enable(True)
#     arm.set_mode(0)
#     arm.set_state(0)
#     arm.move_gohome()

# # initialize_robot(arm)


# # cap = cv2.VideoCapture("https://robotcopilotstream.smtoctolabs.com/mjpg/video.mjpg?videocodec=h264&resolution=320x240")

# # Define the conversation prompt
# convs = [
#     {"role": "system", "content": "You are an agent that can see, talk, and act."},
#     # {"role": "user", "content": "<image_start><image><image_end>\n What action should I take to move the robot to touch the soda can? Based on the initial position of the robot and the image provided the goal was original at position: [409.403961, -175.418945, 176.487289, 179.982144, -3.053521, -23.123889]"},
#     {"role": "user", "content": "<image_start><image><image_end>\n What action should I take to move the robot to touch the soda can?"},
#     # {"role": "user", "content": "<image_start><image><image_end>\n What position is the end effector at?"},
# ]

# i = 0
# while True:
#     print(f"Iteration: {i + 1}")
    
#     ret, frame = cap.read()

#     if not ret:
#         print("Error: Could not read frame.")
#         break

#     # Display the resulting frame
#     # cv2.imshow('MJPG Stream', frame)
#     # Press 'q' to exit the video stream
#     # if cv2.waitKey(1) & 0xFF == ord('q'):
#     #     break
    
#     image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#     # Prepare inputs
#     prompt = processor.tokenizer.apply_chat_template(convs, tokenize=False, add_generation_prompt=True)
#     inputs = processor(images=[image], texts=prompt, return_tensors="pt")
#     inputs["pixel_values"] = inputs["pixel_values"].unsqueeze(0)
#     inputs["image_sizes"] = inputs["image_sizes"].unsqueeze(0)
#     inputs = inputs.to("cuda").to(dtype)
    
#     generation_args = {
#         "max_new_tokens": 500,
#         "temperature": 0.0,
#         "do_sample": False,
#         "use_cache": True,
#         "num_beams": 1,
#     }
    
#     with torch.inference_mode():
#         generate_ids = model.generate(**inputs, **generation_args)
    
#     # Get the last action and convert it to discretized action values.
#     generate_ids = generate_ids[0, -8:-1].cpu().tolist()
#     predicted_action_ids = np.array(generate_ids).astype(np.int64)
#     discretized_actions = processor.tokenizer.vocab_size - predicted_action_ids
#     normalized_actions = discretized_actions / 100 # Normalize the actions
#     normalized_actions[-3:] = 0 # Set the last three values to zero (not used in this example)

#     # Use the first six normalized values as joint angles.
#     delta_next_pose = normalized_actions[:6].tolist()

#     error, current_position = arm.get_position()
#     if error != 0:
#         print("Error getting current position:", error)
#         arm.motion_enable(False)
#         initialize_robot(arm)
#         break
    
#     euclidean_distance = np.linalg.norm(np.array(current_position[:3]) - np.array(GOAL_STATE))
#     print("Euclidean distance to goal:", euclidean_distance)
#     if euclidean_distance < 10:
#         print("Goal reached within 1cm. Stopping loop.")
#         break

#     # Uncomment the following lines to see the delta_next_pose and current_position
#     magma_new_position = [curr + delta for curr, delta in zip(current_position, delta_next_pose)]
#     print("delta_next_pose:", delta_next_pose)
#     print("Current Position:", current_position)
#     print("Magma New Position:", magma_new_position)
#     print("Delta Current and New Position:", np.array(magma_new_position) - np.array(current_position))
#     # error = arm.set_position(*new_position, wait=True)
    
#     # error = arm.set_position(409.403961, -175.418945, 176.487289, 179.982144, -3.053521, -23.123889)
#     # next_position = np.append(points[i], RPY)
#     # next_position = np.append(magma_new_position[0:3], RPY)
#     # print("Linear Next Position:", next_position)
#     # error = arm.set_position(*next_position)
#     # if error != 0:
#     #     print("Error setting position:", error)
#     #     arm.motion_enable(False)
#     #     initialize_robot(arm)
#     #     break
#     # time.sleep(0.05)
    
#     # i += 1

# cap.release()
# cv2.destroyAllWindows()