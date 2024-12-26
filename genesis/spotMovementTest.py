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
    show_viewer = True,
)
plane = scene.add_entity(gs.morphs.Plane())

spot = scene.add_entity(gs.morphs.MJCF(file='mujoco_menagerie/boston_dynamics_spot/spot.xml',
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
# PD control
for i in range(1500):
    if i == 0:
      # testing what 0 position is
      # 0 isn't in knee range, so probably change this
        spot.control_dofs_position(
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            dofs_idx,
        )
    elif i == 250:
      # moving knees with floppy hips
        spot.control_dofs_position(
            np.array([0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1]),
            dofs_idx,
        )
      # no clue what normal force values are, may need to change from 1
        spot.control_dofs_force(
            np.array([0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]), # making hips floppy so that knees can move
            dofs_idx,
    elif i == 500:
      # setting force to 1
        spot.control_dofs_force(
            np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            dofs_idx,
        )
    elif i == 750:
      # moving stuff
      spot.control_dofs_position(
            np.array([0.75, 2, -2, 0.75, 2, -2, 0.75, 2, -2, 0.75, 2, -2]),
            dofs_idx,
        )
    elif i == 1000:
      # setting positions to roughly middle of range
        spot.control_dofs_position(
            np.array([0, 0.5, -1, 0, 0.5, -1, 0, 0.5, -1, 0, 0.5, -1]),
            dofs_idx,
        )
    elif i == 1250:
      # going floppy again
        spot.control_dofs_force(
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            dofs_idx,
        )

    scene.step()
    cam.render()

cam.stop_recording(save_to_filename='genesis/picsAndVids/video1.mp4', fps=60)
