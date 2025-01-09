# Genesis sources
[Website](https://genesis-embodied-ai.github.io/)

[Code](https://github.com/Genesis-Embodied-AI/Genesis)

[Documentation](https://genesis-world.readthedocs.io/en/latest/)

Paper is coming soon.

# Summary
Genesis is a universal physics engine developed entirely in python. It is lightweight, fast, and very user-friendly.

We have gone through some of the Getting Started section of the [user guide](https://genesis-world.readthedocs.io/en/latest/user_guide/index.html).

## User Guide progress
- [x] Hello, Genesis
- [x] Visualization & Rendering
- [x] Control Your Robot
- [ ] Parallel Simulation
- [x] Inverse Kinematics & Motion Planning
- [ ] Advanced and Parallel IK
- [x] Beyond Rigid Bodies (we found this runs really slow)
- [ ] Interactive Information Access and Debugging
- [ ] Training Locomotion Policies with RL
- [ ] Training Drone Hovering Policies with RL
- [ ] Soft Robots
- [x] Command Line Tools

Using these guides to learn, and occasionally referencing the API Reference has allowed us to write our own code for the simulator.

# Installation
Getting Genesis installed was as easy as:
```
pip install genesis-world
```
and installing PyTorch.

# Notes
The gs view command for the terminal opens up two pop up windows, one rendering the starting position of the model, and the other a joint control interface with sliders to control the position of the joints.
```
gs view path/to/model
```
We have utilized this function for planning positions for joints, noting down values to use in our code.

- Motion planning is not yet supported for free joints.

There are two functions for changing the position of a joint:
``` python
# This moves the joint to the position, which relies on defined force ranges
robot.control_dofs_position(position, dofs_idx)

# This "teleports" the joint to the position
robot.set_dofs_position(position, dofs_idx)
```


### Making things exist:

- adding entities:
   ```
   franka = scene.add_entity(
    gs.morphs.MJCF(file='panda.xml',
    pos = (0, 0, 0),)
    )
- if you change franka, change it everywhere
- position = pos
- if you have multiple entities in the same location, they explode

- camera:

   ```
  cam = scene.add_camera(
    res = (640, 480),
    pos = (3.5, 0.0, 0.5),
    fov = 30,
    GUI = True,
    )
- default position is super close
- we've been fixing it by increasing fov, but it gets a fisheye lense effect at high values
- if GUI is set to True, it opens a bunch of windows while the simulation is running (not sure what that is)

- steps:

    ```
    for i in range(1000):
    scene.step()

- steps are like ticks in minecraft
- any changes are implemented at the begining of a step
- the simulator terminates at the end of the index

### Making things move:

- defining joints of a robot

    ```
    jnt_names = [
        'joint1',
        'joint2',
        'joint3',
        'joint4',
        'joint5',
        'joint6',
        'joint7',
        'finger_joint1',
        'finger_joint2',
    ]
    dofs_idx = [franka.get_joint(name).dof_idx_local for name in jnt_names]

- remember the franka thing
  - we use panda
- this puts all of the robot's joints into an array so you can set their positions like this:

  ```
  franka.control_dofs_position(
    np.array([1, 1, 0, 0, 0, 0, 0, 0.04, 0.04]),
    dofs_idx,
  )

- replacing control with set makes the joints "teleport" rather than moving

- 12/17/24 when testing inverse kinematics with spot: [Genesis] [14:46:43] [ERROR] Motion planning is not yet supported for rigid entities with free joints.
