Currently have it working with example code! unable to use our own inputs or evaluate, but it works!

# Notes:
- Optimized for fine-tuning
    - we plan to use it to fine-tune on a dataset we make for specific tasks in genesis
    - hopefully we will be able to make a system to collect data so that we can easily fine tune it for different tasks in the simulator

# Getting it working (short version):
* Setup conda environment from the setup guide in the repository
* Install the requirements (also included in setup guide)
    * Note: if you install torch, and you get errors, follow the instructions through. For us this solved the issue
* Install robosuite
```bash
pip install robosuite==1.4
```
* You may get error with evdev, not being able to build installable wheels. We fixed this with the following commands:
```bash
export CFLAGS="-I/usr/include"
export LDFLAGS="-L/usr/lib"
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
pip install evdev
```
* After this works, you can install robosuite again using the same command as before
* Install robosuite_models
```bash
pip install robosuite_models
```
* There are also a few more packages you need to install:
```bash
pip install bddl
pip install easydict
```
* You need to use git lfs to get the huggingface checkpoints
* You can then run the example code in the repository


# Getting it working (long version):
Followed the setup guide for the conda environment

tried to use example code but had to follow libero instrucitons

got further

no module named 'robosuite'

we first tried to just pip install:
```bash
pip install robosuite==1.4
```

had to manually install 'robosuite' which caused many issues because 'evdev' wouldn't install. Failed to build wheels.
we ended up needing to 

```bash
(openvla-oft) a3r@A3R-Omniverse-Sim:~/Interns/robosuite$ export CFLAGS="-I/usr/include"
(openvla-oft) a3r@A3R-Omniverse-Sim:~/Interns/robosuite$ export LDFLAGS="-L/usr/lib"
(openvla-oft) a3r@A3R-Omniverse-Sim:~/Interns/robosuite$ which gcc
/usr/bin/gcc
(openvla-oft) a3r@A3R-Omniverse-Sim:~/Interns/robosuite$ export CC=/usr/bin/gcc
(openvla-oft) a3r@A3R-Omniverse-Sim:~/Interns/robosuite$ export CXX=/usr/bin/g++
(openvla-oft) a3r@A3R-Omniverse-Sim:~/Interns/robosuite$ pip install evdev
```


Then we got this:
```
ModuleNotFoundError: No module named 'robosuite.environments.manipulation.single_arm_env'
```
we also installed robosuite_models:
```bash
pip install robosuite_models
```

We also had to go back to robosuite==1.4 because SingleArmEnv is gone in 1.5

Also needed to install:

```bash
pip install bddl

pip install easydict
```

You need to use git lfs to get the huggingface checkpoints

Using ```sys.path.append("../..")``` as used in the code kept leading the libraries to be imported from openvla not openVLA-oft.
This was a problem because it wouldn't work with the code it was finding in openvla.

We had to add more paths in various places to get it to work.
```python
sys.path.append("/home/a3r/Interns/internship2024-25/openvlaOFT/openvla-oft/experiments/robot")
sys.path.append('/home/a3r/Interns/internship2024-25/openvlaOFT/openvla-oft')
sys.path.append('/home/a3r/Interns/internship2024-25/openvlaOFT/openvla-oft/prismatic')
sys.path.append('/home/a3r/Interns/internship2024-25/openvlaOFT/openvla-oft/prismatic/models')

```

Not only was this such a pain on it's own, but it also meant that we had to change a bunch of the import statements in the code to get it to work. This was also a pain.

# Example code results (gettingStarted.py):
Generated action chunk (euler rotations):

[0.031 0.062 0.055 -0.000 0.010 -0.000 1.000]

[0.080 0.116 0.051 -0.000 0.012 -0.000 1.000]

[0.212 0.242 0.101 0.007 0.017 0.002 1.000]

[0.412 0.343 0.161 0.012 0.019 0.003 1.008]

[0.671 0.409 0.167 0.016 0.023 0.001 1.000]

[0.796 0.463 0.138 0.007 0.021 0.001 1.000]

[0.865 0.507 0.114 0.004 0.011 0.001 0.996]

[0.898 0.486 0.094 0.016 0.006 0.002 0.992]




cloned LIBERO

moved LIBERO into experiments/robot/libero

added LIBERO. to some paths in run_libero_eval.py to make it work


in run_libero_eval.py needed to change paths to get rid of the experiments.robot.


the imports in run_libero_eval.py want to use files from openVLA for some reason
