# Sources
[Website](https://agibot-world.com/)

[GitHub](https://github.com/OpenDriveLab/Agibot-World)

# Summary
AgiBot World is a huge (in size and breakthrough) new open source robotics dataset.
Over 1 million trajectories, 100 robots, over 100 real scenarios in 5 areas (Home, Restaurant, Industry, Office, Supermarket).
The majority area was in the home.

It seems as if the 100 robots are made up of many 6DoF robotic arms and mobile 2 arm robots.

The training was in a facility of over 4,000 square meters with partially set-up environments for the robots to test in (imagine robots in IKEA).

# What is in the dataset?
Various hardware including, visual tactile sensors, 6DoF robotic arms, mobile 2 arm robots.

A Jupyter Notebook is included for training diffusion policies.

# Getting it working
We were able to get the dataset visualized. (Did not require server-class machine)

We got access to the dataset through Hugging Face, then started following the At a Quick Glance section of the README in their GitHub. Needs cuda to convert to lerobot.

Visualizing the dataset opens in rerun and has many windows:
- action graph
- observation.images.back_left_fisheye
- observation.images.back_right_fisheye
- observation.images.cam_top_depth
- observation.images.hand_left
- observation.images.hand_right
- observation.images.head_center_fisheye
- obsercation.images.head_left_fisheye
- observation.images.head_right_fisheye
- observation.images.top_head
- state graph

## Experimenting with the dataset
We have so far visualized a few tasks, using the process described below in the Notes section.
- task_355
- task_390
- task_422

# Notes
You need to get the data and then convert it to the lerobot format. (Why do they not provide it in the lerobot format?)
Make sure the .tar file is in the data folder. You should also navigate to the data folder in the terminal before running the commands.
```
# Extract
tar -xvf datafile.tar

# Going back
cd ..

# You can start here if you already have data
# Convert
python scripts/convert_to_lerobot.py --src_path ./data/datafile --task_id 123 --tgt_path ./data/datafile_lerobot

# Visualize
python scripts/visualize_dataset.py --task-id 123 --dataset-path ./data/datafile_lerobot
```

Depth camera appears to be seeing double.

Because the dataset includes a Jupyter Notebook for training diffusion policies, this dataset would likely be quite easy to use for training.

# What does this company (AgiBot) do?
Established in February 2023 and have already started mass producing humanoid robots.
The company makes "general-purpose embodied intelligent robots" as well as manufacturing, scientific research, data collection, and more.