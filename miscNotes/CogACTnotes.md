# Sources
[Website](https://cogact.github.io/)

[Code](https://github.com/microsoft/CogACT)

[Paper](https://cogact.github.io/CogACT_paper.pdf)

# Summary
CogACT is a VLA architecture derived from VLM. 
It has a specialized action model trained on outputs from the VLM and improves performance with a model size smaller than other VLAs.

The model will only work on a server-class machine.

## The model
The CogACT model leverages a pretrained Prismatic-7b VLM, with the output being used as the input for the action model.
The action model generates a series of actions, with a diffusion modeling process predicting the action.
The model also predicts actions for multiple time steps with and Adaptive Action Ensemble strategy to aggregate similiatities between actions.

# Getting it working
**We are currently unable to run the model (more details below)**

Needs cuda to run.

Loading the VLA takes a few minutes (5+) even with the small size model.

We used miniconda to set up the environment:
```
conda create --name cogact python=3.10
```

We also needed to add some things to the path for miniconda and pip:
```
/miniconda3/bin
/.local/bin
```

We then followed the installation in CogACT's README, and skipped the training code at first.
Following the instructions for SimplerEnv to evaluate was unsuccessful with the program being unable to find TensorRT.

We then tried to run it by itself (not with SimplerEnv) and were unsuccessful with the issue:
```
Cannot access gated repo for url https://huggingface.co/meta-llama/Llama-2-7b-hf/resolve/main/config.json.
Access to model meta-llama/Llama-2-7b-hf is restricted. You must have access to it and be authenticated to access it. Please log in.
```

After getting setup in HuggingFace we tried again, and the access issue was solved.

Currently we are unable to run the model. 
This is due to errors on both the server machine, and the one we have been using the whole time. 
On January 9th we were getting errors about cuda out of memory, and on January 16th we got those same errors on the server machine. When we tried ot run the model on the machine we had used previously we recieved different errors. First we got 
```
RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1
Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
```
then after uninstalling 'tensorflow[and-cuda]' we got
```
RuntimeError: CUDA unknown error - this may be due to an incorrectly set up environment, e.g. changing env variable CUDA_VISIBLE_DEVICES after program start. Setting the available devices to be zero.
```
# Notes
We are unable to find any helpful documentation for the code.

It helped to remove the version specification in the pyproject.toml for tensorflow before running pip install -e.