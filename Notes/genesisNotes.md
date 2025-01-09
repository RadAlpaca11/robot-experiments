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

There are two functions for changing the position of a joint:
``` python
# This moves the joint to the position, which relies on defined force ranges
robot.control_dofs_position(position, dofs_idx)

# This "teleports" the joint to the position
robot.set_dofs_position(position, dofs_idx)
```

Motion planning is not yet available for free joints