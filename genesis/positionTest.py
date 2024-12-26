# I don't know how much of this is needed to get the position of the feet
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
        show_world_frame = True,
        world_frame_size = 1.0,
        show_link_frame  = False,
        show_cameras     = False,
        plane_reflection = True,
        ambient_light    = (0.1, 0.1, 0.1),
    ),
    renderer = gs.renderers.Rasterizer(),
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
    pos = (3.5, 0.0, 0.5),
    fov = 100,
    GUI = True,
)
scene.build()

fl_dof = np.arange(3)
fr_dof = np.arange(3, 6)
hl_dof = np.arange(6, 9)
hr_dof = np.arange(9, 12)

fl_end_effector = spot.get_link('fl_foot')
fr_end_effector = spot.get_link('fr_foot')
hl_end_effector = spot.get_link('hl_foot')
hr_end_effector = spot.get_link('hr_foot')

# this should give the position of the feet at spawn
fl_pos = fl_end_effector.get_pos()
fr_pos = fr_end_effector.get_pos()
hl_pos = hl_end_effector.get_pos()
hr_pos = hr_end_effector.get_pos()

print('fl_pos:', fl_pos)
print('fr_pos:', fr_pos)
print('hl_pos:', hl_pos)
print('hr_pos:', hr_pos)

for i in range(1500):
    scene.step()