from prismatic.vla.datasets.rlds.dataset import make_dataset_from_rlds
from prismatic.vla.datasets.rlds.oxe.configs import OXE_DATASET_CONFIGS

config = OXE_DATASET_CONFIGS["libero_spatial_no_noops"]

config.pop('state_encoding', None)
config.pop('action_encoding', None)

dataset = make_dataset_from_rlds("libero_spatial_no_noops", 'prismatic/vla/datasets/rlds/oxe/configs', train=False, action_proprio_normalization_type="none", **config)

print(dataset)