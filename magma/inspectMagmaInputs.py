from transformers import AutoModelForCausalLM, AutoTokenizer
import inspect

# Load model (trust_remote_code is required for Magma)
model = AutoModelForCausalLM.from_pretrained("microsoft/Magma-8B", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/Magma-8B", trust_remote_code=True)

# Print the signature of the forward method
print("Model forward signature:")
print(inspect.signature(model.forward))

# Try to get dummy inputs using the tokenizer
sample_text = "Hello, world!"
inputs = tokenizer(sample_text, return_tensors="pt")

print("\nTokenized text input keys and shapes:")
for k, v in inputs.items():
    print(f"{k}: {v.shape}")

# If the model expects an image, you will need to create a dummy one.
try:
    from PIL import Image
    import torch

    # Create a dummy RGB image (batch size 1, 3 channels, 224x224)
    dummy_img = torch.zeros(1, 3, 224, 224)
    print("\nDummy image tensor shape for 'pixel_values':", dummy_img.shape)
except ImportError:
    print("\nPIL or torch not installed, skipping dummy image creation.")

# Optionally, print model outputs for these dummy inputs if you have the resources