from PIL import Image
import torch
import numpy as np
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor 

dtype = torch.bfloat16
model = AutoModelForCausalLM.from_pretrained("microsoft/Magma-8B", trust_remote_code=True, torch_dtype=dtype)
processor = AutoProcessor.from_pretrained("microsoft/Magma-8B", trust_remote_code=True)
model.to("cuda")

# Inference
image = Image.open("../openVLA/picsAndVids/magmaPic.png").convert("RGB")

convs = [
    {"role": "system", "content": "You are an agent that can see, talk, and act."},            
    {"role": "user", "content": "<image_start><image><image_end>\n What is the first step to move the robot to touch the yellow block?"},
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

# get the last action, and convert the action (as token) to a discretized action
generate_ids = generate_ids[0, -8:-1].cpu().tolist()

predicted_action_ids = np.array(generate_ids).astype(np.int64)
discretized_actions = processor.tokenizer.vocab_size - predicted_action_ids

print(discretized_actions)


# i=0

# for id in generate_ids:
#     nextId = id.cpu().tolist()
#     predictedId = np.array(nextId).astype(np.int64)
#     discretizedId = processor.tokenizer.vocab_size - predictedId
#     print(discretizedId)
#     i+=1
#     print(i)

