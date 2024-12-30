# incomplete
# this is going to pick up a block like in kinematicsTest, and then hopefully move using the wheels

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
robot = scene.add_entity(gs.morphs.MJCF(file='genesis/mujoco_menagerie/google_robot/robot.xml',))

cube = scene.add_entity(
    gs.morphs.Box(
        size = (0.04, 0.04, 0.08),
        pos = (0.65, 0.0, 0.02),
    )
)

cam = scene.add_camera(
    res = (640, 480),
    pos = (3.5, 0.0, 0.5),
    fov = 60,
    GUI = False,
)

scene.build()
cam.start_recording()

# this was in kinematicsTest, and this robot has the same number of dofs
motors_dof = np.arange(7)
fingers_dof = np.arange(7,9)

robot.set_dofs_kp(
    np.array([40, 40, 40, 20, 20, 10, 10, 20, 20])
)
robot.set_dofs_kv(
    # copilot autocompleted these values
    # the xml file has kp but not kv
    np.array([10, 10, 10, 5, 5, 2, 2, 5, 5])
)
robot.set_dofs_force_range(
    np.array([-150, -150, -30, -30, -30, -30, -30, -30, -30]),
    np.array([150, 150, 30, 30, 30, 30, 30, 30, 30])
)
end_effector = robot.get_link('link_gripper')

qpos = robot.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.0, 0.25]),
    quat = np.array([0, 1, 0, ])
)

qpos[-2:] = 0.04
path = robot.plan_path(
    qpos_goal = qpos,
    num_waypoints = 200
)
for waypoint in path:
    robot.control_dofs_position(waypoint)
    scene.step()
    cam.render()

for i in range(100):
    scene.step()
    cam.render()

qpos = robot.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.0, 0.135]),
    quat = np.array([0, 1, 0, 0]),
)

robot.control_dofs_position(qpos[:-2], motors_dof)
robot.control_dofs_force(np.array([-0.5, -0.5]), fingers_dof)

for i in range(100):
    scene.step()
    cam.render()

qpos = robot.inverse_kinematics(
    link = end_effector,
    pos = np.array([0.65, 0.0, 0.3]),
    quat = np.array([0, 1, 0, 0]),
)
robot.control_dofs_position(qpos[:-2], motors_dof)
for i in range(200):
    scene.step()
    cam.render()

