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
        world = self.get_world()
        world.scene.add_default_ground_plane()
        world.scene.add_default_sky()
        world.scene.add(
            FixedCuboid(
                prim_path=f"/World/table",
                name=f"table",
                scale = np.array([0.5, 1.25, 0.2]),
                color=np.array([0.5, 0.5, 0.5]),
                position=np.array([0.7, 0.0, 0.1]),
            )
        )
        world.scene.add(
            DynamicCuboid(
                prim_path=f"/World/cube",
                name=f"cube",
                scale = np.array([0.2, 0.2, 0.2]),
                color=np.array([0, 0.0, 1.0]),
                position=np.array([0.7, 0.0, 0.3]),
            )
        )

        self._table = world.scene.get_object(f"table")
        self._cube = world.scene.get_object("cube")

        pass

    async def setup_post_load(self):
        self._world = self.get_world()
        self._world.add_physics_callback("sim_step", callback_fn=self.physics_step)
        
        pass

    def physics_step(self, step_size):
        pass
