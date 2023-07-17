
import typer
import bpy

from controllers.crop_controller import CropController
from controllers.yaml_reader import YamlReader
from renderers.scene_renderer import SceneRenderer
from controllers.light_controller import LightController


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
        crops = ["stage10.009", "stage9.009", "stage8.009", "stage7.009","stage6.009", "stage5.009", "stage4.009", "stage3.009", "stage2.009", "stage1.009", "stage0.009"]
        bpy.ops.wm.open_mainfile(filepath="src/blender_assets/CropAssets.blend")
        # for ob in bpy.context.scene.objects:
        #     if ob.name != "stage7.009" and ob.name != "stage10.009":
        #         ob.select_set(True)
        # bpy.ops.object.delete()
        for ob in bpy.context.scene.objects:
            if ob.name not in crops:
                ob.select_set(True)
        bpy.ops.object.delete()
        collection = "Collection"
        cropcon = CropController(config, collection)
        scenerender = SceneRenderer(config["outfile"][0], collection)
        lightcon = LightController()
        lightcon.add_light()

        cropcon.setup_crops()
        collection1 = bpy.data.collections.get("Collection")
        for ob in bpy.context.scene.objects:
            if ob.name in crops:
                duplicate = collection1.objects.get(ob.name)
                collection1.objects.unlink(duplicate)

        scenerender.render_scene()


if __name__ == "__main__":
    typer.run(TyperLaunchAPI.typer_interface)
