
import typer
import bpy

from controllers.crop_controller import CropController
from controllers.yaml_reader import YamlReader
from renderers.scene_renderer import SceneRenderer
from controllers.camera_controller import CameraController
from controllers.weather_controller import WeatherController
from controllers.soil_controller import SoilController
from controllers.nutrient_controller import NutrientController


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
        bpy.ops.wm.open_mainfile(filepath="src/blender_assets/CropAssets.blend")
        wc = WeatherController("2b8fb3c4f62844189b7edec1063d92f9")
        temperature, precipitation, humidity, sun_rise, sun_set = wc.calculate_weather_conditions(37.7749, -122.4194)
        wc.calculate_sunlight_hours(sun_rise, sun_set)

        sc = SoilController()
        soil_conditions = sc.input_data("loamy", precipitation, temperature)
        soil_conditions = sc.calculate_soil_conditions()

        moisture_content_in_soil = soil_conditions["moisture_content_in_soil"]
        ph_level_in_soil = soil_conditions["ph_level_in_soil"]
        # Assume these values are current conditions
        crop_growth_stage = 5
        weed_proximity = 2

        nutrient_controller = NutrientController(crop_growth_stage, weed_proximity, moisture_content_in_soil, ph_level_in_soil)

        # Get the predicted water and nutrient levels
        nutrient_controller.get_water_level()
        nutrient_controller.get_nutrient_level()


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
