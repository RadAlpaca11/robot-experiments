import numpy as np
from omni.isaac.core.objects import FixedCuboid, DynamicCuboid
from omni.isaac.examples.base_sample import BaseSample

class Demo(BaseSample):
    def __init__(self) -> None:
        super().__init__()
        return

    def setup_scene(self):
        # Used to add assets.
        # Only called to load the world starting from an EMPTY stage.
        pass

    async def setup_post_load(self):
        pass

    def physics_step(self, step_size):
        pass
