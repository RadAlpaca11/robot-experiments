# Sources
[Website](https://playground.mujoco.org/)

[Code](https://github.com/google-deepmind/mujoco_playground/)

[Paper](https://playground.mujoco.org/assets/playground_technical_report.pdf)

# Summary

# Installation
To install we used the notebooks provided, which include commands to install all necessary packages as you go along.

We needed to install a CUDA-enabled jaxlib, which we did with the following command:
```python
! pip install -U "jax[cuda12]"
```

We also had to install the datetime package ourselves, so we added a cell to the notebook:
```python
!pip install datetime
```

# Testing

output1: 