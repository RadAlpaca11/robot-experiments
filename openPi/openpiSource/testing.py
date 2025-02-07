from src.openpi.training import config
from src.openpi.policies import policy_config
from src.openpi.shared import download

import numpy as np

config = config.get_config("pi0_fast_droid")
checkpoint_dir = download.maybe_download("s3://openpi-assets/checkpoints/pi0_fast_droid")

# Create a trained policy.
policy = policy_config.create_trained_policy(config, checkpoint_dir)


# # Run inference on a dummy example.
# example = {
#     "observation/exterior_image_1_left": ...,
#     "observation/wrist_image_left": ...,
#     #... add oher pairs as needed
#     "observation/joint_position": ...,
#     "observation/gripper_position": ...,
#     "prompt": "pick up the fork"
# }
# action_chunk = policy.infer(example)["actions"]

# Run inference on a dummy example.
example = {
    "observation/exterior_image_1_left": np.random.rand(224, 224, 3),  # Example image data
    "observation/wrist_image_left": np.random.rand(224, 224, 3),  # Example image data
    "observation/joint_position": np.array([0.0, 0.1, 0.2]),  # Example joint position data
    "observation/gripper_position": np.array([0.1]),  # Example gripper position data
    "prompt": "pick up the fork"
}
action_chunk = policy.infer(example)["actions"]
print(action_chunk)

