import numpy as np
import genesis as gs

# doesn't currently work; sphere is not in range of panda2 long enough

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
# would it be simpler to use parallel simulation?
panda2 = scene.add_entity(
    gs.morphs.MJCF(
        file='genesis/mujoco_menagerie/franka_emika_panda/panda.xml',
        pos=(-5, 0, 0.2)
    )
)

# blocks don't roll very well
sphere = scene.add_entity(
    gs.morphs.Sphere(
        pos = (0, 0.61, 0.02),
        radius = (0.1)
    )
)

# testing a barrier
right_wall = scene.add_entity(
    gs.morphs.Box(
        pos = (-2.5, 0.85, 0.25),
        size = (5, 0.2, 0.5),
        collision = True,
        fixed = True,
    )
)

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
dofs2_idx = [panda2.get_joint(name).dof_idx_local for name in jnt_names]

cam = scene.add_camera(
    res = (640, 480),
    pos = (3.5, 0.0, 0.5),
    fov = 100,
    GUI = True,
)

scene.build()

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

panda2.set_dofs_kp(
    np.array([4500, 4500, 3500, 3500, 2000, 2000, 2000, 100, 100]),
)
panda2.set_dofs_kv(
    np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
)
panda2.set_dofs_force_range(
    np.array([-87, -87, -87, -87, -12, -12, -12, -100, -100]),
    np.array([87, 87, 87, 87, 12, 12, 12, 100, 100]),
)

# get the end-effector link
end_effector2 = panda2.get_link('hand')

# move to pose before grasp
qpos = panda.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.0, 0.2]),
    quat = np.array([1, 0, 0, 0]),
)
cam.start_recording
# plan path
qpos[-2:] = 0.04
path = panda.plan_path(
    qpos_goal = qpos,
    num_waypoints = 200 # 2s duration
)

panda2.control_dofs_position(
    np.array([0, 0, 0, -0.07, 0, 0, 0, 0, 0]),
    dofs2_idx,
)

# execute path
# does this need to be separate from the second loop?
for waypoint in path:
    panda.control_dofs_position(waypoint)
    scene.step()
    cam.render()

# qpos2 = panda2.inverse_kinematics(
#     link = end_effector2,
#     pos = np.array([-4.35, 0.0, 0.2]),
#     #quat = np.array([1, 0, 0, 0]),
# )

# # plan path
# qpos2[-2:] = 0.04
# path2 = panda2.plan_path(
#     qpos_goal = qpos2,
#     num_waypoints = 200 # 2s duration
# )
# for waypoint2 in path2:
#     panda2.control_dofs_position(waypoint2)
#     scene.step()
#     cam.render()

# # hand is now lowered



# let robot reach waypoint
for i in range(1000):
    scene.step()

    if i == 0:
        # first panda spins to hit sphere
        panda.control_dofs_velocity(
            #velocity lower than 5 moves over the block
            np.array([20, 0, 0, 0, 0, 0, 0, 0, 0])[:1],
            dofs_idx[:1],
        )
    cam.render()
    # not 100% sure i did this correctly
    # this is meant to figure out when the sphere passes the second panda at x-coordinate -5
    active_sphere_pos = sphere.get_pos()
    if active_sphere_pos[0] <= -4.75:
        #print("step:"+ i)
        #print("sphere_pos:" + active_sphere_pos)
        sphere_pos = sphere.get_pos()
        break

# when sphere is within range, second panda moves to hit sphere
qpos2 = panda2.inverse_kinematics(
    link = end_effector2,
    pos = np.array(sphere_pos),
    quat = np.array([0, 1, 0, 0]),
)
path2 = panda2.plan_path(
    qpos_goal = qpos2,
    num_waypoints = 200,
)
for waypoint in path2:
    panda2.control_dofs_position(waypoint)
    scene.step()
    cam.render()


for i in range(50):
    scene.step()
    cam.render()

cam.stop_recording(save_to_filename='picsAndVids/hitBlockTest.mp4', fps=60)