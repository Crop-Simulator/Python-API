
import typer
import bpy

from controllers.crop_controller import CropController
from controllers.yaml_reader import YamlReader
from renderers.scene_renderer import SceneRenderer


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

        collection = "Collection"
        cropcon = CropController(config, collection)
        scenerender = SceneRenderer(config["outfile"][0], collection)
        cropcon.setup_crops()


        scenerender.render_scene()


if __name__ == "__main__":
    typer.run(TyperLaunchAPI.typer_interface)
