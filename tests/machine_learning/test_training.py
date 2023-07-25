import unittest
import numpy as np
import shutil
import cv2
import os
from pathlib import Path
from src.machine_learning.utilities.data_preprocess import extract_frames, slice_image, scale_image_to_fill

class TrainingTest(unittest.TestCase):


    def test_extract_frames(self):
        # Test fail to open video file
        with self.assertLogs("data_preprocess.extract_frames", level="ERROR") as cm:
            extract_frames("video_not_exist_path.mp4", "tmp/test_frames")
        self.assertEqual(cm.output, ["ERROR:data_preprocess.extract_frames:Failed to open video file "
                                     "video_not_exist_path.mp4"])

        # Create a random test video
        test_video_path = "tmp/test_video.mp4"
        test_frames_dir = "tmp/test_frames"
        os.makedirs("tmp", exist_ok=True)

        frame_width = 8
        frame_height = 8
        frame_rate = 5
        duration = 2  # seconds
        frame_interval = 3 # extract every ... frames

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(test_video_path, fourcc, frame_rate, (frame_width, frame_height))

        for _ in range(frame_rate * duration):
            frame = np.random.randint(0, 256, (frame_height, frame_width, 3), dtype=np.uint8)
            # frame = np.ones((frame_height, frame_width, 3), dtype=np.uint8)
            video.write(frame)
        video.release()

        # run the function
        with self.assertLogs("data_preprocess.extract_frames", level="INFO") as cm:
            extract_frames(test_video_path, test_frames_dir, frame_interval)
        self.assertEqual(cm.output, [f"INFO:data_preprocess.extract_frames:Opened video file {test_video_path}",
                                     f"INFO:data_preprocess.extract_frames:Finished extracting video {test_video_path}"])

        # Check the output
        frame_files = list(Path(test_frames_dir).glob("*"))
        self.assertEqual(len(frame_files), duration * frame_rate // frame_interval + 1)

        # Delete the test video and frames
        folder_path = os.path.join(os.path.dirname(__file__), "tmp")
        shutil.rmtree(folder_path)

    def test_slice_image(self) -> None:

        # Test image of expected size
        chunks = slice_image(np.ones((512, 512, 3)))
        self.assertEqual(len(chunks), 1) # should output 1 chunk
        self.assertEqual(chunks[0].shape, (512, 512, 3))

        # Test image of 2048x2048
        chunks = slice_image(np.ones((2048, 2048, 3)))
        self.assertEqual(len(chunks), 16)  # should output 1 chunk
        for chunk in chunks:
            self.assertEqual(chunk.shape, (512, 512, 3))

        # Test too small image
        with self.assertLogs("data_preprocess.slice_image_square", level="WARNING") as cm:
            slice_image(np.ones((500, 500, 3)))
        self.assertEqual(cm.output, ["WARNING:data_preprocess.slice_image_square:Image not sliced: "
                                     "original image size (500,500) is smaller than chunk size (512,512)."])

    def test_scale_image_to_fill(self):
        image = scale_image_to_fill(np.ones((3840, 2160, 3)))
        self.assertEqual(image.shape, (910, 512, 3))

        image = scale_image_to_fill(np.ones((2160, 3840, 3)))
        self.assertEqual(image.shape, (512, 910, 3))


if __name__ == "__main__":
    unittest.main()
