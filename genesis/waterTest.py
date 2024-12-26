import numpy as np
import genesis as gs

# init
gs.init(backend=gs.cpu)

# creating scene
scene = gs.Scene(
    show_viewer    = True,
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (4, 0.0, 3),
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
    sph_options=gs.options.SPHOptions(
        lower_bound = (-0.5, -0.5, 0),
        upper_bound = (0.5, 0.5, 1),
        particle_size = 0.01,
    ),
    
    sim_options = gs.options.SimOptions(
        dt = 4e-3,
        substeps = 10,
    ),
    renderer = gs.renderers.Rasterizer(), # using rasterizer for camera rendering
    show_viewer = True,
)
plane = scene.add_entity(gs.morphs.Plane())
liquid = scene.add_entity(
    # mu = viscosity, gamma = surface tension
    # material=gs.materials.SPH.Liquid(mu=0.02, gamma=0.02),
    material=gs.materials.SPH.Liquid(
        sampler='pbs',
    ),
    morph=gs.morphs.Box(
        pos = (0, 0, 0.65),
        size = (0.4, 0.4, 0.4)
    )
)
scene.build()
horizon=1000
for i in range(horizon):
    scene.step()
