# I don't know how much of this is needed to get the position of the feet
import genesis as gs
import numpy as np

gs.init(backend=gs.cpu)

scene = gs.Scene(
    show_viewer    = True,
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (0, 3, 0.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 40,
        max_FPS       = 60,
    ),
    vis_options = gs.options.VisOptions(
        show_world_frame = True,
        world_frame_size = 1.0,
        show_link_frame  = False,
        show_cameras     = False,
        plane_reflection = True,
        ambient_light    = (0.1, 0.1, 0.1),
    ),
    renderer = gs.renderers.Rasterizer(),
    rigid_options = gs.options.RigidOptions(
        dt = 0.01,
    ),
)

# this doesn't seem to do anything
gs.options.SimOptions(
    gravity = (0.0, 0.0, 0.0),
)

plane = scene.add_entity(gs.morphs.Plane())
spot = scene.add_entity(
    gs.morphs.MJCF(file='genesis/mujoco_menagerie/boston_dynamics_spot/spot.xml',)
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
    pos = (0, 3, 0.5),
    fov = 100,
    GUI = True,
)
scene.build()
fl_dof = np.arange(3)
fr_dof = np.arange(3, 6)
hl_dof = np.arange(6, 9)
hr_dof = np.arange(9, 12)

#rgb, depth, segmentation, normal = cam.render(depth = True, segmentation=True, normal=True)

pos_idx = spot.get_dofs_position(dofs_idx_local = dofs_idx)


#fl_pos = spot.get_pos(spot.get_body('fl_lleg'))
# fr_pos = spot.get_pos('fr_lleg')
# hl_pos = spot.get_pos('hl_lleg')
# hr_pos = spot.get_pos('hr_lleg')

print(pos_idx)
# print("fr_pos:" + fr_pos)
# print("hl_pos:" + hl_pos)
# print("hr_pos:" + hr_pos)

cam.start_recording()


# in other files, we've put the control_dofs_position and control_dofs_force in an if statement that only runs once
for i in range(1000):
    # zeroing velocity makes the robot fall down slower at a consistent rate
    # might be reseting the velocity to 0 every step, so it only has one step to accelerate
    # spot.zero_all_dofs_velocity()
    spot.control_dofs_force(
            # 1000 seems to be the max force for spot
            np.array([1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]),
            dofs_idx,
        )
    # spot moved, but didn't support its own weight
    spot.control_dofs_position(
            np.array([0.29785, 0.055, -1, 0.29785, -0.055, -1, -0.29785, 0.055, -1, -0.29785, -0.055, -1]),
            dofs_idx,
        )
    cam.render()
    scene.step()
    if i==999:
        print(pos_idx)

cam.stop_recording(save_to_filename='genesis/picsAndVids/noGrav2.mp4', fps=60)