import os
from omni.isaac.examples.base_sample import BaseSampleExtension
from .demo import Demo
from omni.kit.menu.utils import add_menu_items, remove_menu_items
from omni.isaac.ui.menu import make_menu_item_description

EXTENSION_TITLE = "Launch Demo"

class DemoExtension(BaseSampleExtension):
    def on_startup(self, ext_id: str):
        super().on_startup(ext_id)
        super().start_extension(
            menu_name="",
            submenu_name="",
            name="Demo",
            title="Isaac Sim Demo",
            doc_link="",
            overview="Simulately Isaac Sim Demo",
            file_path=os.path.abspath(__file__),
            sample=Demo()
        )
