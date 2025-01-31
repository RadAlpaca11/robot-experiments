# Some issues we experience often and how to solve them

One issue we run into is with CUDA:
```
RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1
Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
```
This typically occurs when we first run code after the computer was suspended. We fix this by restarting the computer.