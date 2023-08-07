import base64
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor
from .api import StableDiffusionAPI

from .connector import generate_image

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.processed_files = set()

    def on_modified(self, event):
        # Check if the file is a .png file
        if event.src_path.endswith(".png"):
            base_name = os.path.basename(event.src_path)
            dir_name = os.path.dirname(event.src_path)

            # Check if it's a pair of img_n.png and seg_n.png
            if base_name.endswith("_seg.png"):
                img_file = os.path.join(dir_name, base_name.replace("_seg", ""))
                if os.path.exists(img_file) and img_file not in self.processed_files:
                    self.processed_files.add(event.src_path)
                    self.processed_files.add(img_file)
                    self.executor.submit(self.handle_new_image_pair, img_file, event.src_path)
            else:
                seg_file = os.path.join(dir_name, base_name[:-4]+"_seg.png")
                if os.path.exists(seg_file) and seg_file not in self.processed_files:
                    self.processed_files.add(event.src_path)
                    self.processed_files.add(seg_file)
                    self.executor.submit(self.handle_new_image_pair, event.src_path, seg_file)

    def handle_new_image_pair(self, img_path, seg_path):
        # Read images and call handler function here
        print(f"Handling image pair: {img_path} and {seg_path}")
        with open(img_path, "rb") as _img_file, open(seg_path, "rb") as seg_file:
            seg_file.seek(0)
            image_name = os.path.basename(img_path).replace(".png", "")
            _encoded_img = base64.b64encode(_img_file.read()).decode("utf-8")
            encoded_seg = base64.b64encode(seg_file.read()).decode("utf-8")
            print(f"Encoded image: {_encoded_img[:100]}...")
            url = "http://localhost:7860"
            text_prompt = "best quality, 4k, 8k, ultra highres, raw photo in hdr,\
            sharp focus, intricate texture, skin imperfections, photograph of wheat,\
            crop field, soil, sunlight, photo, photorealistic, spring, sprouting"
            disable_controlnet = os.environ.get("DISABLE_CONTROLNET", "false").lower() == "true"
            width = int(os.environ.get("WIDTH", "512"))
            height = int(os.environ.get("HEIGHT", "512"))

            sd_api_client = StableDiffusionAPI(url)
            images = generate_image(sd_api_client, text_prompt,
                                    disable_controlnet=disable_controlnet, segmentation_mask=encoded_seg, width=width, height=height)

            print(f"Generated {len(images)} images")
            # Save the generated images to disk
            for idx, img in enumerate(images):
                save_file = f"{image_name}_sd{idx}.png"
                with open(save_file, "wb") as f:
                    f.write(base64.decodebytes(bytes(img, "utf-8")))
                print(f"Image {idx} saved to {save_file}")
            self.processed_files.remove(img_path)
            self.processed_files.remove(seg_path)


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
