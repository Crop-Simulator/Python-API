import typer
import bpy
from dotenv.main import load_dotenv
import os

import time

from controllers.crop_controller import CropController
from controllers.yaml_reader import YamlReader
from renderers.scene_renderer import SceneRenderer
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
        
        start_time = time.time()
        """"
        Commented out while we wait for IBM's API key Tests also need to be written
        planting_date = config["planting_date"]
        lat = config["latitude"]
        lon = config["longitude"]
        barley_type = config["barley_type"]
        api_key = os.environ["WEATHER_API"]
        weather_controller = WeatherController(api_key)
        weather_data = weather_controller.get_weather_for_growth_period(barley_type, planting_date, lat, lon)
        """

        bpy.ops.wm.open_mainfile(filepath="src/blender_assets/CropAssets.blend")
        collection = "Collection"
        # Set the unit system to metric
        bpy.context.scene.unit_settings.system = "METRIC"
        bpy.context.scene.unit_settings.scale_length = 1.0  # Set the scale to 1.0 for metric units
        cropcon = CropController(config, collection)
        scenerender = SceneRenderer(config, collection)
        cropcon.setup_crops()


        scenerender.render_scene()
        end_time = time.time()
        total_time = end_time - start_time
        print(total_time)


if __name__ == "__main__":
    typer.run(TyperLaunchAPI.typer_interface)

