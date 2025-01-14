# Genesis sources
[Website](https://genesis-embodied-ai.github.io/)

[Code](https://github.com/Genesis-Embodied-AI/Genesis)

[Documentation](https://genesis-world.readthedocs.io/en/latest/)

Paper is coming soon.

# Summary
Genesis is a universal physics engine developed entirely in python, and controlled with python code. It is lightweight, fast, and very user-friendly. There are plans to include more features, including AI-generated scenes and assets.

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

Using these guides to learn, and occasionally utilizing the [API Reference](https://genesis-world.readthedocs.io/en/latest/api_reference/index.html) has allowed us to write our own code for the simulator.

# Some of our work
After working throught he first two tutorials in the user guide, we felt comfortable enough to start writing our own code, playing around with spawning assets.

<!-- <video src="../genesis/picsAndVids/spotSandwich.mp4" width="320" height="240" controls></video> -->
![Spot sandwich](../genesis/picsAndVids/spotSandwich.mp4)

[Spot sandwich](../genesis/tested/spotSandwich.py)


After getting the hang of that, and successfully completing the Control Your Robot tutorial, we started working on movement. We wanted to explore another model, and after struggling with spot, we decided to try a hand model.
When looking at the xml for the hand model, we finally realized that the joint positions were in radians!
This was also when we discovered the gs view command (see below), which helped us plan the positions for the joints.

<video src="../genesis/picsAndVids/handTest2.mp4" width="320" height="240" controls></video>

[Hand movement](../genesis/tested/handTest2.py)

We then went back to Spot, and took a while trying to get the robot to jump. It took some trial and error, but we finally got it to work.

<video src="../genesis/picsAndVids/jump.mp4" width="320" height="240" controls></video>

[Spot jumping](../genesis/tested/jumpSpot.py)

And then we tried getting Spot to trot. It took a while to get it to stay standing, but discovered that you just really needed to move the legs back down quickly, so that the robot didn't fall over.

<video src="../genesis/picsAndVids/spotTrot1.mp4" width="320" height="240" controls></video>

[Spot trotting](../genesis/tested/spotTrot1.py)


# Installation
Getting Genesis installed was as easy as:
```
pip install genesis-world
```
and installing PyTorch.

# Key findings
- Genesis is very user-friendly and quick to get started with.
- We found the guides and API Reference very helpful in learning how to use the simulator.
- The gs view command is very useful for planning joint positions. (more details in Notes)
- There are plans to have the ability to use AI to generate scenes, assets, and more to the simulator.
- A paper is coming soon, and will hopefully provide deeper insights into the model.

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