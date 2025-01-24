# Sources
[Website](https://playground.mujoco.org/)

[Code](https://github.com/google-deepmind/mujoco_playground/)

[Paper](https://playground.mujoco.org/assets/playground_technical_report.pdf)

# Summary
Currently we have finished the PPO section of the dm_control_suite


# Installation
To install we used the notebooks provided, which include commands to install all necessary packages as you go along.

We also had to install the datetime package ourselves, so we added a cell to the notebook:
```python
!pip install datetime
```

# Testing

Test 1:
```
action_repeat: 1
batch_size: 32
discounting: 0.995
entropy_cost: 0.01
episode_length: 1000
learning_rate: 1.0
normalize_observations: true
num_envs: 512
num_evals: 10
num_minibatches: 16
num_timesteps: 2000
num_updates_per_batch: 16
reward_scaling: 10.0
unroll_length: 30
```
[output1](../mujocoPlayground/mujocoTutorials/output1.png)
[output1](../mujocoPlayground/mujocoTutorials/output1.mp4)


Test 2:
```
action_repeat: 1
batch_size: 32
discounting: 0.995
entropy_cost: 0.01
episode_length: 1000
learning_rate: 1.0
normalize_observations: true
num_envs: 512
num_evals: 10
num_minibatches: 16
num_timesteps: 5000
num_updates_per_batch: 16
reward_scaling: 10.0
unroll_length: 30
```
[output2](../mujocoPlayground/mujocoTutorials/output2.png)
[output2](../mujocoPlayground/mujocoTutorials/output2.mp4)


Test 3:
```
action_repeat: 1
batch_size: 32
discounting: 0.995
entropy_cost: 0.01
episode_length: 1000
learning_rate: 0.5
normalize_observations: true
num_envs: 512
num_evals: 10
num_minibatches: 16
num_timesteps: 5000
num_updates_per_batch: 16
reward_scaling: 10.0
unroll_length: 30
```

Test 4:
```
action_repeat: 1
batch_size: 32
discounting: 0.995
entropy_cost: 0.01
episode_length: 1000
learning_rate: 0.5
normalize_observations: true
num_envs: 512
num_evals: 10
num_minibatches: 16
num_timesteps: 5000
num_updates_per_batch: 32
reward_scaling: 10.0
unroll_length: 30
```

Final results:
```
action_repeat: 1
batch_size: 1024
discounting: 0.995
entropy_cost: 0.01
episode_length: 1000
learning_rate: 0.001
normalize_observations: true
num_envs: 2048
num_evals: 10
num_minibatches: 32
num_timesteps: 1000000
num_updates_per_batch: 16
reward_scaling: 10.0
unroll_length: 30
```
[final result](../mujocoPlayground/mujocoTutorials/finalResult.mp4)