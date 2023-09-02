import cv2, os, configparser, sys
import numpy as np
from enum import Enum, auto

# Variables related to config
config_path = "interactive_annotator_config.ini"
config = None
flag_preferences_changed = False

class ToolMode(Enum):
    ERASER = auto()
    BRUSH = auto()
    RECTANGLE = auto()
    RECTANGLE_ERASE = auto()

# State variables for drawing
drawing = False  # true if mouse is pressed
tool_mode = ToolMode.RECTANGLE
ix, iy = -1, -1

# Variables for image display
image_aspect_ratio = 1
layer_ground = None
layer_weed = None
flag_redo_extract_ground = False
flag_redo_merge_layers = True
IMAGE_WINDOW_NAME = "PRESS KEY: [B]rush [E]raser [R]ectangle [G]RectangleErase [X]Reset [Space]Save and next [Ecs/Q]uit"


def flag_redraw():
    global flag_redo_extract_ground, flag_redo_merge_layers
    flag_redo_extract_ground = True
    flag_redo_merge_layers = True


class TrackbarParameters:
    def __init__(self):
        self.display_width = None
        self.display_mode = 0

        self.lower_h = None
        self.lower_s = None
        self.lower_v = None
        self.upper_h = None
        self.upper_s = None
        self.upper_v = None

        self.smoothing = None

        self.brush_size = None

    def callback_display_width(self, val):
        global image_aspect_ratio, IMAGE_WINDOW_NAME
        self.display_width = val
        cv2.resizeWindow(IMAGE_WINDOW_NAME, val, int(val / image_aspect_ratio))

    def callback_display_mode(self, val):
        self.display_mode = val
        flag_redraw()

    def callback_lower_h(self, val):
        self.lower_h = val
        flag_redraw()

    def callback_lower_s(self, val):
        self.lower_s = val
        flag_redraw()

    def callback_lower_v(self, val):
        self.lower_v = val
        flag_redraw()

    def callback_upper_h(self, val):
        self.upper_h = val
        flag_redraw()

    def callback_upper_s(self, val):
        self.upper_s = val
        flag_redraw()

    def callback_upper_v(self, val):
        self.upper_v = val
        flag_redraw()

    def callback_closing_size(self, val):
        self.smoothing = val
        flag_redraw()

    def callback_brush_size(self, val):
        self.brush_size = val


trackbar_parameters = TrackbarParameters()


# Mouse callback function
def callback_draw_mask(event, x, y, flags, param):
    global ix, iy, drawing, layer_weed, flag_redo_merge_layers

    brush_size = cv2.getTrackbarPos('Brush Size', "Tools Window")

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if tool_mode is ToolMode.BRUSH:
                cv2.circle(layer_weed, (x, y), brush_size, 255, -1)
                flag_redo_merge_layers = True

            elif tool_mode is ToolMode.ERASER:
                cv2.circle(layer_weed, (x, y), brush_size, 0, -1)
                flag_redo_merge_layers = True

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if tool_mode is ToolMode.RECTANGLE:
            cv2.rectangle(layer_weed, (ix, iy), (x, y), 255, -1)
            flag_redo_merge_layers = True
        elif tool_mode is ToolMode.RECTANGLE_ERASE:
            cv2.rectangle(layer_weed, (ix, iy), (x, y), 0, -1)
            flag_redo_merge_layers = True


def extract_ground(image_hsv):
    global trackbar_parameters

    # Define a mask for green color (which might represent plants)
    lower_green = np.array([trackbar_parameters.lower_h, trackbar_parameters.lower_s, trackbar_parameters.lower_v])
    upper_green = np.array([trackbar_parameters.upper_h, trackbar_parameters.upper_s, trackbar_parameters.upper_v])

    ground = cv2.inRange(image_hsv, lower_green, upper_green)

    # Apply closing operation (dilation followed by erosion)
    if trackbar_parameters.smoothing > 0:
        kernel = np.ones((trackbar_parameters.smoothing, trackbar_parameters.smoothing), np.uint8)
        ground = cv2.morphologyEx(ground, cv2.MORPH_CLOSE, kernel)

    return ground


def read_config_or_create_default():
    global config_path, config
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        config["WORK DIRECTORY"] = {
            "source image folder": "../demo_data/test_extract",
            "output image folder": "../demo_data/test_annotation",
        }
        config["ANNOTATION COLOURS BGR"] = {
            "ground": "255, 194, 0",
            "crop": "4, 255, 204",
            "weed": "7, 250, 4",
        }
        config["DISPLAY"] = {
            "width": "800",
            "mode": "0",
        }
        config["TOOL SETTING"] = {
            "lower h": "35",
            "lower s": "40",
            "lower v": "40",
            "upper h": "85",
            "upper s": "255",
            "upper v": "255",
            "smoothing": "1",
            "brush size": "50",
        }
        config["PROGRESS"] = {
            "last processed image index": "0",
            "sorted image list": "",
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)
            print(f"[CONFIG] {config_path} created with default values.")
    else:
        config.read(config_path)
        print(f"[CONFIG] {config_path} loaded")

