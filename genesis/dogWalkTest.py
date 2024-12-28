# UNFINISHED
# Once this code is finished the hope is that this will make the spot walk
import genesis as gs
import numpy as np

gs.init(backend=gs.cpu)

scene = gs.Scene(
    show_viewer    = True,
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (3.5, 0.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 40,
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
    renderer = gs.renderers.Rasterizer(), # using rasterizer for camera rendering
)
plane = scene.add_entity(gs.morphs.Plane())
spot = scene.add_entity(
    gs.morphs.MJCF(file='genesis/mujoco_menagerie/boston_dynamics_spot/spot.xml',)
)
# seems like fl, is front left, fr is front right, hl is hind left, and hr is hind right
# hx is hip x, hy is hip y, and kn is knee
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
    GUI = True,
)

scene.build()

fl_dof = np.arange(3)
fr_dof = np.arange(3, 6)
hl_dof = np.arange(6, 9)
hr_dof = np.arange(9, 12)

fl_end_effector = spot.get_link('fl_lleg')
fr_end_effector = spot.get_link('fr_lleg')
hl_end_effector = spot.get_link('hl_lleg')
hr_end_effector = spot.get_link('hr_lleg')

gb, depth, segmentation, normal = cam.render(depth=True, segmentation=True, normal=True)

cam.start_recording()

fl_qpos = spot.inverse_kinematics(
    link = fl_end_effector,
    pos = np.array([1, 0, 1]),
)

fl_qpos[-2:] = 0.04
path = spot.plan_path(
    qpos_goal = fl_qpos,
    num_waypoints = 200
)
for waypoint in path:
    spot.control_dofs_position(waypoint)
    scene.step()
    cam.render()

for i in range(100):
    scene.step()
    cam.render()
# add movement code here
# could pick values
# if the positionTest code works, we can add it to this code and then add or subtract to the starting positions

cam.stop_recording(save_to_filename='picsAndVids/dogWalkTest.mp4', fps=60)