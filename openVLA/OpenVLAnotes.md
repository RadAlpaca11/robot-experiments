# Sources
[Website](https://openvla.github.io/)

[Code](https://github.com/openvla/openvla)

[Paper](https://arxiv.org/abs/2406.09246)

# Summary
OpenVLA is a 7B parameter VLA that is pretrained on 970k episodes from the Open X-Embodiment dataset and focused on generalist robotics manipulation.

Results from testing show strong results for multi-purpose manipulation especially in multi-task and multi-object scenarios.
More detailed results can be found on their website.

We have not yet been able to get the model running due to the issues with access to Llama 2 7B and with installing dependencies.

# Installation
We cloned the repository, and ran ```pip install -e.``` to install the dependencies.

You also need to get access to the huggingface model, which is explained in the openvla README


# Combining with 

# Notes
Key elements of the model:
- fused visual encoder
- projector
- Llama 2 7B language model backbone

The model has 3 outputs, a change in x, change in theta, and change in grip. 

You don't need to use flash attention 2, you  can comment it out in the code.

From the github README: 

Note: OpenVLA typically requires fine-tuning on a small demonstration dataset (~100 demos) from your target domain robot. Out-of-the-box, it only works well on domains from the training dataset.

Fine-tuning and fully fine-tuning would require server class machines.



# Solving pip install vla issues
* switched to use opencv-python-headless to use with the debugger
* Checked ~/.bashrc and removed pi0 vla configs
* removed and reinstalled conda
* recreated the openvla conda environment with python=3.10 as openvla2 (using the instructions from openvla README)
* created launch.json file through vscode and used copilot to set jusMyCode to false in the launch file for debugging other files
* deleted huggingface cache for openvla to force a redownload
