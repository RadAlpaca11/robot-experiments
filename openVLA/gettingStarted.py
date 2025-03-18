# Install minimal dependencies (`torch`, `transformers`, `timm`, `tokenizers`, ...)
# > pip install -r https://raw.githubusercontent.com/openvla/openvla/main/requirements-min.txt
from transformers import AutoModelForVision2Seq, AutoProcessor
from PIL import Image

import sys
sys.path.append('/openvlaSource/prismatic/conf')

from openvlaSource.prismatic.conf import vla

import torch

# Load Processor & VLA
processor = AutoProcessor.from_pretrained("openvla/openvla-7b", trust_remote_code=True)
model = AutoModelForVision2Seq.from_pretrained(
    "openvla/openvla-7b", 
    #attn_implementation="flash_attention_2",  # [Optional] Requires `flash_attn`
    torch_dtype=torch.bfloat16, 
    low_cpu_mem_usage=True, 
    trust_remote_code=True
).to("cuda:0")

# Grab image input & format prompt
#image: Image.Image = 'get_from_camera(...)'
image = Image.open('openVLA/pickcokecan.png')
#prompt = "In: What action should the robot take to {<INSTRUCTION>}?\nOut:"
prompt = "In: What action should the robot take to pick up the coke can?\nOut:"

# Predict Action (7-DoF; un-normalize for BridgeData V2)
inputs = processor(prompt, image).to("cuda:0", dtype=torch.bfloat16)
action = model.predict_action(**inputs, unnorm_key="bridge_orig", do_sample=False)

# Execute...
# robot.act(action, ...)
# print(robot.act(action, ...))
print(action[2])