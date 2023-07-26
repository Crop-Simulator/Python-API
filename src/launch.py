
import typer
import bpy

from controllers.crop_controller import CropController
from controllers.yaml_reader import YamlReader
from renderers.scene_renderer import SceneRenderer
from controllers.camera_controller import CameraController
from controllers.weather_controller import WeatherController

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
        planting_date = config["planting_date"]
        lat = config["latitude"]
        lon = config["longitude"]
        barley_type = config["barley_type"]
        # api_key = os.environ['WEATHER_API']
        # weather_controller = WeatherController(api_key)
        weather_controller = WeatherController("f9590b70bfae4938a98e0cbd86aa2877")
        weather_data = weather_controller.get_weather_for_growth_period(barley_type, planting_date, lat, lon)
        print(weather_data)

        bpy.ops.wm.open_mainfile(filepath="src/blender_assets/CropAssets.blend")
        # for ob in bpy.context.scene.objects:
        #     print(ob.name)
        for ob in bpy.context.scene.objects:
            if ob.name != "stage11.1":
                ob.select_set(True)
        bpy.ops.object.delete()
        collection = "Collection"
        cameracon = CameraController()
        cropcon = CropController(config, collection)
        scenerender = SceneRenderer(config["outfile"][0], collection)
        cameracon.setup_camera("camera_one", (10,0,0), (1.57057,0.00174533,1.57057), "Collection")
        cropcon.setup_crops()
        collection1 = bpy.data.collections.get("Collection")
        dupe = collection1.objects.get("stage11.1")
        collection1.objects.unlink(dupe)

        scenerender.render_scene()


if __name__ == "__main__":
    typer.run(TyperLaunchAPI.typer_interface)
