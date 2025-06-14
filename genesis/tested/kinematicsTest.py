import numpy as np
import genesis as gs

# init
gs.init(backend=gs.cpu)

# creating scene
scene = gs.Scene(
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
        world_frame_size = 1.0, # length of the world frame in meter
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
    gs.morphs.MJCF(file='genesis/mujoco_menagerie/franka_emika_panda/panda.xml',)
)

cube = scene.add_entity(
    gs.morphs.Box(
        size = (0.04, 0.04, 0.08),
        pos = (0.65, 0.0, 0.02),
    )
)

# jnt_names = [
#     'joint1',
#     'joint2',
#     'joint3',
#     'joint4',
#     'joint5',
#     'joint6',
#     'joint7',
#     'finger_joint1',
#     'finger_joint2',
# ]
# dofs_idx = [panda.get_joint(name).dof_idx_local for name in jnt_names]

cam = scene.add_camera(
    res = (640, 480),
    pos = (3.5, 0.0, 0.5),
    fov = 100,
    GUI = True,
)

scene.build()

gb, depth, segmentation, normal = cam.render(depth=True, segmentation=True, normal=True)

cam.start_recording()

motors_dof = np.arange(7)
fingers_dof = np.arange(7,9)

# these are tuned for the specific robot (panda)
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

# get the end-effector link
end_effector = panda.get_link('hand')
# move to pose before grasp
qpos = panda.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.0, 0.25]),
    quat = np.array([0, 1, 0, 0]),
)
# open gripper
qpos[-2:] = 0.04
path = panda.plan_path(
    qpos_goal = qpos,
    num_waypoints = 200 # 2s duration
)
# execute path
for waypoint in path:
    panda.control_dofs_position(waypoint)
    scene.step()

# let robot reach waypoint
for i in range(100):
    scene.step()

# reach
qpos = panda.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.0, 0.135]),
    quat = np.array([0, 1, 0, 0]),
)
panda.control_dofs_position(qpos[:-2], motors_dof)
panda.control_dofs_force(np.array([-0.5, -0.5]), fingers_dof)

for i in range(100):
    scene.step()

# lift
qpos = panda.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.0, 0.3]),
    quat = np.array([0, 1, 0, 0]),
)
panda.control_dofs_position(qpos[:-2], motors_dof)
for i in range(200):
    scene.step()
    cam.render()

cam.stop_recording(save_to_filename='picsAndVids/kinematics.mp4', fps=60)