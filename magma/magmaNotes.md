# Getting it running

# Notes on the guide
The guide on the [README](./README.md) works right away with one exception.
To run the example inference with local code, you do need to get access to the [Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) dataset. 
The [local inference code](./gettingStarted.py) does not output anything, but if you get it to go through without any errors, you should be good to go.

# How we got it working
We used the terminal on the linux simulation machine in the lab and navigated to the directory where we wanted to install magma.

We then cloned the repository and navigated to the directory:
```bash
git clone https://github.com/microsoft/Magma
cd Magma
```
(Later we actually added it in this repository as a submodule.)

Then created a conda environment and activated it:
```bash
conda create -n magma python=3.10 -y
conda activate magma
```
Then upgraded pip before installing the requirements:
```bash
pip install --upgrade pip

# Don't run this unless in the cloned folder
pip install -e .

pip install -e ".[train]"
pip install -e ".[agent]"
```
Other packages we had to install manually afterward:
```bash
pip install wandb
```
We also installed these packages reccomended in the README from magma:
```bash
# ran these in an outside folder (Interns)
# Install co-tracker
git clone https://github.com/facebookresearch/co-tracker
cd co-tracker
pip install -e .
pip install imageio[ffmpeg]
cd ../
# Install kmeans_pytorch, note: install with pip will leads to error
git clone https://github.com/subhadarship/kmeans_pytorch
cd kmeans_pytorch
pip install -e .
cd ../

# These we ran like normal
pip install ipython
pip install faiss-cpu
pip install decord
```

We created a file called [gettingStarted.py](./gettingStarted.py) and copied the example local code from the README:
```python
from magma.processing_magma import MagmaProcessor
from magma.modeling_magma import MagmaForCausalLM

dtype = torch.bfloat16
model = MagmaForCausalLM.from_pretrained("microsoft/Magma-8B", trust_remote_code=True, torch_dtype=dtype)
processor = MagmaProcessor.from_pretrained("microsoft/Magma-8B", trust_remote_code=True)
model.to("cuda")
```
And running with:
```bash 
python gettingStarted.py
```

After that ran through without errors, we ran the [huggingface inference code](./huggingStarted.py):
```python
from PIL import Image
import torch
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor 

dtype = torch.bfloat16
model = AutoModelForCausalLM.from_pretrained("microsoft/Magma-8B", trust_remote_code=True, torch_dtype=dtype)
processor = AutoProcessor.from_pretrained("microsoft/Magma-8B", trust_remote_code=True)
model.to("cuda")

# Inference
image = Image.open("./assets/images/magma_logo.jpg").convert("RGB")

convs = [
    {"role": "system", "content": "You are agent that can see, talk and act."},            
    {"role": "user", "content": "<image_start><image><image_end>\nWhat is the letter on the robot?"},
]
prompt = processor.tokenizer.apply_chat_template(convs, tokenize=False, add_generation_prompt=True)
inputs = processor(images=[image], texts=prompt, return_tensors="pt")
inputs['pixel_values'] = inputs['pixel_values'].unsqueeze(0)
inputs['image_sizes'] = inputs['image_sizes'].unsqueeze(0)
inputs = inputs.to("cuda").to(dtype)

generation_args = { 
    "max_new_tokens": 500, 
    "temperature": 0.0, 
    "do_sample": False, 
    "use_cache": True,
    "num_beams": 1,
} 

with torch.inference_mode():
    generate_ids = model.generate(**inputs, **generation_args)

generate_ids = generate_ids[:, inputs["input_ids"].shape[-1] :]
response = processor.decode(generate_ids[0], skip_special_tokens=True).strip()

print(response)
```
Using the command
```bash
python huggingStarted.py
```

This worked right away!

We have also spent some time experimenting with input images, and what we can ask magma to do.

One interesting thing is that whenever we ask it to do an action, it spits out gibberish.
Update:
We figured this out! In the paper it mentions using a practice that transforms all the output into text so the robot actions get represented with the last 256 discrete language tokens that are barely used in LLMs. Hence the gibberish.


Once we finally got action outputs, we made some changes to the environment so that we could integrate it with genesis.
```bash
pip install genesis-world

# in our downloads folder (we had this file downloaded)
pip install ompl-1.6.0-cp310-cp310-manylinux_2_28_x86_64
```

We were able to get the model running with genesis and the kuka arm ([code](magmaGen.py)). However this did not yield the results we were hoping. ([videos](picsAndVids))

The outputs of [huggingStarted](huggingStarted.py) were quite large, and we are having some trouble figuring out how to scale them to work in the simulator.

# Notes:
- The easiest to get running fast
    - example code works right away
- ran on omniverse simulation machine

4/1/25: The agents were not working today



# Output logs:
兄弟 direnงเศส肃 المنطقة Yatırımุษย

When asking coordinates of end effector:
兄弟 Yatırım aktivitريع радянційнаุษย



[143 129  59 141 181 127 256]

What is the first step you need to take to move the robot's gripper to the yellow block\
[141 127 101 128 120 143 256]

What is the first step you need to take to move the robot's gripper upwards?\
[143 133  73 137 189 130 256]

How would you move to touch the yellow block?\
[148 133 157 255 126 178 128]

How would you move the robot's gripper to the left?\
[143 133  98 122 133 124 128]




conda install pytorch torchvision torchaudio pytorch-cuda pytorch3d -c pytorch -c nvidia -c pytorch3d
                                                                     