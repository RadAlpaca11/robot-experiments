import sys
sys.path.append('/home/a3r/Interns/internship2024-25/openvlaOFT/openvla-oft')
sys.path.append('/home/a3r/Interns/internship2024-25/openvlaOFT/openvla-oft/prismatic/vla/datasets/rlds/oxe/configs')
sys.path.append('/home/a3r/Interns/internship2024-25/openvlaOFT/openvla-oft/prismatic/vla')
sys.path.append('/home/a3r/Interns/internship2024-25/openvlaOFT/openvla-oft/prismatic')

# from prismatic.vla.datasets.rlds.dataset import make_dataset_from_rlds
# from prismatic.vla.datasets.rlds.oxe.configs import OXE_DATASET_CONFIGS
# from prismatic.vla.datasets.rlds.oxe.materialize import make_oxe_dataset_kwargs

# # config = OXE_DATASET_CONFIGS["libero_spatial_no_noops"]

# # config.pop('state_encoding', None)
# # config.pop('action_encoding', None)

# #dataset = make_dataset_from_rlds("libero_spatial_no_noops", 'prismatic/vla/datasets/rlds/oxe/configs', train=False, action_proprio_normalization_type="none", **config)

# dataset = make_oxe_dataset_kwargs("libero_spatial_no_noops", '/home/a3r/Interns/internship2024-25/openvlaOFT/openvla-oft/prismatic/vla/datasets/rlds/oxe/configs', load_camera_views=("primary",), load_depth=False, load_proprio=True, load_language=True, action_proprio_normalization_type="none")

# print(dataset)

from prismatic.vla.datasets.rlds.dataset import make_dataset_from_rlds
from prismatic.vla.datasets.rlds.oxe.configs import OXE_DATASET_CONFIGS

config = OXE_DATASET_CONFIGS["libero_spatial_no_noops"]

config.pop('state_encoding', None)
config.pop('action_encoding', None)

# Update the dataset directory to the correct path
dataset_dir = 'experiments/robot/libero/LIBERO/libero/libero/bddl_files'  # Replace with the correct path

dataset = make_dataset_from_rlds("libero_spatial_no_noops", dataset_dir, train=False, action_proprio_normalization_type="none", **config)

print(dataset)