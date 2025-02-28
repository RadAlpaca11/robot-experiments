import torch

if torch.cuda.is_available():
    torch.cuda.empty_cache()
    print("CUDA is available")
    print("cuDNN version:", torch.backends.cudnn.version())
else:
    print("CUDA is not available")