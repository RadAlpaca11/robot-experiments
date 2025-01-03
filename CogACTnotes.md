# Notes on CogACT
- Improves performance with smaller model size
- vision model and language models are separate, but combined and pre-trained
- does it build it's own prompts?
- kinda repeating?
- Unseen means the first time? (We're pretty sure)


# Getting it working
- Needs miniconda
- set up conda environment with
```
conda create --name cogact python=3.10
```
- had to add some things to path for miniconda and pip
```
/miniconda3/bin
/.local/bin
```
- followed Installation in README
- skipping training code for now
- following instructions for SimplerEnv to evaluate
- Issues
    - Could not find TensorRT

- Final issue: Cannot access gated repo for url https://huggingface.co/meta-llama/Llama-2-7b-hf/resolve/main/config.json.
Access to model meta-llama/Llama-2-7b-hf is restricted. You must have access to it and be authenticated to access it. Please log in.
