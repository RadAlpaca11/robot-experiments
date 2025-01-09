Genesis is a universal physics engine developed entirely in python. It is lightweight, fast, and very user-friendly.

# Installation
Getting Genesis installed is as easy as:
```
pip install genesis-world
```
and installing PyTorch.

# Learning to use the simulator
The genesis documentation has detailed tutorials, which we followed through, built off of, and quickly learned how to write our own programs for the simulator.




## Notes:
- Completely in python

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

- [documentation](https://genesis-world.readthedocs.io/en/latest/api_reference/index.html)

- 12/17/24 when testing inverse kinematics with spot: [Genesis] [14:46:43] [ERROR] Motion planning is not yet supported for rigid entities with free joints.

## Questions:
- inverse kinematics doesn't need explicit definitions of joints?
- what materials and shapes are avalible in the simulator?