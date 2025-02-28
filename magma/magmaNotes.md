# Getting it running

# Notes on the guide
The guide on the [README](./README.md) works right away with one exception.
To run the example inference with local code, you do need to get access to the [Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) dataset. 
The [local inference code](./gettingStarted.py) does not output anything, but if you get it to go through without any errors, you should be good to go.

# How we got it working

First we cloned the repository and navigated to the directory:
```bash
git clone https://github.com/microsoft/Magma
cd Magma
```
Then created a conda environment and activated it:
```bash
conda create -n magma python=3.10 -y
conda activate magma
```
Then upgraded pip before installing the requirements:
```bash
pip install --upgrade pip
pip install -e.
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
This worked right away!

We have also spent some time experimenting with input images, and what we can ask magma to do.

One interesting thing is that whenever we ask it to do an action, it spits out gibberish.

# Notes:
- The easiest to get running fast
    - example code works right away
- ran on omniverse simulation machine