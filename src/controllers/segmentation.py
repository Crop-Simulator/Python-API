import bpy
import bpycv
import numpy as np
import cv2


class Segmentation:
    def __init__(self, classes=None) -> None:
        """
        classes: a dictionary of class ids to segmentation map values
        """
        if classes is None:
            classes = {}
        self.classes = classes

    def add_class(self, class_id: int, segmentation_value: int):
        self.classes[class_id] = segmentation_value

    def remove_class(self, class_id: int):
        del self.classes[class_id]

    def segment(self, output_file: str):
        self._assign_classes()
        rendered_data = self._render_segmentation()
        segmentation = rendered_data["inst"]
        self._write_segmentation(segmentation, output_file)

    def _assign_classes(self):
        for obj in bpy.data.objects:
            if "segmentation_id" in obj:
                if obj["segmentation_id"] in self.classes:
                    obj["inst_id"] = self.classes[obj["segmentation_id"]]
                elif obj["segmentation_id"] != 0:
                    print(
                        "WARNING: Unknown segmentation id: "
                        + str(obj["segmentation_id"]),
                    )

    def _render_segmentation(self):
        rendered_data = bpycv.render_data()
        return rendered_data

    def _write_segmentation(self, im, output_file: str):
        # save instance map as 16bit grey scale image
        cv2.imwrite(output_file, np.uint16(im))
