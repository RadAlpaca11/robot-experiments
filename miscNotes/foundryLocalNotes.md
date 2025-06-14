# Foundry Local
[Getting started tutorial](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-local/get-started)

Foundry Local can be used to run models locally on Windows or MacOS
### Installing Foundry Local

Windows:
```
winget install Microsoft.FoundryLocal
```
MacOS:
```
brew tap microsoft/foundrylocal
brew install foundrylocal
```
### Running a model (phi-3.5-mini)
```
foundry model run phi-3.5-mini
```
to exit interactive chat:
```
/exit
```
## Compile Huggingface models to run on Foundry Local
Install Olive to optimize models to ONNX format
(The guide suggests using a virtual environment, so you can create one if you want)
```
pip install olive-ai
```
Sign in to Huggingface
```
huggingface-cli login
```
Download and convert models
```
olive auto-opt \
    --model_name_or_path microsoft/Magma-8B \
    --trust_remote_code \
    --output_path models/magma \
    --device cpu \
    --provider CPUExecutionProvider \
    --use_ort_genai \
    --precision int4 \
    --log_level 1
```
In order for this to work, had to run
```
pip install onnxruntime torchvision open_clip_torch
```

| Parameter | Description |
| --- | ---|
| model_name_or_path | Model source: Hugging Face ID, local path, or Azure AI Model registry ID|
| output_path | Where to save the optimized model |
| device | Target hardware: cpu, gpu, or npu |
| provider | Execution provider (for example, CPUExecutionProvider, CUDAExecutionProvider) |
| precision | Model precision: fp16, fp32, int4, or int8 |
| use_ort_genai | Creates inference configuration files |


Got this error:
```
ValueError: Unable to get dummy inputs for the model. Please provide io_config or install an optimum version that supports the model for export.
```

## On Windows:



### When installing olive-ai: 
```
[WinError 206] The filename or extention is too long
```
To solve, ran
```
regedit
```
Navigate to 
```
HKEY_LOCAL_MACHINE/SYSTEM/CurrentControlSet/Control/FileSystem
```
Change variable longPathEnabled to 1

### Installing Huggingface:
Pip install did not work; had to use
```
conda install conda-forge::huggingface_hub
```
huggingface-cli login did not work because pip was not installed
Installed pip
Torch doesn't work with python 3.13; had to downgrade to 3.10
Had to pip install onnxruntime