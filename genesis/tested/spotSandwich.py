import genesis as gs

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
    gs.morphs.MJCF(file='mujoco_menagerie/boston_dynamics_spot/spot.xml',
    pos = (0, 0, 10),)
)
spot2 = scene.add_entity(
    gs.morphs.MJCF(file='mujoco_menagerie/boston_dynamics_spot/spot.xml',
    pos = (0, 0, 3),)
)
spot3 = scene.add_entity(
    gs.morphs.MJCF(file='mujoco_menagerie/boston_dynamics_spot/spot.xml',
    pos = (0, 0, 5),)
)
# spot4 starts off in the ground because z=0
# it will be flung into the air when the scene starts
spot4 = scene.add_entity(
    gs.morphs.MJCF(file='mujoco_menagerie/boston_dynamics_spot/spot.xml',
    pos = (0, 0, 0),)
)

sphere=scene.add_entity(gs.morphs.Sphere(
    pos = (0, 0, 2),
))
sphere2=scene.add_entity(gs.morphs.Sphere(
    pos = (0, 0, 4),
))
sphere3=scene.add_entity(gs.morphs.Sphere(
    pos = (0, 0, 6),
))

cam = scene.add_camera(
    res = (640, 480),
    pos = (3.5, 0.0, 0.5),
    fov = 100,
    GUI = True,
)

scene.build()

gb, depth, segmentation, normal = cam.render(depth=True, segmentation=True, normal=True)

cam.start_recording()
import numpy as np

for i in range(1000):
    scene.step()
    # camera rotates around origin of the plane
    cam.set_pose(
        pos = (3.0 * np.sin(i/60), 3.0 * np.cos(i/60), 2.5),
        lookat = (0, 0, 0.5),
    )
    cam.render()
cam.stop_recording(save_to_filename='genesis/picsAndVids/spotSandwich.mp4', fps=60)