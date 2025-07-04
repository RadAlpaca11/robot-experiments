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
ur10 = scene.add_entity(
    gs.morphs.URDF(file= '../ur_description/ur10_joint_limited_robot.urdf'),
)
jnt_names = [
    'shoulder_pan_joint',
    'shoulder_lift_joint',
    'elbow_joint',
    'wrist_1_joint',
    'wrist_2_joint',
    'wrist_3_joint',
]
dofs_idx = [ur10.get_joint(name).dof_idx_local for name in jnt_names]
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
# PD control
for i in range(1250):
    if i == 0:
        ur10.control_dofs_position(
            np.array([1, -1, 0, 0, 0, 0]),
            dofs_idx,
        )
    elif i == 250:
        ur10.control_dofs_position(
            np.array([-1.5, 0.8, 1, -2, 1, 0.5]),
            dofs_idx,
        )
    elif i == 500:
        ur10.control_dofs_position(
            np.array([0, 0, 0, 0, 0, 0]),
            dofs_idx,
        )
    elif i == 750:
        # control first dof with velocity, and the rest with position
        ur10.control_dofs_position(
            np.array([0, 0, 0, 0, 0, 0])[1:],
            dofs_idx[1:],
        )
        ur10.control_dofs_velocity(
            np.array([1.0, 0, 0, 0, 0, 0])[:1],
            dofs_idx[:1],
        )
    elif i == 1000:
        ur10.control_dofs_force(
            np.array([0, 0, 0, 0, 0, 0]),
            dofs_idx,
        )
    # This is the control force computed based on the given control command
    # If using force control, it's the same as the given control command
    print('control force:', ur10.get_dofs_control_force(dofs_idx))

    # This is the actual force experienced by the dof
    print('internal force:', ur10.get_dofs_force(dofs_idx))

    scene.step()
    cam.render()

cam.stop_recording(save_to_filename='genesis/movement!.mp4', fps=60)