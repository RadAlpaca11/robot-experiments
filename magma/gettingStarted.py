from magmaSource.magma.processing_magma import MagmaProcessor
from magmaSource.magma.modeling_magma import MagmaForCausalLM
import torch

dtype = torch.bfloat16
model = MagmaForCausalLM.from_pretrained("microsoft/Magma-8B", trust_remote_code=True, torch_dtype=dtype)
processor = MagmaProcessor.from_pretrained("microsoft/Magma-8B", trust_remote_code=True)
model.to("cuda")