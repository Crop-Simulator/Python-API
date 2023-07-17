import bpy
import bpycv
import numpy as np
import cv2


class SegmentationClass:
    BACKGROUND = 0
    PLANT = 1


class SegmentationColor:
    # Color code in [B, G, R]
    LAND_GROUND_SOIL = [255, 194, 0]
    SKY = [230, 230, 6]
    PLANT = [4, 255, 204]


class Segmentation:
    def __init__(self, color_map=None) -> None:
        """
        color_map: a dictionary of class ids to segmentation map values
        """
        if color_map is None:
            color_map = {}
        self.color_map = color_map

    def add_class(self, class_id: int, segmentation_value: int):
        self.color_map[class_id] = segmentation_value

    def remove_class(self, class_id: int):
        del self.color_map[class_id]

    def segment(self, output_file: str):
        self._assign_classes()
        rendered_data = self._render_segmentation()
        segmentation = rendered_data["inst"]
        self._write_segmentation(segmentation, output_file)

    def _assign_classes(self):
        for obj in bpy.data.objects:
            if "segmentation_id" in obj:
                if obj["segmentation_id"] in self.color_map:
                    obj["inst_id"] = obj["segmentation_id"]
                elif obj["segmentation_id"] != 0:
                    print(
                        "WARNING: Unknown segmentation id: "
                        + str(obj["segmentation_id"]),
                    )

    def _render_segmentation(self):
        rendered_data = bpycv.render_data()
        # Transform the greyscale instance map to a RGB image
        id_to_color = self.color_map
        rendered_data["inst"] = np.array(
            [id_to_color[inst_id] for inst_id in rendered_data["inst"].flatten()],
        ).reshape(rendered_data["inst"].shape + (3,))
        return rendered_data

    def _write_segmentation(self, im, output_file: str):
        # save instance map as 16bit grey scale image
        cv2.imwrite(output_file, im)
