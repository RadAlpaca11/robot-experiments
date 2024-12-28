import numpy as np
import genesis as gs
gs.init(backend=gs.cpu)
scene = gs.Scene(
    viewer_options = gs.options.ViewerOptions(
        camera_pos    = (3, -1, 1.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        max_FPS       = 60,
    ),
    sim_options = gs.options.SimOptions(
        dt = 0.01,
        substeps = 4,
    ),
    show_viewer = True,
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)

spot = scene.add_entity(gs.morphs.MJCF(file='genesis/mujoco_menagerie/boston_dynamics_spot/spot.xml',
    pos = (0, 0, 0),)
)
jnt_names = [
    'fl_hx',
    'fl_hy',
    'fl_kn',
    'fr_hx',
    'fr_hy',
    'fr_kn',
    'hl_hx',
    'hl_hy',
    'hl_kn',
    'hr_hx',
    'hr_hy',
    'hr_kn',
]
dofs_idx = [spot.get_joint(name).dof_idx_local for name in jnt_names]

cam = scene.add_camera(
    res = (640, 480),
    pos = (3.5, 0.0, 0.5),
    fov = 100,
    GUI = False,
)

scene.build()
cam.start_recording()
import numpy as np

#values need to be tuned (note from hayden: they might be tuned in the xml file?)
spot.set_dofs_kp(
    np.array([20, 20, 15, 20, 20, 15, 20, 20, 15, 20, 20, 15]),
)
spot.set_dofs_kv(
    np.array([50, 50, 40, 50, 50, 40, 50, 50, 40, 50, 50, 40]),
)
spot.dofs_force_range(
    np.array([-15, -15, -10, -15, -15, -10, -15, -15, -10, -15, -15, -10]),
    np.array([150, 15, 10, 15, 15, 10, 15, 15, 10, 15, 15, 10]),
)

# foot is a geometry rather than a body
# using lower leg instead
end_effector = spot.get_link('fl_lleg')

# everything past this point is unfinished

# i don't understand coordinates
qpos = spot.inverse_kinematics(
    link = end_effector,
    pos  = np.array([0.65, 0.055, 0.02]),
    quat = np.array([0, 1, 0, 0]),
)
# something important i think
qpos[-2:] = 0.04
path = spot.plan_path(
    qpos_goal     = qpos,
    num_waypoints = 200, # 2s duration
)
# execute the planned path
for waypoint in path:
    spot.control_dofs_position(waypoint)
    scene.step()

# allow robot to reach the last waypoint
for i in range(100):
    scene.step()
