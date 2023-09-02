import cv2, os, configparser
import numpy as np
from enum import Enum, auto


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
IMAGE_WINDOW_NAME = "PRESS KEY: [B]rush [E]raser [R]ectangle [G]RectangleErase " \
                    "[X]Reset [Space]Save and next [<-]Back [Ecs/Q]uit"


def redraw():
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
        redraw()

    def callback_lower_h(self, val):
        self.lower_h = val
        redraw()

    def callback_lower_s(self, val):
        self.lower_s = val
        redraw()

    def callback_lower_v(self, val):
        self.lower_v = val
        redraw()

    def callback_upper_h(self, val):
        self.upper_h = val
        redraw()

    def callback_upper_s(self, val):
        self.upper_s = val
        redraw()

    def callback_upper_v(self, val):
        self.upper_v = val
        redraw()

    def callback_closing_size(self, val):
        self.smoothing = val
        redraw()

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


def read_config_or_create_default(config_path):
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
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
        config["WORK DIRECTORY"] = {
            "source image folder": "../demo_data/test_extract",
            "last processed image index": "0",
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        print(f"{config_path} created with default values.")
    else:
        config.read(config_path)
        print(f"{config_path} loaded")

    return config


def interactive_annotator(image_path):
    global layer_ground, layer_weed, image_aspect_ratio, tool_mode, trackbar_parameters, \
        flag_redo_extract_ground, flag_redo_merge_layers, IMAGE_WINDOW_NAME

    # Load config file, and create one if none exists
    config_path = "interactive_annotator_config.ini"
    config = read_config_or_create_default(config_path)



    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image_aspect_ratio = image.shape[1] / image.shape[0]

    # Convert the image from BGR to HSV (Hue, Saturation, Value)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Initial definition
    layer_ground = np.zeros_like(image[:, :, 0])
    layer_weed = np.zeros_like(image[:, :, 0])

    cv2.namedWindow("Tools Window", cv2.WINDOW_NORMAL)

    cv2.namedWindow(IMAGE_WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(IMAGE_WINDOW_NAME, callback_draw_mask)

    # Image window resize
    cv2.createTrackbar("Disp Width", "Tools Window", 800, 2000, trackbar_parameters.callback_display_width)
    target_window_width = cv2.getTrackbarPos("Disp Width", "Tools Window")
    cv2.resizeWindow(IMAGE_WINDOW_NAME, target_window_width, int(target_window_width / image_aspect_ratio))

    cv2.createTrackbar("Disp Mode", "Tools Window", 0, 3, trackbar_parameters.callback_display_mode)

    # Trackbars for HSV thresholds
    cv2.createTrackbar('Lower H', "Tools Window", 35, 179, trackbar_parameters.callback_lower_h)
    cv2.createTrackbar('Lower S', "Tools Window", 40, 255, trackbar_parameters.callback_lower_s)
    cv2.createTrackbar('Lower V', "Tools Window", 40, 255, trackbar_parameters.callback_lower_v)
    cv2.createTrackbar('Upper H', "Tools Window", 85, 179, trackbar_parameters.callback_upper_h)
    cv2.createTrackbar('Upper S', "Tools Window", 255, 255, trackbar_parameters.callback_upper_s)
    cv2.createTrackbar('Upper V', "Tools Window", 255, 255, trackbar_parameters.callback_upper_v)

    # Trackbars for smoothing operations
    cv2.createTrackbar('Smoothing', "Tools Window", 1, 30, trackbar_parameters.callback_closing_size)

    # Trackbars for drawing tools
    cv2.createTrackbar('Brush Size', "Tools Window", 50, 300, trackbar_parameters.callback_brush_size)

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
            # press "space" to save

            # annotation colour
            ANNOTATION_BGR_GROUND = (255, 194, 0)
            ANNOTATION_BGR_CROP = (4, 255, 204)
            ANNOTATION_BGR_WEED = (7, 250, 4)

            # Start with image filled with crop colour
            annotated_image = np.full(image.shape, ANNOTATION_BGR_CROP, dtype=np.uint8)

            # Find the pixels where the layer_weed is 255 (i.e., weed pixels)
            weed_indices = np.where(layer_weed == 255)
            # Add weed annotation
            annotated_image[weed_indices[0], weed_indices[1], :] = ANNOTATION_BGR_WEED

            # Find the pixels where the layer_ground is 0 (i.e., ground pixels)
            ground_indices = np.where(layer_ground == 0)
            # Add ground annotation
            annotated_image[ground_indices[0], ground_indices[1], :] = ANNOTATION_BGR_GROUND

            cv2.imshow("Tools Window", annotated_image)

        # if window closed, break
        if cv2.getWindowProperty("Tools Window", cv2.WND_PROP_VISIBLE) < 1 or \
                cv2.getWindowProperty(IMAGE_WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()


# Test the function
interactive_annotator("../demo_data/test_extract/2_frame_600.jpg")
