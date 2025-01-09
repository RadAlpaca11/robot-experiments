# Sources
[Website](https://openvla.github.io/)

[Code](https://github.com/openvla/openvla)

[Paper](https://arxiv.org/abs/2406.09246)

# Summary
OpenVLA is a 7B papameter VLA that is pretrained on 970k episodes from the Open X-Embodiment dataset and focused on generalist robotics manipulation.

Results from testing show strong results for multi-purpose manipulation especially in multi-task and multi-object scenarios.
More detailed results can be found on their website.

We have not yet been able to get the model running due to the issues with access to Llama 2 7B and issues with installing dependencies.

# Notes
Key elements of the model:
- fused visual encoder
- projector
- Llama 2 7B language model backbone

The model has 3 outputs, a change in x, change in theta, and change in grip. 
