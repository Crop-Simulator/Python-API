import cv2
import os
import logging


def extract_frames(video_path: str, output_dir: str, frame_interval: int = 1,
                   output_format: str = "jpg", jpg_quality: int = 95,
                   scale_and_slice_to_512: bool = False) -> None:
    """
        Extracts frames from a video file at a specified frame interval and saves them as images.

        Args:
            video_path (str): The path to the input video file.
            output_dir (str): The path to the output directory where the extracted frames will be saved.
            frame_interval (int, optional): The frame interval for extracting frames. Default is 1, which means
                extract one frame per 1 frame read. A higher value will result in fewer extracted frames.
            output_format (str): "png", "jpg", "jpeg", "bmp". See the list at:
                https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56
            jpg_quality (int): range from 0 to 100 (inclusive), with 100 being the best quality (least compression)
                and 0 being the worst quality (maximum compression)

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

        # save as 512x512 images
        if scale_and_slice_to_512:
            frame = scale_image_to_fill(frame)
            chunks = slice_image(frame)

            for index, chunk in enumerate(chunks):
                # Generate the output file path
                output_path = os.path.join(output_dir, f"{output_count}_frame{frame_number}_chunk{index}.{output_format}")

                if output_format.lower() in ("jpg", "jpeg"):
                    cv2.imwrite(output_path, chunk, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
                else:
                    cv2.imwrite(output_path, chunk)

                logger.debug(f"Saved frame to {output_path}")

        # save without scaling
        else:
            # Generate the output file path
            output_path = os.path.join(output_dir, f"{output_count}_frame{frame_number}.{output_format}")

            if output_format.lower() in ("jpg", "jpeg"):
                cv2.imwrite(output_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
            else:
                cv2.imwrite(output_path, frame)

            logger.debug(f"Saved frame to {output_path}")

        # Increment the counters
        output_count += 1
        frame_number += frame_interval

    # Release the video capture and close the window
    video.release()
    cv2.destroyAllWindows()
    logger.info(f"Finished extracting video {video_path}")


def slice_image(image, chunk_size_x: int = 512, chunk_size_y: int = 512):
    """
        Divide a larger image into smaller chunks side by side.
    """
    logger = logging.getLogger("data_preprocess.slice_image_square")

    image_size_x, image_size_y = image.shape[1], image.shape[0]

    if (image_size_x == chunk_size_x) and (image_size_y == chunk_size_y):
        return [image]

    if (image_size_x < chunk_size_x) or (image_size_y < chunk_size_y):
        logger.warning(
            f"Image not sliced: original image size ({image_size_x},{image_size_y}) is smaller than chunk size ({chunk_size_x},{chunk_size_y}).")
        return [image]

    # Calculate the number of chunks in x and y directions
    x_chunks = image_size_x // chunk_size_x
    y_chunks = image_size_y // chunk_size_y

    # Loop over the image and save each chunk
    chunks = []
    for y in range(y_chunks):
        for x in range(x_chunks):
            # Extract chunk
            chunk = image[y * chunk_size_y:(y + 1) * chunk_size_y, x * chunk_size_x:(x + 1) * chunk_size_x]
            chunks.append(chunk)

    return chunks


def scale_image_to_fill(image, fill_size_x: int = 512, fill_size_y: int = 512):
    """
        Scale image to fill a specific size, such that one side of the image is equal to fill size, and other side of
        image is equal or larger than the other side of
    """
    image_size_x, image_size_y = image.shape[1], image.shape[0]

    if image_size_x / image_size_y >= fill_size_x / fill_size_y:
        # Resize such that new_image_size_y equals fill_size_y, so that new_image_size_x >= fill_size_x
        new_image_size_y = fill_size_y
        new_image_size_x = int(new_image_size_y * image_size_x / image_size_y)
    else:
        # Resize such that image_size_x equals fill_size_x
        new_image_size_x = fill_size_x
        new_image_size_y = int(new_image_size_x * image_size_y / image_size_x)

    return cv2.resize(image, (new_image_size_x, new_image_size_y))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    video_path = "../demo_data/barley_10_days_old.mp4"
    output_dir = "../demo_data/test_lora_train_data"
    os.makedirs(output_dir, exist_ok=True)

    frame_interval = 30  # Extract 1 frame per 300 frames (roughly 10 secs)
    extract_frames(video_path, output_dir, frame_interval, "jpg", 50, True)

# ruff: noqa
