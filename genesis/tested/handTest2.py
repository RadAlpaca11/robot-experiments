import genesis as gs
import numpy as np

gs.init(backend=gs.cpu)

scene = gs.Scene(
    show_viewer    = True,
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (0, 0.0, 2),
        camera_lookat = (0.0, 0.0, 0.0),
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
    renderer = gs.renderers.Rasterizer(), # using rasterizer for camera rendering
)
plane = scene.add_entity(gs.morphs.Plane())

# Spawns palm-up
hand = scene.add_entity(
    gs.morphs.MJCF(file='genesis/mujoco_menagerie/leap_hand/right_hand.xml')
)
jnt_names = [
    'if_mcp',
    'if_rot',
    'if_pip',
    'if_dip',
    'mf_mcp',
    'mf_rot',
    'mf_pip',
    'mf_dip',
    'rf_mcp',
    'rf_rot',
    'rf_pip',
    'rf_dip',
    'th_cmc',
    'th_axl',
    'th_mcp',
    'th_ipl'
]
dofs_idx = [hand.get_joint(name).dof_idx_local for name in jnt_names]
dofs_idx_split = np.array_split(dofs_idx, 4)
# 0 is index, 1 is middle, 2 is ring, 3 is thumb

cam = scene.add_camera(
    res = (640, 480),
    pos = (1.5, -1.5, 1.0),
    lookat = (0, 0, 0),
    fov = 30,
    GUI = True,
)

scene.build()

# Taken from xml file
hand.set_dofs_kp(
    np.array([3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]),
)
hand.set_dofs_kv(
    np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]),
)

hand.set_dofs_force_range(
    np.array([-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5]),
    np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]),
)

cam.start_recording()

# Attempting to move each finger one at a time
for i in range(500):
    if i==25:
        hand.control_dofs_position(
            np.array([1.5, 0 , 0, 0]),
            dofs_idx_split[0],
        )
    if i==50:
        hand.control_dofs_position(
            np.array([1.5, 0 , 1.5, 0]),
            dofs_idx_split[0],
        )
    if i==75:
        hand.control_dofs_position(
            np.array([1.5, 0 , 1.5, 1.5]),
            dofs_idx_split[0],
        )
    if i==100:
        hand.control_dofs_position(
            np.array([0.65, 0 , 0.65, 0.65]),
            dofs_idx_split[0],
        )
    if i==125:
        hand.control_dofs_position(
            np.array([1.5, 0 , 0, 0]),
            dofs_idx_split[1],
        )
    if i==150:
        hand.control_dofs_position(
            np.array([1.5, 0 , 1.5, 0]),
            dofs_idx_split[1],
        )
    if i==175:
        hand.control_dofs_position(
            np.array([1.5, 0 , 1.5, 1.5]),
            dofs_idx_split[1],
        )
    if i==200:
        hand.control_dofs_position(
            np.array([0.65, 0 , 0.65, 0.65]),
            dofs_idx_split[1],
        )
    if i==225:
        hand.control_dofs_position(
            np.array([1.5, 0 , 0, 0]),
            dofs_idx_split[2],
        )
    if i==250:
        hand.control_dofs_position(
            np.array([1.5, 0 , 1.5, 0]),
            dofs_idx_split[2],
        )
    if i==275:
        hand.control_dofs_position(
            np.array([1.5, 0 , 1.5, 1.5]),
            dofs_idx_split[2],
        )
    if i==300:
        hand.control_dofs_position(
            np.array([0.65, 0 , 0.65, 0.65]),
            dofs_idx_split[2],
        )
    if i==325:
        hand.control_dofs_position(
            np.array([1.5, 0 , 0, 0]),
            dofs_idx_split[3],
        )
    if i==350:
        hand.control_dofs_position(
            np.array([1.5, 0 , 1.5, 0]),
            dofs_idx_split[3],
        )
    if i==375:
        hand.control_dofs_position(
            np.array([1.5, 0 , 1.5, 1.5]),
            dofs_idx_split[3],
        )
    if i==400:
        hand.control_dofs_position(
            np.array([0.65, 0 , 0.65, 0.65]),
            dofs_idx_split[3],
        )
    cam.render()
    scene.step()

cam.stop_recording(save_to_filename='genesis/picsAndVids/handTest2.mp4')