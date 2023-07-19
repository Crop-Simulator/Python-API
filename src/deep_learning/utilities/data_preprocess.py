
import cv2
import os
import logging

def extract_frames(video_path: str, output_dir: str, frame_interval: int = 1, output_format: str = "jpg",) -> None:
    """
        Extracts frames from a video file at a specified frame interval and saves them as PNG images.

        Args:
            video_path (str): The path to the input video file.
            output_dir (str): The path to the output directory where the extracted frames will be saved.
            frame_interval (int, optional): The frame interval for extracting frames. Default is 1, which means
                extract one frame per 1 frame read. A higher value will result in fewer extracted frames.
            output_format (str): "png", "jpg", "jpeg", "bmp". See the list at:
                https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56

        Returns:
            None
    """

    logger = logging.getLogger("data_preprocess.extract_frames")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        logger.error(f"Failed to open video file {video_path}")
    else:
        logger.info(f"Opened video file {video_path}")

    # Initialize counters
    frame_number = 0
    output_count = 1

    while video.isOpened():
        # Read the next desired frame
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = video.read()

        if not success:
            break

        # Generate the output file path
        output_path = os.path.join(output_dir, f"{output_count}_frame_{frame_number}.{output_format}")

        # Save the frame
        cv2.imwrite(output_path, frame)
        logger.debug(f"Saved frame {output_count}_frame_{frame_number}.{output_format}")

        # Increment the counters
        output_count += 1
        frame_number += frame_interval

    # Release the video capture and close the window
    video.release()
    cv2.destroyAllWindows()
    logger.info(f"Finished extracting video {video_path}")


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    # Example usage
    video_path = "../demo_data/barley_10_days_old.mp4"
    output_dir = "../demo_data/test_extract"
    frame_interval = 600  # Extract 1 frame per 600 frames
    extract_frames(video_path, output_dir, frame_interval)
