import base64
import cv2
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor
from .api import StableDiffusionAPI

from .connector import generate_image

def encode_png(path: str) -> str:
    im = cv2.imread(path)
    encoded = base64.encodebytes(cv2.imencode(".png", im)[1]).decode("utf-8")
    return encoded

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.processed_files = set()

    def on_modified(self, event):
        # Watch for the modification of depth maps
        # Check if the file is a .png file
        if event.src_path.endswith(".png"):
            base_file_name = event.src_path.replace("_depth.png", "").replace("_seg.png", "")
            scene_file = base_file_name + ".png"
            seg_file = base_file_name + "_seg.png"
            depth_file = base_file_name + "_depth.png"
            if os.path.exists(scene_file) and os.path.exists(seg_file) and os.path.exists(depth_file) \
                and scene_file not in self.processed_files:
                self.executor.submit(self.handle_new_image_pair, scene_file, seg_file, depth_file)
                self.processed_files.add(scene_file)

    def handle_new_image_pair(self, img_path, seg_path, depth_file):
        # Read images and call handler function here
        print(f"Handling image pair: {img_path}, {seg_path}, {depth_file}")
        with open(seg_path, "rb") as seg_file:
            seg_file.seek(0)
            image_name = os.path.basename(img_path).replace(".png", "")
            encoded_img = encode_png(img_path)
            encoded_seg = encode_png(seg_path)
            encoded_depth = encode_png(depth_file)
            url = os.environ.get("SD_API_URL", "http://localhost:7860")
            text_prompt = "best quality, 4k, 8k, ultra highres, raw photo\
            sharp focus, intricate texture, skin imperfections, photograph of barley with weed,\
            crop field, soil, sunlight, photo, photorealistic"
            disable_controlnet = os.environ.get("DISABLE_CONTROLNET", "false").lower() == "true"
            width = int(os.environ.get("WIDTH", "512"))
            height = int(os.environ.get("HEIGHT", "512"))

            sd_api_client = StableDiffusionAPI(url)
            images = generate_image(sd_api_client, config={"prompt": text_prompt, "width": width, "height": height},
                            controlnet_config={
                                "disable_controlnet": disable_controlnet,
                                "segmentation_mask": encoded_seg,
                                "depth_mask": encoded_depth,
                            },
                            input_image=encoded_img)

            print(f"Generated {len(images)} images")
            # Save the generated images to disk
            for idx, img in enumerate(images):
                save_file = f"{image_name}_sd{idx}.png"
                with open(save_file, "wb") as f:
                    f.write(base64.decodebytes(bytes(img, "utf-8")))
                print(f"Image {idx} saved to {save_file}")
            if img_path in self.processed_files:
                self.processed_files.remove(img_path)


if __name__ == "__main__":
    path = "output_images" # the path to the directory to watch
    try:
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        print(f"Watching directory {path} for new image pairs...")
    except FileNotFoundError as e:
        e.strerror += f'. The given path is "{path}"'
        raise e
    try:
        while True:
            # yield the current thread
            time.sleep(0)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
