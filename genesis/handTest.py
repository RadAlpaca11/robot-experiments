import genesis as gs
import numpy as np

gs.init(backend=gs.cpu)

scene = gs.Scene(
    show_viewer    = True,
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (0, 0.0, 2),
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

cam = scene.add_camera(
    res = (640, 480),
    pos = (0, 0.0, 2),
    fov = 100,
    GUI = True,
)

scene.build()
if_dofs = np.arange(3)
mf_dofs = np.arange(3, 7)
rf_dofs = np.arange(7, 11)
th_dofs = np.arange(11, 15)

for i in range(1000):
    scene.step()
    # trying to move index finger
    if i==0:
        hand.control_dofs_force(
            np.array([10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            dofs_idx,
        )
        
        hand.control_dofs_position(
            np.array([1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]),
            dofs_idx,
        )