def check_progress():
    global config, config_path

    # Get a sorted list of all image filenames in the folder
    all_images = sorted([img for img
                         in os.listdir(config["WORK DIRECTORY"]["source image folder"])
                         if img.lower().endswith((".png", ".jpg", ".jpeg"))])
    all_images_str = ", ".join(all_images)

    last_processed_image_index = int(config['PROGRESS']['last processed image index'])

    # Compare with the list stored in config, and reset "last processed image index" if list changed
    if all_images_str != config["PROGRESS"]["sorted image list"]:
        config["PROGRESS"]["sorted image list"] = all_images_str
        config["PROGRESS"]["last processed image index"] = "-1"
        last_processed_image_index = -1
        with open(config_path, 'w') as configfile:
            config.write(configfile)
            print(f"[CONFIG] Image list has changed since last execution. {config_path} updated with new image list")

    # Exit if all images processed
    elif last_processed_image_index >= len(all_images) - 1:
        print(f"[CONFIG] All images in the source folder "
              f"{config['WORK DIRECTORY']['source image folder']} has been processed. ")
        sys.exit("Annotation completed. Please select another folder in config and restart the programme.")

    # Continue on previous progress
    else:
        print(f"[CONFIG] Detected previous progress. The last processed image is "
              f"{all_images[last_processed_image_index]}.")
        print(f"[CONFIG] Start working on {all_images[last_processed_image_index + 1]}")

    return all_images, last_processed_image_index


def get_next_image(all_images, current_image_index):
    global config, config_path

    if current_image_index >= len(all_images) - 1:
        print(f"[CONFIG] All images in the source folder "
              f"{config['WORK DIRECTORY']['source image folder']} has been processed. ")
        sys.exit("Please select another folder and restart the programme.")

    else:
        # open image
        next_image_index = current_image_index + 1
        image_path = os.path.join(config["WORK DIRECTORY"]["source image folder"], all_images[next_image_index])
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)

        # update config file
        config["PROGRESS"]["last processed image index"] = str(current_image_index)


        with open(config_path, 'w') as configfile:
            config.write(configfile)
            print(f"[CONFIG] The last processed image record has been updated to {all_images[current_image_index]}")
            print(f"[WORKFLOW] Start working on image {all_images[next_image_index]}")

        return image, next_image_index


def save_annotated_image(image_shape, image_name):
    global layer_ground, layer_weed, config

    # Start with image filled with crop colour
    annotated_image = np.full(image_shape,
                              tuple(map(int, config["ANNOTATION COLOURS BGR"]["crop"].split(', '))), dtype=np.uint8)

    # Find the pixels where the layer_weed is 255 (i.e., weed pixels)
    weed_indices = np.where(layer_weed == 255)
    # Add weed annotation
    annotated_image[weed_indices[0], weed_indices[1], :] = \
        tuple(map(int, config["ANNOTATION COLOURS BGR"]["weed"].split(', ')))

    # Find the pixels where the layer_ground is 0 (i.e., ground pixels)
    ground_indices = np.where(layer_ground == 0)
    # Add ground annotation
    annotated_image[ground_indices[0], ground_indices[1], :] = \
        tuple(map(int, config["ANNOTATION COLOURS BGR"]["ground"].split(', ')))

    # Save image
    os.makedirs(config["WORK DIRECTORY"]["output image folder"], exist_ok=True)
    filename, extension = os.path.splitext(image_name)
    output_path = os.path.join(config["WORK DIRECTORY"]["output image folder"], filename + ".png")
    cv2.imwrite(output_path, annotated_image)

    return annotated_image, output_path


