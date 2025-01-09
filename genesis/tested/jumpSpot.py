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
    'hr_kn'
]
dofs_idx = [spot.get_joint(name).dof_idx_local for name in jnt_names]
dofs_idx_split = np.array_split(dofs_idx, 4)
# 0 is front left, 1 is front right, 2 is hind left, 3 is hind right

cam = scene.add_camera(
    res = (640, 480),
    pos = (0, 2, 0.5),
    fov = 100,
    GUI = True,
)

scene.build()

# Taken directly from xml file
spot.set_dofs_kp(
    np.array([500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]),
    dofs_idx,
)
spot.set_dofs_kv(
    np.array([40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]),
    dofs_idx,
)

spot.set_dofs_force_range(
    np.array([-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100]),
    np.array([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]),
    dofs_idx,
)

cam.start_recording()

for i in range(250):
    if i==0:
        # crouching
        spot.control_dofs_position(
            np.array([0, 1, -2.25, 0, 1, -2.25, 0, 1, -2.25, 0, 1, -2.25]),
            dofs_idx,
        )
    if i==100:
        # extending back legs first; spot tends to do backflips
        spot.control_dofs_position(
            np.array([0, 1, -2.25, 0, 1, -2.25, 0, 0, -0.25, 0, 0, -0.25]),
            dofs_idx
        )
    if i==125:
        # extending front legs
        spot.control_dofs_position(
            np.array([0, 1.15, -0.5, 0, 1.15, -0.5, 0, 0, -0.25, 0, 0, -0.25]),
            dofs_idx,
        )
    if i==132:
        # drawing legs in for more airtime
        spot.control_dofs_position(
            np.array([0, 1, -2.25, 0, 1, -2.25, 0, 1, -2.25, 0, 1, -2.25]),
            dofs_idx,
        )
    cam.render()
    scene.step()

cam.stop_recording(save_to_filename='genesis/picsAndVids/jump.mp4')