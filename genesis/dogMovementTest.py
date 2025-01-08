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
    gs.morphs.MJCF(file='genesis/mujoco_menagerie/boston_dynamics_spot/spot_arm.xml',)
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
dofs_idx_split = np.array_split(dofs_idx, 3)
# 0 is front left, 1 is front right, 2 is hind left, 3 is hind right

arm_jnts = [
    'arm_sh0',
    'arm_sh1',
    'arm_el0',
    'arm_el1',
    'arm_wr0',
    'arm_wr1',
    'arm_f1x'
]
arm_idx = [spot.get_joint(name).dof_idx_local for name in arm_jnts]

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
    np.array([-75, -75, -75, -75, -75, -75, -75, -75, -75, -75, -75, -75]),
    np.array([75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75]),
    dofs_idx,
)

spot.set_dofs_force_range(
    np.array([-100, -100, -100, -100, -100, -100, -100]),
    np.array([100, 100, 100, 100, 100, 100, 100]),
    arm_idx,
)

spot.control_dofs_position(
    np.array([0, -3.14, 3.14, 0, 0, 0, 0]),
    arm_idx,
)

cam.start_recording()
x=0
for i in range(750):
    # standing up
    if x==1:
        spot.control_dofs_position(
            np.array([0.15, 0.5,-1, -0.15, 0.5, -1, 0.15, 0.5, -1, -0.15, 0.5, -1]),
            dofs_idx,
        )
    # raising fl and hr legs
    if x>=100:
        spot.control_dofs_position(
            np.array([0, 1, -2]),
            dofs_idx[:3],
        )
        spot.control_dofs_position(
            np.array([0, 1, -2]),
            dofs_idx[9:],
        )
    #fl and hr legs forward
    if x>=110:
        spot.control_dofs_position(
            np.array([0.15, 0.45, -1.2]),
            dofs_idx[:3],
        )
        spot.control_dofs_position(
            np.array([-0.15, 0.45, -1.2]),
            dofs_idx[9:],
        )
    
    # it wasn't working earlier because this was missing
    # raising fr and hl legs
    if x>=120:
        spot.control_dofs_position(
            np.array([0, 1, -2]),
            dofs_idx[:3],
        )
        spot.control_dofs_position(
            np.array([0, 1, -2]),
            dofs_idx[9:],
        )
    #fr and hl legs forward
    if x>=130:
        spot.control_dofs_position(
            np.array([-0.15, 0.45, -1.2]),
            dofs_idx[3:6],
        )
        spot.control_dofs_position(
            np.array([0.15, 0.45, -1.2]),
            dofs_idx[6:9],
        )
    if x==150:
        x=0
    x+=1
    cam.render()
    scene.step()

cam.stop_recording(save_to_filename='genesis/picsAndVids/spotMovement.mp4')