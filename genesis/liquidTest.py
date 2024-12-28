# there's a lot going on here
# there should be liquid in the scene
# there should be a fluid emitter in the scene?
# there should be an elastic box in the scene?

import genesis as gs

gs.init(backend=gs.cpu)

# combination of previous code used to set up scene, and instructions for fluid simulation
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt = 4e-3,
        substeps = 10,
    ),
    sph_options = gs.options.SPHOptions(
        lower_bound = (-0.5, -0.5, 0.0),
        upper_bound = (0.5, 0.5, 1),
        particle_size = 0.01,
    ),
    vis_options = gs.options.VisOptions(
        visualize_sph_boundary = True,
        show_world_frame = True,
        world_frame_size = 1.0,
        show_link_frame = False,
        show_cameras = False,
        plane_reflection = True,
        ambient_light = (0.1, 0.1, 0.1),
    ),
    show_viewer = True,
    viewer_options = gs.options.ViewerOptions(
        res = (1280, 960),
        camera_pos = (0.5, 0.5, 0.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov = 40,
        max_FPS = 60,
    ),
    renderer = gs.renderers.Rasterizer(),
)

plane = scene.add_entity(gs.morphs.Plane())
fluid = scene.add_entity(
    #material = gs.materials.SPH.liquid(mu=0.02, gamma=0.02),
    morph = gs.morphs.Box(
        size = (0.4, 0.4, 0.4),
        pos = (0.0, 0.0, 0.65),
    ),
    surface = gs.surfaces.Default(
        color = (0.4, 0.8, 1.0),
        vis_mode = 'particle',
    ),
)
elastic = scene.add_entity(
    material = gs.materials.MPM.Elastic(),
    morph = gs.morphs.Box(
        size = (0.2, 0.3, 0.2),
        pos = (0.0, -0.5, 0.25),
    ),
    surface = gs.surfaces.Default(
        color = (1.0, 0.4, 0.4),
        vis_mode = 'particle',
    ),
)

emitter = scene.add_emitter(
    material = gs.matherials.SPH.liquid(mu=0.02, gamma=0.02),
    max_particles = 1000,
    surface = gs.surfaces.Default(
        color = (0.4, 1.0, 0.8),
        vis_mode = 'particle',
    ),
)

cam = scene.add_camera(
    res = (640, 480),
    pos = (0.5, 0.5, 0.5),
    fov = 100,
    GUI = True,
)

scene.build()

cam.start_recording()

for i in range(250):
    scene.step()
    cam.render()

particles = fluid.get_particles()

cam.stop_recording(save_to_filename='picsAndVids/liquidTest.mp4')