CogACT improves performance with a smaller model size, compared to other VLAs.

# The model
The CogACT model leverages a pretrained Prismatic-7b VLM, with the output being used as the input for the action model.
The action model generates a series of actions, with a diffusion modeling process predicting the action.
The model also predicts actions for multiple time steps with and Adaptive Action Ensemble strategy to aggregate similiatities between actions.



# Getting it working
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

After getting setup in HuggingFace we tried again.



# Notes on CogACT
- Improves performance with smaller model size
- vision model and language models are separate, but combined and pre-trained
- does it build it's own prompts?
- kinda repeating?
- Unseen means the first time? (We're pretty sure)