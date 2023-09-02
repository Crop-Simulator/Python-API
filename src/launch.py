import typer
import bpy
from dotenv.main import load_dotenv
import time
import sys
import os

from src.controllers.crop_controller import CropController
from src.controllers.yaml_reader import YamlReader
from src.renderers.scene_renderer import SceneRenderer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


load_dotenv()

class TyperLaunchAPI:
    """
    This class is used to launch the application using the Typer library.
    """

    @staticmethod
    def typer_interface(config_file: str):
        config = YamlReader().read_file(config_file)
        TyperLaunchAPI.launch(config)

    @staticmethod
    def launch(config):
        
        model_names = {
            "stage0" : "stage0.stand",
            "stage1": "stage1.stand",
            "stage2": "stage2.stand",
            "stage3": "stage3.stand",
            "stage4": "stage4.stand",
            "stage5": "stage5.stand",
            "stage6": "stage6.stand",
            "stage7": "stage7.stand",
            "stage8": "stage8.stand",
            "stage9": "stage9.stand",
            "stage10": "stage10.stand",
            "ground" : "ground",
            "weed" : "weed",
        }

        start_time = time.time()
        collection_name = "Collection"
        bpy.ops.wm.open_mainfile(filepath="src/blender_assets/CropAssets.blend")
        for obj in bpy.data.objects:
            obj.location = (1000,1000,1000)
        # Set the unit system to metric
        bpy.context.scene.unit_settings.system = "METRIC"
        bpy.context.scene.unit_settings.scale_length = 1.0  # Set the scale to 1.0 for metric units
        cropcon = CropController(config, collection_name)
        scenerender = SceneRenderer(config, collection_name)
        
        
        for day in range(config["growth_simulator"]["total_days"]):
            print("Day:", day)
            cropcon.setup_crops(day)
            scenerender.render_scene(day)
            
        # collection = bpy.data.collections.get(collection_name)
        # for obj in bpy.context.scene.objects:
        #     if obj.name in model_names.values():
        #         target = collection.objects.get(obj.name)
        #         collection.objects.unlink(target)
        end_time = time.time()
        total_time = end_time - start_time
        print("Time taken to run:", total_time)


if __name__ == "__main__":
    typer.run(TyperLaunchAPI.typer_interface)