def interactive_annotator(image_path):
    global layer_ground, layer_weed, image_aspect_ratio, tool_mode, trackbar_parameters, \
        flag_redo_extract_ground, flag_redo_merge_layers, IMAGE_WINDOW_NAME, config_path, config

    # Load config file, and create one if none exists
    read_config_or_create_default()

    # Check progress
    all_images, last_processed_image_index = check_progress()

    # Open next image
    image, current_image_index = get_next_image(all_images, last_processed_image_index)
    image_aspect_ratio = image.shape[1] / image.shape[0]

    # Windows setup
    cv2.namedWindow("Tools Window", cv2.WINDOW_NORMAL)
    cv2.namedWindow(IMAGE_WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(IMAGE_WINDOW_NAME, callback_draw_mask)

    # Trackbars
    cv2.createTrackbar("Disp Width", "Tools Window", int(config["DISPLAY"]["width"]), 2000,
                       trackbar_parameters.callback_display_width)
    cv2.createTrackbar("Disp Mode", "Tools Window", int(config["DISPLAY"]["mode"]), 3,
                       trackbar_parameters.callback_display_mode)
    cv2.createTrackbar('Lower H', "Tools Window", int(config["TOOL SETTING"]["lower h"]), 179,
                       trackbar_parameters.callback_lower_h)
    cv2.createTrackbar('Lower S', "Tools Window", int(config["TOOL SETTING"]["lower s"]), 255,
                       trackbar_parameters.callback_lower_s)
    cv2.createTrackbar('Lower V', "Tools Window", int(config["TOOL SETTING"]["lower v"]), 255,
                       trackbar_parameters.callback_lower_v)
    cv2.createTrackbar('Upper H', "Tools Window", int(config["TOOL SETTING"]["upper h"]), 179,
                       trackbar_parameters.callback_upper_h)
    cv2.createTrackbar('Upper S', "Tools Window", int(config["TOOL SETTING"]["upper s"]), 255,
                       trackbar_parameters.callback_upper_s)
    cv2.createTrackbar('Upper V', "Tools Window", int(config["TOOL SETTING"]["upper v"]), 255,
                       trackbar_parameters.callback_upper_v)
    cv2.createTrackbar('Smoothing', "Tools Window", int(config["TOOL SETTING"]["smoothing"]), 30,
                       trackbar_parameters.callback_closing_size)
    cv2.createTrackbar('Brush Size', "Tools Window", int(config["TOOL SETTING"]["brush size"]), 300,
                       trackbar_parameters.callback_brush_size)

    # Image window resize
    target_window_width = cv2.getTrackbarPos("Disp Width", "Tools Window")
    cv2.resizeWindow(IMAGE_WINDOW_NAME, target_window_width, int(target_window_width / image_aspect_ratio))

    # Convert the image from BGR to HSV (Hue, Saturation, Value)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Initialize layers
    layer_weed = np.zeros_like(image[:, :, 0])
    layer_ground = extract_ground(image_hsv)
    layer_merged_display_bgr = None

    # GUI main loop
    while True:
        if flag_redo_extract_ground:
            layer_ground = extract_ground(image_hsv)
            flag_redo_extract_ground = False

        if flag_redo_merge_layers:
            # start with deep-copying an image
            layer_merged_display_bgr = image.copy()

            # Find the pixels where the layer_ground is 0 (i.e., ground pixels)
            ground_indices = np.where(layer_ground == 0)
            # Find the pixels where the layer_weed is 255 (i.e., weed pixels)
            weed_indices = np.where(layer_weed == 255)

            # Different display mode:
            if trackbar_parameters.display_mode == 0:
                # Replace weed with red
                layer_merged_display_bgr[weed_indices[0], weed_indices[1], :] = (100,100,220)

                # Darken the ground area
                layer_merged_display_bgr[ground_indices[0], ground_indices[1], :] = \
                        image[ground_indices[0], ground_indices[1], :] // 3

            # do nothing when mode==1, i.e., show original image for reference

            elif trackbar_parameters.display_mode == 2:
                # Replace weed with red
                layer_merged_display_bgr[weed_indices[0], weed_indices[1], :] = (100, 100, 220)

                # replace ground with grey
                layer_merged_display_bgr[ground_indices[0], ground_indices[1], :] = (127,127,127)

            elif trackbar_parameters.display_mode == 3:
                # Replace weed with black
                layer_merged_display_bgr[weed_indices[0], weed_indices[1], :] = (0, 0, 0)

                # replace ground with red
                layer_merged_display_bgr[ground_indices[0], ground_indices[1], :] = (100,100,220)

            flag_redo_merge_layers = False

        # Display the segmented view
        cv2.imshow(IMAGE_WINDOW_NAME, layer_merged_display_bgr)

        # keyboard event
        key = cv2.waitKey(1) & 0xFF

        if key == ord('b'):
            tool_mode = ToolMode.BRUSH
        elif key == ord('e'):
            tool_mode = ToolMode.ERASER
        elif key == ord('r'):
            tool_mode = ToolMode.RECTANGLE
        elif key == ord('g'):
            tool_mode = ToolMode.RECTANGLE_ERASE
        elif key == ord('x'):
            layer_weed = np.zeros_like(image[:, :, 0])
            flag_redo_merge_layers = True
        elif key == ord('q') or key == 27:
            # press "q" or "esc" to quit
            break
        elif key == 32:
            # press "space" to save and preview annotated image
            annotated_image, output_path = save_annotated_image(image.shape, all_images[current_image_index])
            cv2.imshow("Tools Window", annotated_image)

            print(f"[WORKFLOW] Progress [{current_image_index + 1}/{len(all_images)}]. "
                  f"Annotated image saved to {output_path}. ")

            # switch to next image
            image, current_image_index = get_next_image(all_images, current_image_index)

            # resize window if aspect ratio changed
            if image_aspect_ratio != image.shape[1] / image.shape[0]:
                image_aspect_ratio = image.shape[1] / image.shape[0]
                target_window_width = cv2.getTrackbarPos("Disp Width", "Tools Window")
                cv2.resizeWindow(IMAGE_WINDOW_NAME, target_window_width, int(target_window_width / image_aspect_ratio))

            # Convert the image from BGR to HSV (Hue, Saturation, Value)
            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Reset layers
            layer_weed = np.zeros_like(image[:, :, 0])
            flag_redraw()


        # if window closed, break
        if cv2.getWindowProperty("Tools Window", cv2.WND_PROP_VISIBLE) < 1 or \
                cv2.getWindowProperty(IMAGE_WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()


# Test the function
interactive_annotator("../demo_data/test_extract/2_frame_600.jpg")
