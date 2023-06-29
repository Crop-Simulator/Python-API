import typer

from controllers.crop_controller import CropController
from controllers.yaml_reader import YamlReader
from renderers.scene_renderer import SceneRenderer
from controllers.camera_controller import CameraController


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
        collection = "Cube Collection"
        cameracon = CameraController()
        cropcon = CropController(config["crop"], collection)
        scenerender = SceneRenderer(config["outfile"][0], collection)
        cameracon.setup_camera("camera_one", (10,0,0), (1.57057,0.00174533,1.57057), "Cube Collection")
        cropcon.setup_crops()
        scenerender.render_scene()


if __name__ == "__main__":
    typer.run(TyperLaunchAPI.typer_interface)
